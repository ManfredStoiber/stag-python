#include "submodules/pybind11_opencv_numpy/ndarray_converter.h"
#include <pybind11/cast.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "StagWrapper.cpp"
namespace py = pybind11;
using namespace py::literals;

PYBIND11_MODULE(stag, m) {
  NDArrayConverter::init_numpy();
  m.def("detectMarkers", &detectMarkers, "Detect STag markers in image. Returns (corners, ids) of detected markers.");
}