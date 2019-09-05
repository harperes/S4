Installation Guide for S4
=========================

**It is recommended that you use the admin-compiled versions of our
software on Thanos and Ultron. Please follow these instructions to
install and use S4.**

This guide covers the installation of the S4 software. This guide
currently (<2019-08-05 Thu>) only covers installation on Ubuntu Linux;
this software *should* be able to be installed on any Unix/Linux
machine, but the exact packages and steps will be OS dependent.

Summary
--------

#. Install prerequisites from package managers
#. Setup environment files
#. Compile and setup prerequisites from github
#. Compile S4
#. Install MANTIS/SIGNAC

Conventions used in this guide
------------------------------

This guide suggests/assumes some basic familiarity with linux, git, and
compiling your own software.

We suggest creating a ``code`` directory specifically for storing
different git repositories. We recommended creating this directory in
your home directory:

.. code:: bash

   $: mkdir ~/code

After cloning a number of repositories, your code directory will look a
little like this

.. code:: bash

   ~/code
      |
      |---pybind11/
      |---OpenBLAS/
      |---S4/

We also suggest creating a ``build`` directory in a different location
to keep the files generated during compilation and installation
separated from the source code/git repositories. We recommend creating
this directory in your home directory:

.. code:: bash

   $: mkdir ~/build

After compiling a number of projects, your build directory will look a
little like this

.. code:: bash

   ~/build
      |
      |---pybind11/
      |---OpenBLAS/
      |---S4/

Together, it will look like

.. code:: bash

   ~/
    |
    |---code/
    |     |
    |     |---pybind11/
    |     |---OpenBLAS
    |     |---S4/
    |
    |---build/
    |     |
    |     |---pybind11/
    |     |---OpenBLAS/
    |     |---S4/

Then, when compiling a package, you will issue a command similar to:

.. code:: bash

   $: S4_CODE=~/code/S4
   $: S4_BUILD=~/build/S4
   $: cd ${S4_BUILD}
   $: ccmake ${S4_CODE} <args>

Installing Prerequisites
------------------------

The following software is required to compile and run S4. If you are
compiling your own software, you *should* be familiar enough with Linux
to find the correct packages/versions, but refer to the list below for
common packages. Note that because Ubuntu is *downstream* of Debian, a
notoriously stable distro (read: lagging behind w/r/t current packages),
these packages **will not** be as up-to-date as those found *via* conda.

Ubuntu ``apt`` packages
~~~~~~~~~~~~~~~~~~~~~~~

-  ``cmake`` required to use the cmake build system, used for S4
-  ``cmake-curses-gui`` required to use the cmake cache
-  ``ninja-build`` alternate to make
-  ``gfortran`` needed for OpenBLAS to compile
-  ``libfftw3-dev`` required for the fast fourier transforms
-  ``libopenmpi-dev`` required for mpi-based parallelism
-  ``python3-dev``
-  ``python3-numpy``
-  ``python-dev``
-  ``python-numpy``
-  ``python3-mpi4py``
-  ``python3-pip``
-  ``python3-pytest``

The python packages not be strictly necessary, but due to potential
conflict between the system and conda pythons, have been found to make
installation easier/work

conda packages
~~~~~~~~~~~~~~

Install the following conda packages.

**Note:** If you create a new environment to install these packages
(``$: conda create -n ENV_NAME ...``), you will need to activate that
environment (``$: conda activate ENV_NAME``) before compiling or using
S4.

Make sure to enable conda forge:

.. code:: bash

   $: conda config --add channels conda-forge

#. *Required* packages

   -  ``pytest``
   -  ``h5py``
   -  ``pytables``
   -  ``mpi4py blas=1.1=openblas``
   -  ``pandas``

#. *Recommended* packages

   -  ``tensorflow-gpu``
   -  ``keras-gpu``
   -  ``ipython``
   -  ``jupyter``
   -  ``matplotlib``
   -  ``seaborn``

#. ``yml`` installation

   For your convenience, a yml file is provided for one-command
   installation:

   .. code:: bash

      $: S4_CODE=~/code/S4
      $: conda env create -f s4py.yml

Environment Setup
-----------------

We will be opening and editing files using super-user privileges during
this step. You will need to use an appropriate text editor to do this. A
few examples of how you may do so are included below:

.. code:: bash

   $: sudo vim <file>
   $: sudo emacs <file>
   $: sudo gedit <file>

**NOTE:** you can also open a file with sudo privileges in emacs *via* `C-x C-f /sudo::`

Each step will include a file name, and below the text that needs to be
added to the file. For example:

Open and edit an example file (``/pth/to/file.txt``)

.. code:: bash

   This text must be added to the file for this step to be complete

**NOTE**: The steps below are the proper way to do this on **UBUNTU**.
Please research the way to do this on other OS's e.g. macOS, Fedora,
etc.

**NOTE:** You do not *have* to install to ``/opt``, but this is where we
recommended installing this compiled software, as well as where it is
installed on Thanos, Ultron, etc.

#. Open and edit a file for OpenBLAS
   (``/etc/ld.so.conf.d/OpenBLAS.conf``)

   **NOTE:** You will need to use ``sudo``

   .. code:: bash

      /opt/OpenBLAS/lib

#. Open and edit a file for S4 (``/etc/ld.so.conf.d/S4.conf``)

   **NOTE:** You will need to use ``sudo``

   .. code:: bash

      /opt/S4

#. (Re)-configure the files

   .. code:: bash

      $: sudo ldconfig

#. Open and edit ``/etc/environment``

   **NOTE:** You will need to use ``sudo``

   **NOTE:** It is recommended to copy the previous path and comment
   (add a ``#`` to the beginning of the line) before making these
   changes.

   Add the following to the beginning of your path.

   .. code:: bash

      PATH="/opt/pybind11:/opt/OpenBLAS/lib:/opt/OpenBLAS:..."

   **NOTE:** You need to include *lib* after *OpenBLAS/* or cmake will not be find OpenBLAS

   The ``...`` represents **THE REST OF THE EXISTING PATH**, so that
   your new path will look something like:

   .. code:: bash

      PATH="/opt/pybind11:/opt/OpenBLAS/lib:/opt/OpenBLAS:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

#. Log out and log back in to set ``PATH``

Compiling Prerequisites
-----------------------

We will be compiling our own pybind11 and OpenBLAS.

Compile and Install pybind11
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we need to install pybind11 to properly expose underlying C++ code
to python.

#. Define path variables

   .. code:: bash

      # Recommended paths
      $: gitParentDir=~/Code
      $: codeDir=~/Code/pybind11
      $: buildDir=~/Build/pybind11
      $: installPath=/opt/pybind11

#. Clone repository

   .. code:: bash

      $: cd $gitParentDir
      $: git clone https://github.com/pybind/pybind11

#. Install python module

   .. code:: bash

      $: cd $codeDir
      $: pip install . --user

   If you are installing using the ``--user`` flag, this should install
   to ``/home/UNAME/.local/lib/python3.6/site-packages/pybind11``.
   Otherwise, if you are using conda, this should install to your conda
   environment, either
   ``/home/UNAME/miniconda3/lib/python3.6/site-packages/pybind11``,
   ``/home/UNAME/.conda/lib/python3.6/site-packages/pybind11``,
   ``/home/UNAME/miniconda3/envs/ENV_NAME/lib/python3.6/site-packages/pybind11``,
   or
   ``/home/UNAME/.conda/envs/ENV_NAME/lib/python3.6/site-packages/pybind11``.

   **NOTE:** you may also install this to your miniconda environment by
   skipping the ``--user`` flag. This module will then only be active
   when the miniconda environment is active.

#. Activate your conda environment

   .. code:: bash

      $: conda activate ENV

#. C++ module and cmake files

   `Link to example on
   github <https://github.com/sdhnshu/pybind_demo>`__. Below adapted
   from link.

   **NOTE:** The required ``cmake`` flags will differ *slightly*
   depending on whether you are compiling using the system python, the
   **base** miniconda python, or an **environment** miniconda python.
   Please read carefully below and use the correct version of the
   command based on your use case.

   If you are installing from an **environment** miniconda python, you
   will need to also specify the python executable and the python
   library. The executable path may be found by running the following
   commands

   Determine the path to your python executable

   .. code:: bash

      (ENV) $: which python
      /home/UNAME/miniconda3/envs/s4py/bin/python

   **NOTE:** Depending on your install, "``miniconda3``" may be
   ``".conda"``, so check to make sure you use your path, not the
   example one listed in the installation instructions.

   In the compilation code below, ``/pth/to/conda/env`` specifically
   corresponds to the location of the conda environment of your choice.
   In the code example above ``/pth/to/conda/env`` would be
   ``/home/UNAME/miniconda3/envs/s4py/``, so the location of the python
   executable is therefore ``/pth/to/conda/env/bin/python``.

   .. code:: bash

      $: mkdir -p $buildDir
      $: cd $buildDir

      # If running from a miniconda environment python (RECOMMENDED)
      $: ccmake $codeDir -DCMAKE_INSTALL_PREFIX=$installPath \
                         -DPYTHON_EXECUTABLE=/pth/to/conda/env/bin/python \
                         -DPYTHON_LIBRARY=/pth/to/conda/env/lib/python3.6m.so

      # If running from the system or base miniconda python:
      $: ccmake $codeDir -DCMAKE_INSTALL_PREFIX=$installPath

      # If this is the first time you run ccmake, you should see a screen
      # displaying "EMPTY CACHE"
      # press "c" once to run the initial configuration
      # press "c" again to run again
      # Now you should see an option "g" to generate the required files

      # Compile. The -jN flag (optional) will use N threads to compile
      $: make install -j10

#. Add install to PATH (**only set if not installing to
   ``/opt/pybind11``**)

   \*Note: this should already be handled *if you followed the previous
   instructions*

   .. code:: bash

      # edit .bashrc PATH
      $: PB11_INSTALL=/opt/pybind11
      export PATH="${PB11_INSTALL}:$PATH"
      $: source .bashrc

Compile and Install OpenBLAS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Note: Make sure to compile OpenBLAS in single-threaded mode: `Search
   for \`multi-threaded' to find the correct flags to include in
   ``make`` <https://github.com/xianyi/OpenBLAS/wiki/faq>`__

#. Define path variables

   .. code:: bash

      # Recommended paths
      $: gitParentDir=~/Code
      $: codeDir=~/Code/OpenBLAS
      $: buildDir=~/Build/OpenBLAS
      $: installPath=/opt/OpenBLAS

#. Clone Repository

   .. code:: bash

      $: cd $codeDir
      $: git clone https://github.com/xianyi/OpenBLAS

#. Ensure optimal performance, otherwise OpenBLAS will use MPI to parallelize and the parallelism gained will be suboptimal.

   .. code:: bash

      $: export OPENBLAS_NUM_THREADS=1

#. There can issues compiling OpenBLAS within an active conda
   environment. You should deactive any active conda 
   environment before compiling OpenBLAS.

   .. code:: bash

      $: conda deactivate

#. Make and Install (NOTE: Slight differences for AMD versus Intel chipsets.)

   .. code:: bash

      $: cd $codeDir
      $: make USE_THREAD=0 PREFIX=$installDir
      $: mkdir -p $buildDir
      $: cd $buildDir

      # AMD chipsets only:
      $: ccmake $codeDir -DUSE_THREAD=0 -DCMAKE_INSTALL_PREFIX=$installDir

      # Intel chipsets only:
      $: ccmake $codeDir -DUSE_THREAD=0 -DCMAKE_INSTALL_PREFIX=$installDir -DTARGET=SKYLAKEX
      # Within the ccmake configurer, hit t to switch to advanced mode 
      # Tell the compiler to expect the skylake architecture
      CMAKE_C_FLAGS   -march=skylake-avx512

      # All
      $: [sudo] make install -j10
      $: cd $codeDir
      $: make USE_THREAD=0 PREFIX=$installPath
      $: [sudo] make USE_THREAD=0 PREFIX=$installPath install

   **Note: for some reason I've only been able to successfully get cmake
   to find both openblas and lapack correctly if installed in this
   strange make-cmake-make order**

#. Add install to PATH (**NOTE:** THIS SHOULD NOT BE NEEDED)

   **Note: for some reason, this seems to be required in order for cmake
   to find this during the compilation of S4** **NOTE:** this may
   actually not be needed. the issue may be related to improperly naming
   the ``OpenBLAS.conf`` file in ``/etc/ld.so.conf.d/`` **Note:** this
   should already be handled *if you followed the previous instructions*

   .. code:: bash

      # edit .bashrc PATH
      export PATH="/pth/to/OpenBLAS_install/lib:/pth/to/OpenBLAS_install:$PATH"
      $: source .bashrc

   **NOTE:** Again, make sure to include both `/pth/to/OpenBLAS_INSTALL/lib` and `/pth/to/OpenBLAS_install`

#. Add ``OPENBLAS_NUM_THREADS=1`` to .bashrc

   .. code:: bash

      # edit .bashrc
      export OPENBLAS_NUM_THREADS=1
      $: source .bashrc

Install S4
~~~~~~~~~~

Now to install S4. Instructions are very similar to the above.

#. Ensure that the version of python you are using during compilation is
   the same that you will be using when running (as of <2018-12-18 Tue>
   3.6 is recommended and specified in the s4py.yml)

#. We recommend installing S4 within the s4py conda environment to avoid
   version conflicts, though you may use the system python if desired:

   .. code:: bash
   $: conda activate s4py

#. Define path variables

   **Note**: You do not have to install to ``/opt/``. On your own
   machine you can install wherever you would like. If you omit
   ``-DCMAKE_INSTALL_PREFIX``, S4 will install to ``~/.local``

   .. code:: bash

      # Recommended paths
      $: gitParentDir=~/Code
      $: codeDir=~/Code/S4
      $: buildDir=~/Build/S4
      $: installPath=/opt

#. Clone S4

   .. code:: bash

      $: cd $codeDir
      $: git clone https://github.com/harperes/S4.git

#. Compile S4

   .. code:: bash

      $: cd $buildDir
      $: ccmake $codeDir -DCMAKE_INSTALL_PREFIX=$installPath
      $: [sudo] make install -j6

   **Note: on the cluster, S4 is properly compiled for all users by
   the admins. make sure that the paths are correct**

   You **shouldn't** need to add in other arguments; the cmake scripts
   will be updated as needed to ensure the build process is as smooth as
   possible.

#. Ensure that Python can find S4

   In order to use S4, S4 must be on the ``PYTHONPATH``. If you install
   to ``~/.local`` S4 should already be on your ``PYTHONPATH``. If you
   install to ``/opt/``, make sure to add the following to either
   ``/etc/environment`` or ``~/.bashrc``. If you compile from within an
   anaconda environment, S4 might be installed to that specific anaconda
   environment

   #. ``/etc/environment``

      .. code:: bash

         PYTHONPATH='/opt'

   #. ``~/.bashrc/``

      .. code:: bash

         export PYTHONPATH='/opt:$PYTHONPATH'

#. Verify S4 installation

   .. code:: bash

      $: conda activate ENV_NAME
      $: cd $codeDir/tests
      # run unit tests
      $: python -m unittest

#. If the unittest failed, you may have build in the wrong directory
   or you may need to re-run ldconfig
   .. code:: bash
   $: sudo ldconfig

Appendix: System vs ``conda`` python
====================================

Conda will allow you to install any version of python your heart
desires. Ubuntu 18.04 ships with python 3.6, and it is much more
difficult to switch system python versions. When compiling your own
python packages against the system python, they may only be used by the
same conda version of python.

**Be sure to use the same conda python version (3.6) in conda as the
system python!**

S4 may be compiled against either the system python or a conda version
of python. Currently no issues are known compiling against one and using
in both, provided the minor version of python e.g. 3.*x\* is the same.
For the purposes of this guide, it is assumed that you will be using an
anaconda version of python.

A good heuristic is to install python packages from ``conda`` and
everything else from the Ubuntu Software center / Synaptic / ``apt``.
This is especially important for running anything related to machine
learning because:

#. The conda repositories are more up-to-date than the Ubuntu
   repositories
#. conda provides a simple way to create and use multiple environments
#. conda packages are better optimized than those from pip
#. gpu-enabled versions of tensorflow and keras are available and
   correctly install in one line of code

If you are compiling your own version of software e.g. S4, you will need
to install some packages from the Ubuntu software center. It appears to
be possible to compile against the system (Ubuntu) python and run from a
conda python, but not the other way around. With that in mind, please
refer to the following sections to assist in properly setting up your
computer to compile and run software.

Select and use Ubuntu (system) python
-------------------------------------

**NOTE:** When you install miniconda, you usually add the miniconda
python path to your main path. In your ``.bashrc`` file, that line looks
something like:

.. code:: bash

   ...
   # added by Miniconda3 installer
   export PATH="/home/${USER}/miniconda3/bin:$PATH"
   ...

To avoid using this python when compiling your own software and compile
against the system python, comment out the above line so that it looks
like

.. code:: bash

   ...
   # added by Miniconda3 installer
   # export PATH="/home/${USER}/miniconda3/bin:$PATH"
   ...

Now, either start a new terminal or re-source your .bashrc
(``$: source ~/.bashrc``). Check that the correct python is now
selected:

.. code:: bash

   # Miniconda python
   $: which python
   /home/UNAME/miniconda3/bin/python
   # System python
   $: which python3
   /usr/bin/python3

**Note: you need to specify python3 to use python3.6 rather than 2.7 for
the system python (you can alter this behavior in your ``.bash_aliases``
file)**

Now the miniconda python and any associated libraries/packages will not
be loaded, and you are free to use the packages available in the Ubuntu
repositories

.. |S4| replace:: S\ :sup:`4`
