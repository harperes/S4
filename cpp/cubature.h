/* Adaptive multidimensional integration of a vector of integrands.
 *
 * Copyright (c) 2005-2009 Steven G. Johnson
 *
 * Portions (see comments) based on HIntLib (also distributed under
 * the GNU GPL, v2 or later), copyright (c) 2002-2005 Rudolf Schuerer.
 *     (http://www.cosy.sbg.ac.at/~rschuer/hintlib/)
 *
 * Portions (see comments) based on GNU GSL (also distributed under
 * the GNU GPL, v2 or later), copyright (c) 1996-2000 Brian Gough.
 *     (http://www.gnu.org/software/gsl/)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */
#include <pybind11/pybind11.h>

#ifndef CUBATURE_H
#define CUBATURE_H

#ifdef __cplusplus
extern "C"
{
#endif /* __cplusplus */

/* USAGE: Call adapt_integrate with your function as described below.

	  To compile a test program, compile cubature.c with
	  -DTEST_INTEGRATOR as described at the end. */

/* a vector integrand - evaluates the function at the given point x
   (an array of length ndim) and returns the result in fval (an array
   of length fdim).   The void* parameter is there in case you have
   to pass any additional data through to your function (it corresponds
   to the fdata parameter you pass to adapt_integrate). */
typedef void (*integrand) (unsigned ndim, const double *x, void *,
			   unsigned fdim, double *fval);

/* a vector integrand of a vector of npt points: x[i*ndim + j] is the
   j-th coordinate of the i-th point, and the k-th function evaluation
   for the i-th point is returned in fval[k*npt + i]. */
typedef void (*integrand_v) (unsigned ndim, unsigned npt,
			     const double *x, void *,
			     unsigned fdim, double *fval);

typedef struct {
    double val, err;
    } esterr;

static double relError(esterr ee);
static double errMax(unsigned fdim, const esterr *ee);

typedef struct {
    unsigned dim;
    double *data;	/* length 2*dim = center followed by half-widths */
    double vol;	/* cache volume = product of widths */
    } hypercube;

static double compute_vol(const hypercube *h);
static hypercube make_hypercube(unsigned dim, const double *center, const double *halfwidth);
static hypercube make_hypercube_range(unsigned dim, const double *xmin, const double *xmax);
static void destroy_hypercube(hypercube *h);

typedef struct {
    hypercube h;
    unsigned splitDim;
    unsigned fdim; /* dimensionality of vector integrand */
    esterr *ee; /* array of length fdim */
    double errmax; /* max ee[k].err */
    } region;

static region make_region(const hypercube *h, unsigned fdim);
static void destroy_region(region *R);
static int cut_region(region *R, region *R2);

typedef int (*evalError_func)(struct rule_s *r,
    unsigned fdim, integrand_v f, void *fdata,
    unsigned nR, region *R);
typedef void (*destroy_func)(struct rule_s *r);

typedef struct rule_s {
    unsigned dim, fdim;         /* the dimensionality & number of functions */
    unsigned num_points;       /* number of evaluation points */
    unsigned num_regions; /* max number of regions evaluated at once */
    double *pts; /* points to eval: num_regions * num_points * dim */
    double *vals; /* num_regions * num_points * fdim */
    evalError_func evalError;
    destroy_func destroy;
    } rule;

static void destroy_rule(rule *r);
static int alloc_rule_pts(rule *r, unsigned num_regions);
static rule *make_rule(size_t sz, /* >= sizeof(rule) */
    unsigned dim, unsigned fdim, unsigned num_points,
    evalError_func evalError, destroy_func destroy);
static int eval_regions(unsigned nR, region *R,
    integrand_v f, void *fdata, rule *r);
static unsigned ls0(unsigned n);
static void evalR_Rfs(double *pts, unsigned dim, double *p, const double *c, const double *r);
static void evalRR0_0fs(double *pts, unsigned dim, double *p, const double *c, const double *r);
static void evalR0_0fs4d(double *pts, unsigned dim, double *p, const double *c,
    const double *r1, const double *r2);

typedef struct {
    rule parent;

    /* temporary arrays of length dim */
    double *widthLambda, *widthLambda2, *p;

    /* dimension-dependent constants */
    double weight1, weight3, weight5;
    double weightE1, weightE3;
    } rule75genzmalik;

static int isqr(int x);
static void destroy_rule75genzmalik(rule *r_);
static int rule75genzmalik_evalError(rule *r_, unsigned fdim, integrand_v f, void *fdata, unsigned nR, region *R);
static rule *make_rule75genzmalik(unsigned dim, unsigned fdim);
static int rule15gauss_evalError(rule *r,
    unsigned fdim, integrand_v f, void *fdata,
    unsigned nR, region *R);
static rule *make_rule15gauss(unsigned dim, unsigned fdim);

typedef region heap_item;
typedef struct {
    unsigned n, nalloc;
    heap_item *items;
    unsigned fdim;
    esterr *ee; /* array of length fdim of the total integrand & error */
    } heap;

static void heap_resize(heap *h, unsigned nalloc);
static heap heap_alloc(unsigned nalloc, unsigned fdim);
static void heap_free(heap *h);
static int heap_push(heap *h, heap_item hi);
static int heap_push_many(heap *h, unsigned ni, heap_item *hi);
static heap_item heap_pop(heap *h);
static int ruleadapt_integrate(rule *r, unsigned fdim, integrand_v f, void *fdata, const hypercube *h, unsigned maxEval, double reqAbsError, double reqRelError, double *val, double *err, int parallel);
static int integrate(unsigned fdim, integrand_v f, void *fdata,
    unsigned dim, const double *xmin, const double *xmax,
    unsigned maxEval, double reqAbsError, double reqRelError,
    double *val, double *err, int parallel);
int adapt_integrate_v(unsigned fdim, integrand_v f, void *fdata,
    unsigned dim, const double *xmin, const double *xmax,
    unsigned maxEval, double reqAbsError, double reqRelError,
    double *val, double *err);

typedef struct fv_data_s
    {
    integrand f;
    void *fdata;
    double *fval1;
    } fv_data;

static void fv(unsigned ndim, unsigned npt,
    const double *x, void *d_,
    unsigned fdim, double *fval);

/* Integrate the function f from xmin[dim] to xmax[dim], with at most
   maxEval function evaluations (0 for no limit), until the given
   absolute or relative error is achieved.  val returns the integral,
   and err returns the estimate for the absolute error in val; both
   of these are arrays of length fdim, the dimension of the vector
   integrand f(x). The return value of the function is 0 on success
   and non-zero if there  was an error. */
int adapt_integrate(unsigned fdim, integrand f, void *fdata,
		    unsigned dim, const double *xmin, const double *xmax,
		    unsigned maxEval, double reqAbsError, double reqRelError,
		    double *val, double *err);

/* as adapt_integrate, but vectorized integrand */
int adapt_integrate_v(unsigned fdim, integrand_v f, void *fdata,
		      unsigned dim, const double *xmin, const double *xmax,
		     unsigned maxEval, double reqAbsError, double reqRelError,
		      double *val, double *err);

#ifdef __cplusplus
}  /* extern "C" */
#endif /* __cplusplus */

#endif /* CUBATURE_H */
