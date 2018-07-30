# - Find Accelerators
# Set the correct accelerator flags as necessary

if (NOT APPLE)

  set(vecLIB_LINKER_LIBS -llapack -lblas)
  mark_as_advanced(vecLib_LINKER_LIBS)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_BLAS")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_LAPACK")

else()

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
  endif()

  # set(vecLib_LINKER_LIBS -lcblas "-framework Accelerate")
  set(vecLib_LINKER_LIBS "-framework Accelerate")
  mark_as_advanced(vecLib_LINKER_LIBS)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_BLAS")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_LAPACK")
  
endif()
