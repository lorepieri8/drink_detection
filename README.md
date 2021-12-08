# Drink Detection

Simple scripts to generate an arbitrary large synthetic dataset starting from 3d models and train a neural network to recognise real objects.
The script performs also randomisation, by varying the models background, lighting, texture, etc
To get better result on real objects I suggest to also augment the dataset with real pictures.

## Build the synthetic dataset

- Install Blender 2.93.6

- Install zpy (https://zumolabs.github.io/zpy/zpy/install/pip/) and zpy add-on (https://zumolabs.github.io/zpy/addon/install/). For more info: (https://github.com/ZumoLabs/zpy)
Make sure to install zpy with the python blender, not your system python.
See https://blender.stackexchange.com/a/122337/116831 as an example of installing python modules in blender.

- Load the .blend file, load the run.py script + config.gin and run the simulation (press "Run" in the Execute tab) in the zpy add-on.

## Train and Evaluate a detection model

If in Colab:
- Zip the output folder containing the dataset and the target images.
- Upload the two zip files to a colab instance
- Run the notebook

To run locally:
- Install Detectron2 (Linux has binaries, Mac need install from source, Win not supported) (https://github.com/facebookresearch/detectron2/blob/main/INSTALL.md)


## About the neural network:

The detector uses detectron2, and in particular it starts training from a pretrained Mask-RCNN with Feature Pyramide Network architecture, which is suited for both instance segmentation and object detection tasks.
Mask RCNN is a region based convolutional neural network, which works by first extracting region proposals and then predictin which object is inside. Thanks to a pooling of region of interests (ROI Pooling) images of any size are allowed and thanks to the Feature Pyramide Network architecture the detector is able to detect objects at multiple scales, from small to large.
