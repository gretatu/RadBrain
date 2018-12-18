A toolbox for implementing text in the gyri of a (real) brain surface reconstruction using a pretrained deep VGG-19 network.

*In collaboration with [Matt Siegelman](https://github.com/msieg), Massachusetts Institute of Technology, 2018.*

#### Dependencies:

- tensorflow
- opencv

#### Usage:
- Clone this repository.
- After installing the dependencies:
  Download the VGG-19 model weights (see the ["VGG-VD models from the Very Deep Convolutional Networks for Large-Scale Visual Recognition project" section](http://www.vlfeat.org/matconvnet/pretrained/)). More info about the VGG-19 network can be found [here](http://www.robots.ox.ac.uk/~vgg/research/very_deep/).
  After downloading, copy the weights file imagenet-vgg-verydeep-19.mat to the project directory.

- Run the python script RadBrain.py, which will ask you to enter the word you wish to write in the gyri.
- Wait. 
- The result will be located in the /output/ folder.

#### Acknowledgements

The implementation is based on the projects:

- TensorFlow implementation of VGG-19 'neural-style-tf' by [cysmith](https://github.com/cysmith/neural-style-tf).

- Brain surface reconstruction is made with [Freesurfer 6.0.0](https://surfer.nmr.mgh.harvard.edu/) and processed in [MeshLab](http://www.meshlab.net/). 
