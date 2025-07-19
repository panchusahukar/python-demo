// video_checker.cpp

#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

string check_frame_fake(const Mat &frame) {
    // Dummy condition: based on average brightness
    Scalar avg = mean(frame);
    if (avg[0] < 90) return "Fake";
    return "Real";
}

int main() {
    string path = "test_video.mp4";
    VideoCapture cap(path);

    if (!cap.isOpened()) {
        cerr << "Error opening video file.\n";
        return -1;
    }

    int frameCount = 0, fakeCount = 0;
    Mat frame;

    while (cap.read(frame) && frameCount < 30) {
        string result = check_frame_fake(frame);
        if (result == "Fake") fakeCount++;
        frameCount++;
    }

    cap.release();

    float fakeRatio = (float)fakeCount / frameCount;
    string finalLabel = (fakeRatio > 0.3) ? "Fake" : "Real";

    cout << "Final result: " << finalLabel << " (Fake ratio: " << fakeRatio << ")\n";
    return 0;
}
