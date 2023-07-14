from flojoy import OrderedPair, flojoy, Matrix, Scalar
import numpy as np


import scipy.stats


@flojoy(node_type='default')
def SEM(
	default: OrderedPair | Matrix,
	axis: int = 0,
	ddof: int = 1,
	nan_policy: str = 'propagate',
	) -> OrderedPair | Matrix | Scalar:
	'''The SEM node is based on a numpy or scipy function.
	The description of that function is as follows:

		Compute standard error of the mean.
		
		Calculate the standard error of the mean (or standard error of
		measurement) of the values in the input array.
		
	Parameters
	----------
	a : array_like
		An array containing the values for which the standard error is
		returned.
	axis : int or None, optional
		Axis along which to operate. Default is 0. If None, compute over
		the whole array `a`.
	ddof : int, optional
		Delta degrees-of-freedom. How many degrees of freedom to adjust
		for bias in limited samples relative to the population estimate
		of variance. Defaults to 1.
	nan_policy : {'propagate', 'raise', 'omit'}, optional
		Defines how to handle when input contains nan.
	The following options are available (default is 'propagate'):
		
	* 'propagate': returns nan
	* 'raise': throws an error
	* 'omit': performs the calculations ignoring nan values

	Returns
	----------
	DataContainer:
		type 'ordered pair', 'scalar', or 'matrix'
	'''

	result = OrderedPair(
		m=scipy.stats.sem(
			a=default.y,
			axis=axis,
			ddof=ddof,
			nan_policy=nan_policy,
		))

	return result
