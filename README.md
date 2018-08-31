# GPdoemd
[![Build Status](https://travis-ci.org/cog-imperial/GPdoemd.svg?branch=dev)](https://travis-ci.org/cog-imperial/GPdoemd/branches) [![codecov](https://codecov.io/gh/cog-imperial/GPdoemd/branch/dev/graph/badge.svg)](https://codecov.io/gh/cog-imperial/GPdoemd/branch/dev) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python package based on the following paper presented at ICML 2018  
[**Design of experiments for model discrimination using Gaussian process surrogate models.**](http://proceedings.mlr.press/v80/olofsson18a.html)
```
@inproceedings{Olofsson2018a,
  author    = {Simon Olofsson and Marc Peter Deisenroth and Ruth Misener},
  title     = {Design of experiments for model discrimination hybridising analytical and data-driven approaches},
  booktitle = {ICML '18: Proceedings of the International Conference on Machine Learning},
  address   = {Stockholm, Sweden},
  year      = {2018},
}
```

## Background
Here we provide a brief introduction to design of experiments for model discrimination, and the method used in the GPdoemd package. For more information, we refer to the paper referenced above.

##### Design of experiments for model discrimination
We are interested in some system $$g$$ (e.g. the human body, a bioreactor, or a chemical reaction), from which we can generate data constisting of noisy observations $$\mathbf y = g(\mathbf x)$$ given experimental designs $$\mathbf x$$. To predict the bahviour of the system, the engineers and researchers come up with several competing models $$f_i$$, $$i=1,\dots,M$$. The models produce predictions $$f_i(\mathbf x, \mathbf \theta_i)$$ given some model parameters $$\mathbf \theta_i$$. In a classical setting, these model parameters are tuned to make the model predictions fit the observed data.

If we are in a setting where we have multiple rival models and insufficient data to discriminate between them (i.e. to discard inaccurate models), we need to design additional experiments $$\mathbf x$$ to collect more data. The goal is to find the experimental design $$\mathbf x^\ast$$ that yields the expected maximally informative observations for discriminating between the models. Simply put, we want to find the experiment for which the model predictions differ the most.

There are existing methods to try to solve the problem of design of experiments for model discrimination. Roughly, these can be dividied into analytic methods (computationally cheap, but limited to certain models) and data-driven methods (Monte Carlo-based, flexible but often computationally expensive). In the paper references above, and in this software package, the idea is to use an approach that hybridises analytic and data-driven methods, using analytic surrogate models learnt from sampled data.

## Installation
The GPdoemd package has been tested and validated on OSX and Ubuntu.  
No guarantees are provided that GPdoemd works on Windows-based systems.

##### Requirements
Python 3.4+
* numpy >= 1.7
* scipy >= 0.17
* [GPy](https://github.com/SheffieldML/GPy)

##### Optional
* gp_grief ([forked repository](https://github.com/scwolof/gp_grief)): for using GP-GRIEF models

##### Creating a virtual environment
We recommend installing GPdoemd in a virtual environment.  
To set up a new virtual environment called myenv (example name), run the command
```
python3 -m venv myenv
```
in the folder where you want to store the virtual environment.  
After the virtual environment has been created, activate it as follows
```
source myenv/bin/activate
```
It is recommended that you update the pip installation in the virtual environment
```
pip install --upgrade pip
```

##### Installing GPdoemd
First install all required packages in the virtual environment.  
The required packages are listed above and in the file [requirements.txt](https://github.com/cog-imperial/GPdoemd/blob/master/requirements.txt).  
```
pip install numpy scipy six paramz
pip install GPy
```
To install GPdoemd, run the following in the virtual environment
```
pip install git+https://github.com/cog-imperial/GPdoemd
```
It is also possible to clone into/download the GPdoemd git repository and install it using setup.py, but this is not recommended for most users.

##### Uninstalling GPdoemd
The GPdoemd package can be uninstalled by running
```
pip uninstall GPdoemd
```
Alternatively, the folder containing the virtual environment can be deleted.

## Authors
* **[Simon Olofsson](https://www.doc.ic.ac.uk/~so2015/)** ([scwolof](https://github.com/scwolof)) - Imperial College London

## License
The GPdoemd package is released under the MIT License. Please refer to the [LICENSE](https://github.com/cog-imperial/GPdoemd/blob/master/LICENSE) file for details.

## Acknowledgements
This work has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement no.675251.

