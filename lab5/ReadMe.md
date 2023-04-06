# Week 6 Lab 05
- Author: Joo Kai Tay
- Student number: 22489437

To pick a colour in the HSV colour map, we select two values of hue to search between. A lower threshold and a upper threshold. The saturation and value values are set to 0 for the lower threshold and 255 for the upper threshold. 

In OpenCV, hue values go from 0-180

## Approach
- Image is read in BGR colour space. So we convert it to HSV colour space
- Define the range of colour we want to search for using the sliders and create HSV mask
- Threshold the HSV image to only get the colours we defined in step 2

## Iris Image
- Lower threshold: 0
- Upper threshold: 81

## Peppers Image
- Lower threshold: 0
- Upper threshold: 108