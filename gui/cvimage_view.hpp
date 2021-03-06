//
//  cvimage_view.hpp
//  CameraCalibration
//
//  Created by jimmy on 2019-02-02.
//  Copyright © 2019 Nowhere Planet. All rights reserved.
//

#ifndef cvimage_view_hpp
#define cvimage_view_hpp

#include <stdio.h>
#include <iostream>
#include <opencv2/core/core.hpp>
#include <vgl/vgl_line_segment_2d.h>

#include "cvui.h"   

using cv::Mat;

enum AnnotationState { point, line, circle };

class CVImageView {

private:
	std::string window_name_;
	cv::Point image_pos_;

	cv::Size window_size_;
	cv::Size image_size_;

	Mat image_;
	Mat image_after_scale_;



protected:
	// These three vectors are used to draw annotations on windows only, no transformation of coordinates

	// ordinary points
	std::vector<cv::Point> windows_points_;

	// to distinguish from ordinary points, use other color
	std::vector<cv::Point> windows_points_circle_;

	// lines
	std::vector<std::pair<cv::Point, cv::Point>> windows_line_;

	AnnotationState state_;

public:
	Mat frame_;

public:
	CVImageView(std::string name);
	virtual ~CVImageView();

	std::string getWindowName() const;
	void setWindowName(std::string name);

	cv::Size getWindowSize() const;
	void setWindowSize(cv::Size size);

	cv::Point getImagePosition() const;
	void setImagePosition(cv::Point p);

	// set/get image
	Mat getImage() const;
	void setImage(const Mat& img);

	// set/get image Size
	cv::Size getImageSize() const;
	void setImageSize(cv::Size size);

	// exchange between window point and image point
	cv::Point windowPointForImagePoint(const cv::Point& p) const;
	cv::Point imagePointForWindowPoint(const cv::Point& p) const;

	void drawFrame();
	void drawPoint(cv::Point p, cv::Scalar color);
	void drawLine(std::pair<cv::Point, cv::Point> line, cv::Scalar color);

	void setState(AnnotationState state);

	// interface
	// subclasses must draw annotation (point, line)

	virtual void annotate() = 0;

	virtual void clearAnnotations() = 0;
};

#endif /* cvimage_view_hpp */
