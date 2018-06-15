Download & Installation
=======================

GitHub repository
-----------------

The source code is located at this `GitHub repository <https://github.com/harperic/S4>`_.
You can clone it with the command::

	git clone https://github.com/harperic/S4.git

Compiling from source
---------------------

Dependencies
^^^^^^^^^^^^

Before compiling, there are a number of packages that are recommended.
None of these is required except for either Lua or Python.

* `Lua <http://www.lua.org>`_ 5.2.x - This is required for the Lua frontend.
  Either this or Python is required.
  On Ubuntu or Debian, the repository packages are called ``liblua5.2``
  and ``liblua5.2-dev``.
* `Python <http://python.org>`_ 2.x or 3.x - This is required to build |S4| as a Python extension.
  Either this or Lua is required.
  On Ubuntu or Debian, the repository package is called ``python-dev`` or ``python3-dev``.
* BLAS and Lapack implementation - Optional, but highly recommended. It is suggested that `OpenBLAS <http://www.openblas.net/>`_ be used.
* `FFTW3 <http://fftw.org>`_ - Optional, provides a 2-3x speedup in FFT computations.
  On Ubuntu or Debian, the repository package is called ``libfftw3-dev``.
  On Ubuntu or Debian, install the repository package is called ``libsuitesparse-dev``.
* POSIX Threads - Optional, typically provided by the compiler. Allows multi-threading support on shared-memory machines.
* MPI - Optional, provides support for parallel computing on distributed-memory machines.

Compilation
^^^^^^^^^^^^^^^^^^^^^^^^
# The previous Makefiles have been replaced with CMake to hopefully make compilation easier

# Currently this version has only been developed for macOS with packages provided by macports
  (NEED LINK) and/or anaconda (NEED LINK).

# To begin installation, run the command::

  ccmake ~/code/S4 -DLUA_INCLUDES=/opt/local/include -DFFTW_INCLUDES=/opt/local/include -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx

# Once ccmake is complete and the parameters have been adjusted to your liking, make the project::

  make -j4

Adjust `j4` as n+2 where n is the number of cores on your machine (please do not abuse login nodes on HPC)

# Currently the include directories for Lua and FFTW need to be passed into the compiler, as do the correct mpi-enabled compilers

# The resulting Lua binary is called ``luaS4``. The Python shared

.. |S4| replace:: S\ :sup:`4`
