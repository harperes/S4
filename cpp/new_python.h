#ifndef NEW_PYTHON_H
#define NEW_PYTHON_H

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

// this is the python wrapper class for the simulation
// will properly initialize and expose relevant methods, etc.
// will also avoid horrifying spaghetti code
class PySimulation
    {
    public:
    PySimulation();
    ~PySimulation();
    // I dont' know what I should call this...
    void CreateNew();
    struct EPSData
        {
        S4_real eps[18];
        int type;
        };
    // these need the proper arguments included
    /* void AddMaterial(); */
    EPSData SetEPS(py::array_t<double> pyEPS);
    void AddMaterial(std::string pyName, py::array_t<double> pyEPS);
    void SetMaterial(std::string pyName, py::array_t<double> pyEPS);
    void SetLattice(py::array_t<double> pyLattice);
    void SetNumG(int n);
    int GetNumG();
    void AddLayer(std::string pyName, double pyThickness, std::string pyBackground);
    void SetLayer(std::string pyName, double pyThickness, std::string pyBackground);
    void SetLayerThickness(std::string pyName, double pyThickness);
    void SetLayerPatternCircle(std::string pyName, std::string pyMaterial, py::array_t<double> pyCenter, double pyRadius);

    private:
    S4_Simulation* S;
    double *Lr;//[4];
    unsigned int nG;
    /* static char *kwlist[] = {"Lattice", "NumBasis", NULL}; */
    };

#endif
