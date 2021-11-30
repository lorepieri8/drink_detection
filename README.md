# Drink Detection

## Build the synthetic dataset

-Install Blender 2.93.6
-Install zpy and zpy add-on (https://github.com/ZumoLabs/zpy)
-Load the .blend file, load the run.py script + config.gin and run the simulation (press "Run" in the Execute tab) in the zpy add-on.

## Train and Evaluate a detection model

If in Colab:
    -Zip the output folder containing the dataset and the target images.
    -Upload the two zip files to a colab instance

-Run the notebook


# About the neural network:

The detector uses detectron2, and in particular it starts training from a pretrained Mask-RCNN with Feature Pyramide Network architecture, which is suited for both instance segmentation and object detection tasks.
Mask RCNN is a region based convolutional neural network, which works by first extracting region proposals and then predictin which object is inside. Thanks to a pooling of region of interests (ROI Pooling) images of any size are allowed and thanks to the Feature Pyramide Network architecture the detector is able to detect objects at multiple scales, from small to large.
