CMAKE_MINIMUM_REQUIRED(VERSION 2.6.2 FATAL_ERROR)

if (CMAKE_MAJOR_VERSION VERSION_GREATER 2)
if(COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)
    cmake_policy(SET CMP0026 OLD)
    cmake_policy(SET CMP0042 OLD)
endif(COMMAND cmake_policy)
endif()

project (S4)

add_subdirectory(CMake)

# Find Lua (may eventually be removed due to not using lua)
include(FindLua)
include_directories(${LUA_INCLUDES})
# Find FFTW
include(FindFFTW)
include_directories(${FFTW3_INC})
# Find Accelerators
include(FindAccelerators)
include_directories(${vecLib_INCLUDES})

# set(BLAS_LIBRARIES "-framework Accelerate")
# mark_as_advanced(BLAS_LIBRARIES)
# set(LAPACK_LIBRARIES -framework Accelerate)
# mark_as_advanced(LAPACK_LIBRARIES LAPACK_INCLUDES)

include(S4CFlagsSetup)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -Wall -msse3 -msse2 -msse")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -Wall -msse3 -msse2 -msse")

# setup python
include(S4PythonSetup)
include_directories(${PYTHON_INCLUDE_DIR})

# I should eventually add pybind11 as a submodule
find_package(pybind11)

# setup numpy
include (S4NumpySetup)
include_directories(${NUMPY_INCLUDE_DIR})

# macros
include (S4Macros)
# mpi
include(S4MPISetup)
include_directories(${MPI_CXX_INCLUDE_DIRS})
link_directories(${MPI_CXX_LIBRARIES})

# Keep around for eventually adding in pybind as a submodule
# include external source projects
# include_directories(${CMAKE_CURRENT_SOURCE_DIR}/extern)

# set (UPDATE_SUBMODULES 1 CACHE BOOL "Update git submodules for dependency projects")

# if (UPDATE_SUBMODULES)
  # message(STATUS "Updating git submodules")
  # execute_process(COMMAND git submodule update --init
                  # WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
# else (UPDATE_SUBMODULES)
  # message(STATUS "Not updating git submodules")
# endif (UPDATE_SUBMODULES)

# set the default install prefix
IF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    SET(CMAKE_INSTALL_PREFIX ${PYTHON_USER_SITE} CACHE PATH "Python site installation directory (defaults to USER_SITE)" FORCE)
ENDIF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)

# Fixup conda linking, if this python appears to be a conda python
if (${CMAKE_MAJOR_VERSION} GREATER 2)
  get_filename_component(_python_bin_dir ${PYTHON_EXECUTABLE} DIRECTORY)
  if (EXISTS "${_python_bin_dir}/conda")
      message("-- Detected conda python, activating workaround")
      set(_using_conda On)
  else()
      set(_using_conda Off)
  endif()
endif()

add_subdirectory(cpp)
# add_subdirectory(doc)
