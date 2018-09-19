# - Find Accelerators
# Set the correct accelerator flags as necessary

if (NOT APPLE)

# I need lines here to allow an env var set...unless there's a BLAS helper for that already...

find_package(BLAS REQUIRED)
find_package(LAPACK REQUIRED)

 # set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${BLAS_LINKER_FLAGS} -lcblas -lblas -DHAVE_BLAS ${LAPACK_LINKER_FLAGS} -DHAVE_LAPACK -llapack")
 set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${BLAS_LINKER_FLAGS} -DHAVE_BLAS ${LAPACK_LINKER_FLAGS} -DHAVE_LAPACK")
 mark_as_advanced(BLAS_LIBRARIES)
 mark_as_advanced(LAPACK_LIBRARIES)
message("${BLAS_LINKER_FLAGS}")
 set(LINALG_LIBS ${BLAS_LIBRARIES} ${LAPACK_LIBRARIES} CACHE PATH "LIBRARIES NEEDED FOR LINEAR ALGEBRA ACCELERATION")
 mark_as_advanced(LINALG_LIBS)

else(NOT APPLE)

  set(__veclib_include_suffix "Frameworks/vecLib.framework/Versions/Current/Headers")
  exec_program(xcode-select ARGS -print-path OUTPUT_VARIABLE CMAKE_XCODE_DEVELOPER_DIR)
  find_path(vecLib_INCLUDES vecLib.h
    DOC "vecLib include directory"
    PATHS /System/Library/Frameworks/Accelerate.framework/Versions/Current/${__veclib_include_suffix}
    /System/Library/${__veclib_include_suffix}
    ${CMAKE_XCODE_DEVELOPER_DIR}/Platforms/MacOSX.platform/Developer/SDKs/MaxOSX.sdk/System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Headers/
    NO_DEFAULT_PATH)
  include(FindPackageHandleStandardArgs)
  find_package_handle_standard_args(vecLib DEFAULT_MSG vecLib_INCLUDES)

  if(vecLIB_FOUND)
    if(vecLib_INCLUDES MATCHES "^/System/Library/Frameworks/vecLib.framework.*")

      set(vecLib_LINKER_LIBS -lcblas "-framework vecLib")
      message(STATUS "Found standalone vecLib.framework")
    else()
      set(vecLib_LINKER_LIBS -lcblas "-framework Accelerate")
      message(STATUS "Found veclib as part of Accelerate")
    endif()
    mark_as_advanced(vecLib_INCLUDES)
    mark_as_advanced(vecLib_LINKER_LIBS)
  endif(vecLIB_FOUND)

  # set(vecLib_LINKER_LIBS -lcblas "-framework Accelerate")
  set(vecLib_LINKER_LIBS "-framework Accelerate")
  mark_as_advanced(vecLib_LINKER_LIBS)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_BLAS")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_LAPACK")

  set(LINALG_LIBS "-framework Accelerate" CACHE STRING "LIBRARIES NEEDED FOR LINEAR ALGEBRA ACCELERATION")

endif(NOT APPLE)
