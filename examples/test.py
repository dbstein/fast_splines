import numpy as np
import scipy as sp
import scipy.interpolate
import time
from fast_splines import interp2d

################################################################################
# Setup test

n = 1000
k = 5

v, h = np.linspace(0, 1, n, endpoint=True, retstep=True)
x, y = np.meshgrid(v, v, indexing='ij')

test_x = (x + np.random.rand(*x.shape)*h)[:-1,:-1]
test_y = (y + np.random.rand(*y.shape)*h)[:-1,:-1]

def test_function(x, y):
    return np.exp(x)*y + y**2/(0.2 + x)

f_grid = test_function(x, y)
truth = test_function(test_x, test_y)

################################################################################
# scipy

st = time.time()
interper = sp.interpolate.RectBivariateSpline(v, v, f_grid, kx=k, ky=k)
fitting_time = time.time() - st
st = time.time()
est = interper.ev(test_x, test_y)
eval_time = time.time() - st
err = np.abs(est - truth)

print('\n--- scipy ---')
print('   Fitting time:  {:0.2f}'.format(fitting_time*1000))
print('   Eval time:     {:0.2f}'.format(eval_time   *1000))
print('   Maximum error: {:0.2e}'.format(err.max()))

################################################################################
# fast_splines

st = time.time()
interpolater = interp2d(v, v, f_grid, k)
fitting_time = time.time()-st
est = interpolater(test_x, test_y)
err = np.abs(est - truth)

# run a second time so you don't catch numba compile time
st = time.time();
interpolater(test_x, test_y)
eval_time = time.time()-st

print('\n--- fast_splines ---')
print('   Fitting time:  {:0.2f}'.format(fitting_time*1000))
print('   Eval time:     {:0.2f}'.format(eval_time   *1000))
print('   Maximum error: {:0.2e}'.format(err.max()))


