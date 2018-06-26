#include <pybind11/pybind11.h>

namespace py = pybind11;

#ifdef HAVE_MPI
#include <mpi.h>
#endif

#include <stdio.h>
#include <string.h>
#include <stdarg.h>

// #ifdef WIN32
// #define _USE_MATH_DEFINES
// #endif

#include <math.h>
#include <stdlib.h>
#include "S4.h"
#include "convert.h"
// #include "test_func.h"
#include "SpectrumSampler.h"
#include "cubature.h"
#include "Interpolator.h"
#include "rcwa.h"
// #include "fmm/fft_iface.h"
// #include "kiss_fft/kiss_fft.h"
// #include "kiss_fft/tools/kiss_fftnd.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#ifndef Bool
#define Bool unsigned char
#endif

PYBIND11_MODULE(S4, m)
    {
    m.doc() = "S4 Lorem Ipsum";
    py::class_<S4_Simulation>(m, "S4_Simulation");
    py::class_<Interpolator>(m, "Interpolator");
    py::class_<SpectrumSampler>(m, "SpectrumSampler");
    py::class_<S4Interpolator_Data>(m, "S4Interpolator_Data");
    py::class_<S4Excitation_Data>(m, "S4Excitation_Data");
    py::class_<S4SpectrumSampler_Data>(m, "S4SpectrumSampler_Data");

    // py::class_<data_point>(m, "data_point")
        // .def_readwrite("x", &data_point::x)
        // .def_readwrite("y", &data_point::y)
        // ;
    // py::class_<SpectrumSampler_>(m, "SpectrumSampler_");
    // py::class_<SpectrumSampler>(m, "SpectrumSampler");
    // m.def("Interpolator_New", &Interpolator_New);
    // that one works
    // m.def("adapt_integrate", &adapt_integrate);
    m.def("GetLayerZIntegral", &GetLayerZIntegral);
    m.def("SolveLayerEigensystem", &SolveLayerEigensystem);

    // m.def("fft_next_fast_size", &fft_next_fast_size);

    // m.def("kiss_fftnd", &kiss_fftnd);
    // m.def("SpectrumSampler_New", &SpectrumSampler_New);
    // m.def("convert_units", &convert_units);
    // m.def("new_function", &new_function);
    // m.def("test_function", &test_function);
    }
