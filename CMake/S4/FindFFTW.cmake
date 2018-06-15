# - Find FFTW
# Find installed FFTW libraries

find_path(FFTW3_INC fftw3.h)
find_library(FFTW3_LIB NAMES fftw3)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(FFTW DEFAULT_MSG FFTW3_LIB FFTW3_INC)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_LIBFFTW3 ${FFTW_INC}")

mark_as_advanced(FFTW3_LIB FFTW3_INC)
