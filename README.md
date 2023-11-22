[![Build and upload to PyPI](https://github.com/ManfredStoiber/stag-python/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ManfredStoiber/stag-python/actions/workflows/python-publish.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stag-python)


# Python Wrapper for [STag - A Stable, Occlusion-Resistant Fiducial Marker System](https://github.com/ManfredStoiber/stag)

## 📊 Comparison Between Different Marker Systems:
[<img src="https://github.com/ManfredStoiber/stag/assets/47210077/668ca457-33dd-4ce7-8b94-662c7a5bb4d9" width="400" height="200" />](https://www.youtube.com/watch?v=vnHI3GzLVrY)

## 📖 Usage
### Installation
`pip install stag-python`


### Example
Note: in this example cv2 is used for loading the image. To use cv2, you need to install opencv-python: `pip install opencv-python`
```Python
import stag
import cv2

# specify marker type
libraryHD = 21

# load image
image = cv2.imread("example.jpg")

# detect markers
(corners, ids, rejected_corners) = stag.detectMarkers(image, libraryHD)
```

For a more comprehensive example refer to [example.py](https://github.com/ManfredStoiber/stag-python/blob/master/example/example.py)

## 🏷 Markers

- Markers can be downloaded here: [Drive](https://drive.google.com/drive/folders/0ByNTNYCAhWbIV1RqdU9vRnd2Vnc?resourcekey=0-9ipvecbezW8EWUva5GBQTQ&usp=sharing)
- Reference code for Marker Generator: [ref/marker_generator](https://github.com/ManfredStoiber/stag/tree/master/ref/marker_generator)

## 🛠 Configuration
Following parameters can be specified:
- __`libraryHD`__:
   - Sets the "family" or "type" of used STag markers
      - Each library has a different amount of markers
      - Only the markers of the chosen library will be detected
   - The following HD libraries are possible:

        | __HD__           | 11     | 13    | 15  | 17  | 19 | 21 | 23 |
        |------------------|--------|-------|-----|-----|----|----|----|
        | __Library Size__ | 22,309 | 2,884 | 766 | 157 | 38 | 12 | 6  |

   - Specifies the used Hamming Distance, for further information refer to the [original paper](https://arxiv.org/abs/1707.06292)


- __`errorCorrection`__:
   - Sets the amount of error correction
   - Has to be in range `0 <= errorCorrection <= (libraryHD-1)/2`
   - For further information refer to the [original paper](https://arxiv.org/abs/1707.06292)

## 📋 Build From Source
0. __Install__ Prerequisites

   [__CMake__ >= 3.16](https://cmake.org/getting-started/)
   - On Linux: `apt install cmake`

   [__OpenCV__ 4](https://opencv.org/get-started/) for C++
   - On Linux: `apt install libopencv-dev`
   
   __NumPy__: `pip install numpy`
     - On Linux: if during step 2 the error `"numpy/ndarrayobject.h: No such file or directory"` occurs, try one of following solutions:
         - Run `apt install python-numpy` or
         - Search for "ndarrayobject.h" (`find / -name ndarrayobject.h`) and create a symlink from its parent directory to "/usr/include/numpy" (e.g. `ln -s /usr/local/lib/python3.8/dist-packages/numpy/core/include/numpy /usr/include/numpy`)
1. __Clone__ this repository recursively:
   - `git clone --recursive https://github.com/ManfredStoiber/stag-python`
2. __Build__ the project

   In the project directory, run the following command:

   - `pip install .`
3. __Run__ the example
    1. `cd example`
    2. `python example.py`

## 📰 Originally Published in the Following Paper:

[B. Benligiray; C. Topal; C. Akinlar, "STag: A Stable Fiducial Marker System," Image and Vision Computing, 2019.](https://arxiv.org/abs/1707.06292)

<p align="center">
  <img src="https://user-images.githubusercontent.com/19530665/57179654-c0c11e00-6e88-11e9-9ca5-0c0153b28c91.png"/>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/19530665/57179660-cae31c80-6e88-11e9-8f80-bf8e24e59957.png"/>
</p>

