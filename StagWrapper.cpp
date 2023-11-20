#include<vector>
#include "submodules/stag/src/Marker.h"
#include "submodules/stag/src/Stag.h"
using cv::Mat;

std::vector<std::vector<std::vector<double>>> getCorners(Stag *stag) {

    std::vector<std::vector<std::vector<double>>> ret;
    for (Marker marker : stag->markers) {
        std::vector<std::vector<double>> contours;
        for (cv::Point2d pt : marker.corners) {
            contours.push_back({pt.x, pt.y});
        }
        ret.push_back(contours);
    }
    return ret;
}

std::vector<int> getIds(Stag *stag) {
    std::vector<int> ret;
    for (Marker marker : stag->markers) {
        ret.push_back(marker.id);
    }
    return ret;
}

std::tuple<std::vector<std::vector<std::vector<double>>>, std::vector<int>> detectMarkers(Mat inImage) {
    Stag stag(21, 7, true);
    stag.detectMarkers(inImage);
    return std::tuple<std::vector<std::vector<std::vector<double>>>, std::vector<int>>{getCorners(&stag), getIds(&stag)};
}
