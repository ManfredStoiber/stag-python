# This file is heavily inspired by: https://github.com/pybind/cmake_example/blob/master/setup.py
opencv_version = "4.8.1"

import os
import re
import subprocess
import sys
from pathlib import Path

import requests
import zipfile

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib

from distutils.dir_util import mkpath

def get_install_path():
    return sys.prefix

# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        # Must be in this form due to bug in .resolve() only fixed in Python 3.10+
        ext_fullpath = Path.cwd() / self.get_ext_fullpath(ext.name)
        extdir = ext_fullpath.parent.resolve()

        # Using this requires trailing slash for auto-detection & inclusion of
        # auxiliary "native" libs

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        cmake_args = [
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
        ]
        
        cmake_stag_args = [
            # Set output directory for generated shared libraries
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}{os.sep}stag",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}{os.sep}stag",
        ]
        
        build_args = []
        # Adding CMake arguments set as environment variable
        # (needed e.g. to build for ARM OSx on conda-forge)
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator or cmake_generator == "Ninja":
                try:
                    import ninja

                    ninja_executable_path = Path(ninja.BIN_DIR) / "ninja"
                    cmake_args += [
                        "-GNinja",
                        f"-DCMAKE_MAKE_PROGRAM:FILEPATH={ninja_executable_path}",
                    ]
                except ImportError:
                    pass

        else:
            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                ]
                build_args += ["--config", cfg]

        if sys.platform.startswith("darwin"):
            # Cross-compile support for macOS - respect ARCHFLAGS if set
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += [f"-j{self.parallel}"]

        build_temp_stag = Path(self.build_temp) / ext.name
        if not build_temp_stag.exists():
            build_temp_stag.mkdir(parents=True)

        build_temp_opencv = Path(self.build_temp) / "opencv"
        if not build_temp_opencv.exists():
            build_temp_opencv.mkdir(parents=True)

        # exclude modules not required
        opencv_exclude_modules = [
            "ts",
            "stitching",
            "objdetect",
            "photo",
            "ml",
            "python3"
        ]
        opencv_exclude_modules_args = [f"-DBUILD_opencv_{module}=OFF" for module in opencv_exclude_modules]

        # download OpenCV
        print(f"Downloading OpenCV {opencv_version}..", flush=True)
        url = f"https://github.com/opencv/opencv/archive/refs/tags/{opencv_version}.zip"
        r = requests.get(url, allow_redirects=True)

        print(f"Extracting OpenCV {opencv_version}..", flush=True)
        opencv_zipfile = f"{self.build_temp}/opencv.zip"
        open(opencv_zipfile, "wb").write(r.content)
        with zipfile.ZipFile(opencv_zipfile, 'r') as zip_ref:
            zip_ref.extractall(f"{ext.sourcedir}/submodules")

        # compile and install OpenCV
        subprocess.run(
            ["cmake", ext.sourcedir + f"/submodules/opencv-{opencv_version}", f"-DCMAKE_INSTALL_PREFIX={get_install_path()}", *opencv_exclude_modules_args, *cmake_args], cwd=build_temp_opencv, check=True
        )
        subprocess.run(
            ["cmake", "--build", ".", "-j10", *build_args], cwd=build_temp_opencv, check=True
        )
        subprocess.run(
            ["cmake", "--install", ".", *build_args], cwd=build_temp_opencv, check=True
        )

        # compile stag
        subprocess.run(
            ["cmake", ext.sourcedir, *cmake_args, *cmake_stag_args], cwd=build_temp_stag, check=True
        )
        subprocess.run(
            ["cmake", "--build", ".", *build_args], cwd=build_temp_stag, check=True
        )

setup(
    ext_modules=[
        CMakeExtension("stag"),
    ],
    cmdclass={"build_ext": CMakeBuild},
)
