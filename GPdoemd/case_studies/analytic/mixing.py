"""
MIT License

Copyright (c) 2018 Simon Olofsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
from scipy.special import exp1

"""
Model super class
"""
class MicroMacroModel:
	@property
	def n_outputs (self):
		return 1
	@property
	def x_bounds (self):
		return np.array([[   1., 100.],	 # residence time
						 [ 0.01,   1.],	 # initial concentration
						 [   0.,   1.]]) # reactor type
	@property
	def p_bounds (self):
		return np.array([[ 1e-6, 1e-1]]) # reaction constant


"""
PFR reactor models
"""
def PFR_0 (x, p, grad=False):
	R  = p * x[0] / x[1]
	Rt = np.array( R < 1., dtype=float)
	C  = Rt * (1. - R)
	dC = Rt * -x[0]/x[1]
	return C if not grad else [C, dC[None,:]]

def PFR_1 (x, p, grad=False):
	R  = p * x[0]
	C  = np.exp(-R)
	dC = -x[0] * C
	return C if not grad else [C, dC[None,:]]

def PFR_2 (x, p, grad=False):
	R  = p * x[0] * x[1]
	C  = 1. / (1. + R)
	dC = -x[1] * x[0] * C**2
	return C if not grad else [C, dC[None,:]]

"""
CSTR reactor models
"""
def CSTR_0_macro (x, p, grad=False):
	R  = p * x[0] / x[1]
	C  = 1 - R + R * np.exp(-1./R)
	dC = x[0] / x[1] * ((1. + 1./R) * np.exp(-1./R) - 1.)
	return C if not grad else [C, dC[None,:]]

def CSTR_1 (x, p, grad=False):
	R  = p * x[0]
	C  = 1. / (1. + R)
	dC = -x[0] * C**2
	return C if not grad else [C, dC[None,:]]

def CSTR_2_micro (x, p, grad=False):
	R  = p * x[0] * x[1]
	C  = 1. / (2 * R) * ( np.sqrt(1 + 4*R) - 1 )
	dC = ( 1. / np.sqrt(1 + 4*R) - C ) / p
	return C if not grad else [C, dC[None,:]]

def CSTR_2_macro (x, p, grad=False):
	R  = p * x[0] * x[1]
	if R < 1.5e-3:
		# Risk of overflow
		C  = np.array([1.])
		dC = np.array([0.])
	else:
		C  = (1. / R) * np.exp(1. / R) * exp1(1. / R)
		dC = (1. - C*R - C)/(R*p)
	return C if not grad else [C, dC[None,:]]


"""
Models
"""
class M1 (MicroMacroModel):
	# Zero-order reaction, micro mixing
	@property
	def name (self):
		return 'M1'
	def __call__ (self, x, p, grad=False):
		return PFR_0(x, p, grad=grad)

class M2 (MicroMacroModel):
	# Zero-order reaction, macro mixing
	@property
	def name (self):
		return 'M2'
	def __call__ (self, x, p, grad=False):
		reactor = CSTR_0_macro if x[2] <= 0.5 else PFR_0
		return reactor(x, p, grad=grad)

class M3 (MicroMacroModel):
	# First-order reaction
	@property
	def name (self):
		return 'M3'
	def __call__ (self, x, p, grad=False):
		reactor = CSTR_1 if x[2] <= 0.5 else PFR_1
		return reactor(x, p, grad=grad)

class M4 (MicroMacroModel):
	# Second-order reaction, micro mixing
	@property
	def name (self):
		return 'M4'
	def __call__ (self, x, p, grad=False):
		reactor = CSTR_2_micro if x[2] <= 0.5 else PFR_2
		return reactor(x, p, grad=grad)

class M5 (MicroMacroModel):
	# Second-order reaction, macro mixing
	@property
	def name (self):
		return 'M5'
	def __call__ (self, x, p, grad=False):
		reactor = CSTR_2_macro if x[2] <= 0.5 else PFR_2
		return reactor(x, p, grad=grad)

"""
Data generator
"""
class DataGen (MicroMacroModel):
	def __init__ (self, i=2):
		self.truemodel = i

	@property
	def truemodel (self):
		return self._truemodel
	@truemodel.setter
	def truemodel (self, value):
		if not hasattr(self, '_truemodel'):
			assert isinstance(value, int) and 0 <= value <= 4
			self._truemodel = value
			
	@property
	def p (self):
		return [0.006, 0.006, 0.015, 0.025, 0.025][ self.truemodel ]
	@property
	def measvar (self):
		return np.array([0.05])**2
	@property
	def name (self):
		return 'M{:d}'.format( self.truemodel + 1 )

	def __call__ (self, x):
		model = [M1, M2, M3, M4, M5][self.truemodel]
		state = model()(x, self.p)
		noise = np.sqrt(self.measvar) * np.random.randn(self.n_outputs)
		return np.abs( state + noise )


"""
Get model functions
"""
def get (i=2):
	return DataGen(i), [M1(),M2(),M3(),M4(),M5()]








