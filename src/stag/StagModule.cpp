#include "ndarray_converter.h"
#include <pybind11/cast.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>
#include "../../submodules/stag/src/Marker.h"
#include "../../submodules/stag/src/Stag.h"
using cv::Mat;

namespace py = pybind11;
using namespace py::literals;

py::tuple cornersToTuple(const std::vector<std::vector<cv::Point2f>>& corners) {
    py::tuple ret = py::tuple(corners.size());
    for (int i=0; i<corners.size(); i++) {
        std::vector<std::vector<float>> contours_vec;
        for (cv::Point2f pt : corners[i]) {
            contours_vec.push_back({static_cast<float>((int)pt.x), static_cast<float>((int)pt.y)});
        }
        py::array_t<std::float_t> contours = py::cast(contours_vec);
        ret[i] = contours.reshape({1, 4, 2});
    }
    return ret;
}

py::array idsToArray(const std::vector<int>& ids) {
    py::array_t<std::int32_t > ret_id = py::cast(ids);
    return ret_id.reshape({-1, 1});
}

std::vector<std::vector<cv::Point2f>> cornersToVector(py::iterable& corners) {
    std::vector<std::vector<cv::Point2f>> corners_vec;
    for (auto tmp : corners) {
        std::vector<cv::Point2f> contours_vec;
        for (std::vector<float> pt : tmp.cast<py::array>().reshape({4, 2}).cast<std::vector<std::vector<float>>>()) {
            contours_vec.emplace_back(pt[0], pt[1]);
        }
        corners_vec.push_back(contours_vec);
    }
    return corners_vec;
}

std::vector<int> idsToVector(py::iterable& ids) {
    auto ids_array = py::cast<py::array>(ids);
    auto ids_vec = std::vector<int>();
    auto ids_flat = ids_array.reshape({-1});

    for (py::handle id : ids_flat) {
        ids_vec.push_back(id.cast<int>());
    }

    return ids_vec;
}

cv::Scalar borderColorToScalar(const py::iterable& borderColor) {
    if (len(borderColor) != 3) {
        throw std::invalid_argument("Invalid value for border color.");
    }
    auto color = borderColor.cast<std::vector<int>>();
    return cv::Scalar(color[0], color[1], color[2]);
}

/**
 * Detects markers in given image.
 * @param inImage OpenCV Matrix of input image.
 * @param libraryHD The library HD that is used. Possible values are [11,&nbsp;13,&nbsp;15,&nbsp;17,&nbsp;19,&nbsp;21,&nbsp;23].
 * @param errorCorrection The amount of error correction that is going to be used.
 *  Value needs to be in range 0&nbsp;\<=&nbsp;errorCorrection&nbsp;\<=&nbsp;(HD-1)/2.\n
 *  If set to -1, the max possible value for the given library HD is used.
 * @returns Tuple of (corners, ids, rejectedImgPoints) of detected markers
 */
py::tuple detectMarkers(const Mat &image, int libraryHD, int errorCorrection=-1) {
    auto corners = std::vector<std::vector<cv::Point2f>>();
    auto ids = std::vector<int>();
    auto rejectedImgPoints = std::vector<std::vector<cv::Point2f>>();

    stag::detectMarkers(image, libraryHD, corners, ids, errorCorrection, rejectedImgPoints);

    // convert corners to python opencv format
    auto ret_corners = cornersToTuple(corners);

    // convert ids to python opencv format
    auto ret_ids = idsToArray(ids);

    // convert rejectedImgPoints to python opencv format
    auto ret_rejectedImgPoints = cornersToTuple(rejectedImgPoints);

    py::tuple ret = py::make_tuple(ret_corners, ret_ids, ret_rejectedImgPoints);
    return ret;
}

/**
 * Draw detected markers in image
 * @param image Input/output image. It must have 1 or 3 channels. The number of channels is not altered.
 * @param corners Position of marker corners on input image. For N detected markers, the dimensions of this array should be Nx4.
 * @param ids Vector of identifiers for markers in param @corners.
 * @param borderColor Color (BGR) of marker borders.
 */
Mat& drawDetectedMarkers(Mat& image,
                         py::iterable& corners,
                         py::iterable ids = py::array(),
                         const py::iterable& borderColor = py::make_tuple(50, 255, 50) ) {

    std::vector<std::vector<cv::Point2f>> corners_vec = cornersToVector(corners);
    std::vector<int> ids_vec = idsToVector(ids);
    cv::Scalar borderColor_scalar = borderColorToScalar(borderColor);

    stag::drawDetectedMarkers(image, corners_vec, ids_vec, borderColor_scalar);

    return image;
}

PYBIND11_MODULE(_core, m) {
    NDArrayConverter::init_numpy();
    m.def("detectMarkers",
          &detectMarkers,
          "image"_a,
          "libraryHD"_a,
          "errorCorrection"_a=-1,
          "Detect STag markers in given image.\n"
          "\n"
          "Parameters:\n"
          " image : ndarray (HxWxC)\n"
          "     OpenCV Matrix of input image. Supported are images with 1, 3 and 4 channels.\n"
          " libraryHD : int\n"
          "     The HD library that is used. Possible values are [11, 13, 15, 17, 19, 21, 23].\n"
          " errorCorrection : int, optional\n"
          "     The amount of error correction that is going to be used.\n"
          "     Value needs to be in range 0 <= errorCorrection <= (HD-1)/2.\n"
          "     If omitted or set to -1, the max possible value for the given HD library is used.\n"
          "\n"
          "Returns:\n"
          " (corners, ids, rejectedImgPoints) of detected markers.");
    m.def("drawDetectedMarkers",
          &drawDetectedMarkers,
          "image"_a,
          "corners"_a,
          "ids"_a=py::array(),
          "border_color"_a=py::make_tuple(50, 255, 50),
          "Draw detected markers in image.\n"
          "\n"
          " image : ndarray (HxWxC)\n"
          "     Input/output image. The number of channels is not altered.\n"
          " corners : iterable (Nx4)\n"
          "     Position of marker corners on input image. For N detected markers, the dimensions of this iterable should be Nx4.\n"
          " ids : iterable\n"
          "     Iterable of identifiers for markers in param corners.\n"
          " border_color : tuple (b, g, r)\n"
          "     Color of marker borders.");

}
