# Maintainer: harperic

##################################
## Find MPI

# This mostly work on Mac if the C/CXX compilers are set to be
# mpicc, mpicxx
find_package(MPI REQUIRED)

# manually set the libraries (for some reason these aren't correctly
# set with the CMake package
GET_FILENAME_COMPONENT(MPI_DIR ${MPI_C_COMPILER} DIRECTORY)
GET_FILENAME_COMPONENT(MPI_DIR ${MPI_DIR} DIRECTORY)
set(MPI_LIBRARY ${MPI_DIR}/lib)
set(MPI_C_LIBRARIES ${MPI_DIR}/lib)
set(MPI_CXX_LIBRARIES ${MPI_DIR}/lib)
set(MPI_C_INCLUDE_DIRS ${MPI_DIR}/include)
set(MPI_CXX_INCLUDE_DIRS ${MPI_DIR}/include)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DHAVE_MPI")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_MPI")

mark_as_advanced(MPI_EXTRA_LIBRARY MPI_LIBRARY CMAKE_C_FLAGS CMAKE_CXX_FLAGS)
