#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

#include "new_python.h"

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
#include "S4_internal.h"
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

PySimulation::PySimulation()
    {
    // these are dummy/default values for the simulation
    Lr = new double[4];
    Lr[0] = 1;
    Lr[1] = 0;
    Lr[2] = 0;
    Lr[3] = 1;
    nG = 1;
    }

PySimulation::~PySimulation()
    {
    delete[] Lr;
    S4_Simulation_Destroy(S);
    }

void PySimulation::CreateNew()
    {
    S = S4_Simulation_New(Lr, nG, NULL);
    }

PySimulation::EPSData PySimulation::SetEPS(py::array_t<double> pyEPS)
    {
    S4_real eps[18];
    int type = 0;
    // time to play around with the arrays
    // ripping this straight from the website
    py::buffer_info info = pyEPS.request();
    // cast the data into a pointer to access later
    double *ptr = static_cast<double *>(info.ptr);
    // check array dimensions
    if (info.ndim == 1)
        {
        // check that we have a pair here
        if (info.shape[0] == 1)
            {
            // assume real only, and that's fine
            eps[0] = ptr[0];
            type = S4_MATERIAL_TYPE_SCALAR_COMPLEX;
            }
        else if (info.shape[0] == 2)
            {
            // handle the complex pair
            eps[0] = ptr[0];
            eps[1] = ptr[1];
            type = S4_MATERIAL_TYPE_SCALAR_COMPLEX;
            }
        else if (info.shape[0] == 9)
            {
            // this is a tensor in a flat form; accept anyway
            for (size_t t=0; t < 9; ++t)
                {
                eps[t] = ptr[t];
                }
            type = S4_MATERIAL_TYPE_XYTENSOR_COMPLEX;
            }
        else
            {
            // create a string stream object
            std::ostringstream s;
            // write the error, including the size of the array
            s << "Provided flat array of size " << info.shape[0]
              << " does not match accepted sizes: 1, 2, 9" << std::endl;
            // throw runtime error. For now everything will be a runtime error
            throw std::runtime_error(s.str());
            }
        }
    else if (info.ndim == 2)
        {
        // tensor; check that it is 3x3
        int nx = info.shape[0];
        int ny = info.shape[1];
        if ((nx != 3) || (ny != 3))
            {
            // create a string stream object
            std::ostringstream s;
            // write the error, including the size of the array
            s << "The tensor form of eps must be a 3 x 3 matrix;"
              << " provided matrix is: " << nx << " x " << ny << std::endl;
            // throw runtime error. For now everything will be a runtime error
            throw std::runtime_error(s.str());
            }
        for (size_t t=0; t < 9; ++t)
            {
            eps[t] = ptr[t];
            }
        // correctly format eps
        /* [ a b c ]    [ a b   ]
         * [ d e f ] -> [ d e   ]
         * [ g h i ]    [     i ]
         */
        eps[4] = eps[6]; eps[5] = eps[7];
        eps[6] = eps[8]; eps[7] = eps[9];
        eps[8] = eps[16]; eps[9] = eps[17];
        type = S4_MATERIAL_TYPE_XYTENSOR_COMPLEX;
        }
    else
        {
        // create a string stream object
        std::ostringstream s;
        // write the error, including the size of the array
        s << "The array provided is of dimensionality "
          << ". Only 1 or 2 dimensional arrays are accepted." << std::endl;
        // throw runtime error. For now everything will be a runtime error
        throw std::runtime_error(s.str());
        }
    // create the struct;
    struct PySimulation::EPSData sEPS;
    std::memcpy(sEPS.eps, eps, sizeof(double)*18);
    // sEPS.eps = eps;
    sEPS.type = type;
    return sEPS;
    }

void PySimulation::AddMaterial(std::string pyName, py::array_t<double> pyEPS)
    {
    // initialize variables
    S4_real eps[18];
    int type = 0;
    S4_MaterialID M;
    const char *name;

    // put pyName into the char
    name = pyName.c_str();
    // use shared code to interpret the EPS
    struct PySimulation::EPSData sEPS = SetEPS(pyEPS);
    std::memcpy(eps, sEPS.eps, sizeof(double)*18);
    type = sEPS.type;
    // set the material
    M = S4_Simulation_SetMaterial(S, -1, name, type, eps);
    if(M < 0)
        {
        // create a string stream object
        std::ostringstream s;
        // write the error, including the size of the array
        s << "AddMaterial: there was a problem allocation the material named "
          << name << std::endl;
        // throw runtime error. For now everything will be a runtime error
        throw std::runtime_error(s.str());
        }
    }

void PySimulation::SetMaterial(std::string pyName, py::array_t<double> pyEPS)
    {
    // currently this needs to have CreateNew called first
    // TODO add in a check to make sure that a simulation exists
    // Do whatever I need to "wrap" the thing

    // initialize variables
    S4_real eps[18];
    int type = 0;
    S4_MaterialID M;
    const char *name;

    // put pyName into the char
    name = pyName.c_str();
    // get the material index; this will return a -1 if it's not yet defined
    // and thus operate like the add code
    // you know, I could probably just run this as if it were the add code...ugh
    M = S4_Simulation_GetMaterialByName(S, name);
    // use shared code to interpret the EPS
    struct PySimulation::EPSData sEPS = SetEPS(pyEPS);
    std::memcpy(eps, sEPS.eps, sizeof(double)*18);
    type = sEPS.type;
    // set the material
    M = S4_Simulation_SetMaterial(S, M, name, type, eps);
    if(M < 0)
        {
        std::ostringstream s;
        // write the error, including the size of the array
        s << "SetMaterial: there was a problem allocation the material named "
          << name << std::endl;
        // throw runtime error. For now everything will be a runtime error
        throw std::runtime_error(s.str());
        }
    }

// not yet implemented
// void PySimulation::SetLattice(double pyLattice)
    // {
    // specifically handles the single value instance (1D lattice)
    // }

void PySimulation::SetLattice(py::array_t<double> pyLattice)
    {
    // set the lattice basis vectors

    // get the information about the incoming numpy array
    py::buffer_info info = pyLattice.request();
    double *ptr = static_cast<double *>(info.ptr);
    if (info.ndim != 2)
        {
        std:: ostringstream s;
        s << "lattice constant must be a 2-dimensional (2 x 2) array";
        throw std::runtime_error(s.str());
        }
    int nx = info.shape[0];
    int ny = info.shape[1];
    if ((nx != 2) || (ny != 2))
        {
        std:: ostringstream s;
        s << "The tensor form of eps must be a 2 x 2 matrix;"
          << " provided matrix is: " << nx << " x " << ny << std::endl;
        throw std::runtime_error(s.str());
        }
    // Create array to pass into S4
    S4_real Lr[4];
    for (size_t i = 0; i < 4; ++i)
        {
        Lr[i] = ptr[i];
        }
    int setLatticeReturn = S4_Simulation_SetLattice(S, Lr);
    if(0 != setLatticeReturn)
        {
        std::ostringstream s;
        switch(setLatticeReturn)
            {
            case 1: /* degenerate */
                s << "SetLattice: Lattice vectors are degenerate (for 1D lattice, set second vector to zero).";
            case 2: /* both zero */
                s << "SetLattice: Lattice vectors are both zero.";
            default:
                s << "Some other error occured while setting Lattice vectors. Aborting.";
            }
        throw std::runtime_error(s.str());
        }
    }

void PySimulation::SetNumG(int n)
    {
    if (n < 1)
        {
        std::ostringstream s;
        s << "n must be >= 1";
            throw std::runtime_error(s.str());
        }
    Simulation_SetNumG(S, n);
    }

int PySimulation::GetNumG()
    {
    int n = Simulation_GetNumG(S, NULL);
    return n;
    }

void PySimulation::AddLayer(std::string pyName, double pyThickness, std::string pyBackground)
    {
    S4_LayerID layer;
    const char* name;
    S4_real thickness = pyThickness;
    const char* matname;
    // set the name to the pyName;
    name = pyName.c_str();
    matname = pyBackground.c_str();
    // get the material by name
    S4_MaterialID M = S4_Simulation_GetMaterialByName(S, matname);
    if (M < 0)
        {
        std::ostringstream s;
        s << "AddLayer: Unknown material " << matname;
        throw std::runtime_error(s.str());
        }
    layer = S4_Simulation_SetLayer(S, -1, name, &thickness, -1, M);
    if (layer < 0)
        {
        std::ostringstream s;
        s << "AddLayer: There was a problem allocating the layer named " << name;
        throw std::runtime_error(s.str());
        }
    }

void PySimulation::SetLayer(std::string pyName, double pyThickness, std::string pyBackground)
    {
    S4_LayerID layer;
    const char* name;
    S4_real thickness = pyThickness;
    const char* matname;
    // set the name to the pyName;
    name = pyName.c_str();
    // attempt to access the layer by name
    layer = S4_Simulation_GetLayerByName(S, name);
    // handle if no layer is found
    if (layer < 0)
        {
        // use/search with material name
        matname = pyBackground.c_str();
        S4_MaterialID M = S4_Simulation_GetMaterialByName(S, matname);
        // handle is material not found
        if (M < 0)
            {
            std::ostringstream s;
            s << "SetLayer: Unknown material " << matname;
            throw std::runtime_error(s.str());
            }
        layer = S4_Simulation_SetLayer(S, -1, name, &thickness, -1, M);
        if (layer < 0)
            {
            std::ostringstream s;
            s << "SetLayer: There was a problem allocating the layer named " << name;
            throw std::runtime_error(s.str());
            }
        else
            {
            S4_Simulation_SetLayer(S, layer, NULL, &thickness, -1, -1);
            }
        }
    }

void PySimulation::SetLayerThickness(std::string pyName, double pyThickness)
    {
    S4_LayerID layer;
    const char* name;
    S4_real thickness = pyThickness;
    // set the name to the pyName;
    name = pyName.c_str();
    // attempt to access the layer by name
    layer = S4_Simulation_GetLayerByName(S, name);
    // handle if no layer is found
    if (layer < 0)
        {
        std::ostringstream s;
        s << "SetLayerThickness: Layer named " << name << " not found";
        throw std::runtime_error(s.str());
        }
    else
        {
        if (thickness < 0)
            {
            std::ostringstream s;
            s << "SetLayerThickness: Thickness must be non-negative";
            throw std::runtime_error(s.str());
            }
        S4_Simulation_SetLayer(S, layer, NULL, &thickness, -1, -1);
        }
    }

void PySimulation::SetLayerPatternCircle(std::string pyName, std::string pyMaterial, py::array_t<double> pyCenter, double pyRadius)
    {
    const char *layer_name = pyName.c_str();
    const char *material_name = pyMaterial.c_str();
    double radius = pyRadius;
    double center[2];
    S4_LayerID layer;
    S4_MaterialID M;
    //handle the array
    py::buffer_info info = pyCenter.request();
    // check that the center is appropriately formatted
    if (info.ndim != 1)
        {
        std::ostringstream s;
        s << "Center must be a 1D array with 2 elements: [x, y]";
        throw std::runtime_error(s.str());
        }
    else if (info.shape[0] != 2)
        {
        std::ostringstream s;
        s << "Center must be a 1D array with 2 elements: [x, y]";
        throw std::runtime_error(s.str());
        }
    double *ptr = static_cast<double *>(info.ptr);

    layer = S4_Simulation_GetLayerByName(S, layer_name);
    // can't find layer
    if (layer < 0)
        {
        std::ostringstream s;
        s << "SetLayerPatternCircle: Layer " << layer_name << " not found";
        throw std::runtime_error(s.str());
        }
    if (S4_Layer_IsCopy(S, layer) > 0)
        {
        std::ostringstream s;
        s << "SetLayerPatternCircle: Cannot pattern a layer copy.";
        throw std::runtime_error(s.str());
        }
    M = S4_Simulation_GetMaterialByName(S, material_name);
    if (M < 0)
        {
        std::ostringstream s;
        s << "SetLayerPatternCircle: Material named " << material_name << " not found";
        throw std::runtime_error(s.str());
        }
    // I think we'll yolo this
    center[0] = ptr[0];
    center[1] = ptr[1];
    S4_real hw[2];
    hw[0] = radius;
    hw[1] = radius;
    int ret = S4_Layer_SetRegionHalfwidths(S, layer, M, S4_REGION_TYPE_ELLIPSE, hw, center, NULL);
    if (ret != 0)
        {
        std::ostringstream s;
        s << "SetLayerPatternCircle: There was a problem allocating the pattern.";
        throw std::runtime_error(s.str());
        }
    }

PYBIND11_MODULE(_S4, m)
    {
    m.doc() = "C++ wrapper for S4 RCWA Code. Care should be taken directly interacting with \
this module. End-users should use the python wrapper instead.";
    py::class_<PySimulation>(m, "S4_Simulation")
        .def(py::init<>())
        .def("_CreateNew", &PySimulation::CreateNew)
        .def("_AddMaterial", &PySimulation::AddMaterial)
        .def("_SetMaterial", &PySimulation::SetMaterial)
        .def("_SetLattice", &PySimulation::SetLattice)
        .def("_SetNumG", &PySimulation::SetNumG)
        .def("_GetNumG", &PySimulation::GetNumG)
        .def("_AddLayer", &PySimulation::AddLayer)
        .def("_SetLayer", &PySimulation::SetLayer)
        .def("_SetLayerThickness", &PySimulation::SetLayerThickness)
        .def("_SetLayerPatternCircle", &PySimulation::SetLayerPatternCircle)
        // .def("Clone", &S4_Simulation_Clone)
        // .def("New", &S4_Simulation_New)
        ;
    // py::class_<Interpolator>(m, "Interpolator");

    // py::class_<data_point>(m, "data_point")
        // .def_readwrite("x", &data_point::x)
        // .def_readwrite("y", &data_point::y)
        // ;
    }
