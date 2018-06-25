/* Copyright (C) 2009-2011, Stanford University
 * This file is part of S4
 * Written by Victor Liu (vkl@stanford.edu)
 *
 * S4 is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * S4 is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
#include <pybind11/pybind11.h>

#ifndef _SPECTRUM_SAMPLER_H_
#define _SPECTRUM_SAMPLER_H_

// SpectrumSampler_Options is defined with an alias type
typedef struct SpectrumSampler_Options_{
    int initial_num_points;
    double range_threshold;
    double max_bend;
    double min_dx;
    int parallelize;
    } SpectrumSampler_Options;

// data_point is defined with an alias type
typedef struct data_point_{
    double x, y;
    struct data_point_ *prev, *next;
    } data_point;


// SpectrumSampler_ is the alias...?
typedef struct SpectrumSampler_{
    data_point *value;
    union{
        data_point *active;
        struct{
            data_point **active;
            int n_active;
            int n_alloc;
            double *buf;
            } active_list;
        } active_set;
    int done;
    int state;
    double x0, x1;
    double y_max, y_min;
    SpectrumSampler_Options options;
    } *SpectrumSampler;
// this defines SpectrumSampler as a pointer to SpectrumSampler_ (the alias...??)
/* typedef struct SpectrumSampler_* SpectrumSampler; */

SpectrumSampler SpectrumSampler_New(double x0, double x1, const SpectrumSampler_Options *options);
void SpectrumSampler_Destroy(SpectrumSampler sampler);
int SpectrumSampler_IsDone(const SpectrumSampler sampler);
int SpectrumSampler_IsParallelized(const SpectrumSampler sampler);
double SpectrumSampler_GetFrequency(const SpectrumSampler sampler);
int SpectrumSampler_SubmitResult(SpectrumSampler sampler, double y);
int SpectrumSampler_GetNumPoints(const SpectrumSampler sampler);

/* returns number of freqs */
int SpectrumSampler_GetFrequencies(const SpectrumSampler sampler, const double **freqs);
int SpectrumSampler_GetSubmissionBuffer(const SpectrumSampler sampler, double **y);
int SpectrumSampler_SubmitResults(SpectrumSampler sampler);

typedef void* SpectrumSampler_Enumerator;
SpectrumSampler_Enumerator SpectrumSampler_GetPointEnumerator(const SpectrumSampler sampler);
int SpectrumSampler_Enumerator_Get(SpectrumSampler_Enumerator, double pt[2]);

#endif /* _SPECTRUM_SAMPLER_H_ */
