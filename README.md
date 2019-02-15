# fast_splines: numba accelerated spline evaluation on regular grids (in 1 and 2D)

This code provides a drop-in replacement for the scipy function RectBivariateSpline. Only the code for the evaluation stage is changed, the fitting part is still done using the scipy wrapping of the [dierckx](http://www.netlib.org/dierckx/) package. The knots and coefficients are then extracted, and passed into a numba accelerated port of the relevant functions from dierckx for evaluation. Usage is virtually the same as RectBivariateSpline:

```python
from fast_splines import interp2d

interpolater = interp2d(xv, yv, f, k)
out = interper(xo, yo)
```

Only constant extrapolation and odd valued k=1,3,5 are supported.

## Performance

On my machine with 12 cores, this function varies between being about the same speed as the scipy function (for small evaluations), to being up to 100x faster (for large evaluations).

While there are other numba based interpolation routines out there (e.g. [this one](https://github.com/EconForge/interpolation.py)), they are not accurate to the domain boundaries for k > 1. For bilinear interpolation, the fitting routine in that package is *much* faster. Times (in milliseconds) for evaluation of a cubic spline are shown below; they are compute from an n by n grid to n^2 evaluation points, on a 12 core machine with two Intel(R) Xeon(R) CPU E5-2643 v3 @ 3.40GHz processors and 128gb of RAM. 

| n    | scipy time | fast_splines | interpolation |
|------|------------|--------------|---------------|
| 50   | 0.91       | 0.35         | 0.40          |
| 500  | 160        | 7.1          | 9.6           |
| 5000 | 104665     | 455          | 1039          |

For the largest array, fast_splines performs the evaluation 230 times faster! I'll note that the errors are exactly the same for the scipy/fast_splines versions: e.g. for n=50, the maximum error for both is 2.87e-8, while for the interpolation package the max error is 4.66e-5. The error is similar in the interior, but almost three orders of magnitude larger near domain edges!

## To do:

1. Someday, it would be good to rewrite the fitting routines to get better performance; an alternate option is to use a multiprocessing solution that decomposes the rectangular domain. We shall see.
2. For bilinear interpolation, I should default to using the interpolation packages fitting routine if its installed, since that's much faster.
3. For speed on uniform grids, I've put in a faster way of locating the appropriate cell (this is what restricts me to odd k, also). I could remove that (or flag it), to allow even k and evaluation on non-uniform grids. I tend not to use these, so it hasn't been a priority, but would be nice.

