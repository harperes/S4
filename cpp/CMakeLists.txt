######################
# Perform setup to make a target into a functional python module
macro(setup_pymodule target)
set_target_properties(${target} PROPERTIES PREFIX "")
if (APPLE)
    set_target_properties(${target} PROPERTIES SUFFIX ".so")
endif(APPLE)
target_link_libraries(${target} ${PYTHON_LIBRARIES})
fix_conda_python(${target})
endmacro(setup_pymodule)
#####################

set(PYTHON_MODULE_BASE_DIR S4)

# ${CMAKE_CURRENT_SOURCE_DIR} refers to cpp
include_directories(${CMAKE_CURRENT_SOURCE_DIR}
                    ${CMAKE_CURRENT_SOURCE_DIR}/RNP
                    ${CMAKE_CURRENT_SOURCE_DIR}/ffm
                    ${CMAKE_CURRENT_SOURCE_DIR}/kiss_fft
                    ${CMAKE_CURRENT_SOURCE_DIR}/pattern
                    ${CMAKE_CURRENT_BINARY_DIR}
                    )

set(S4_SOURCES
    S4.cpp
    rcwa.cpp
    fmm/fmm_common.cpp
    fmm/fmm_FFT.cpp
    fmm/fmm_kottke.cpp
    fmm/fmm_closed.cpp
    fmm/fmm_PolBasisNV.cpp
    fmm/fmm_PolBasisVL.cpp
    fmm/fmm_PolBasisJones.cpp
    fmm/fmm_experimental.cpp
    fmm/fft_iface.cpp
    pattern/pattern.c
    pattern/intersection.c
    pattern/predicates.c
    numalloc.c
    gsel.c
    sort.c
    kiss_fft/kiss_fft.c
    kiss_fft/tools/kiss_fftnd.c
    SpectrumSampler.c
    cubature.c
    Interpolator.c
    convert.c
    RNP/Eigensystems.cpp
            )

foreach(src IN LISTS S4_SOURCES)
  list(APPEND SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/${src})
endforeach(src IN LISTS S4_SOURCES)

set_source_files_properties(${SOURCES} PROPERTIES COMPILE_DEFINITIONS NO_IMPORT_ARRAY)
# add_library(libS4 OBJECT ${SOURCES})
# add_executable(luaS4 $<TARGET_OBJECTS:libS4> main_lua.c)
# target_link_libraries(luaS4 ${LUA_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB})

# this is already done
add_library(S4 SHARED ${SOURCES})
# target_link_libraries(testS4 ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY} ${BLAS_LIBRARIES} ${LAPACK_LIBRARIES})
target_link_libraries(S4 ${LINALG_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})
pybind11_add_module(_S4 ${CMAKE_CURRENT_SOURCE_DIR}/python.cpp)
target_link_libraries(_S4 PRIVATE S4 ${LINALG_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY} )


# I need to fix this since this apparently isn't correct...
INSTALL(TARGETS S4
  LIBRARY DESTINATION ${PYTHON_MODULE_BASE_DIR}
  )
INSTALL(TARGETS _S4
  LIBRARY DESTINATION ${PYTHON_MODULE_BASE_DIR}
  )

# need to change the dylib path on macOS/OSX
if (APPLE)
  add_custom_command(TARGET _S4
    POST_BUILD COMMAND
    ${CMAKE_INSTALL_NAME_TOOL} -change "${CMAKE_CURRENT_BINARY_DIR}/libS4.dylib" "${CMAKE_INSTALL_PREFIX}/${PYTHON_MODULE_BASE_DIR}/libS4.dylib" $<TARGET_FILE:_S4>)
endif(APPLE)

MACRO(copy_file file)
    add_custom_command (
        OUTPUT ${file}
        DEPENDS ${file}
        POST_BUILD
        COMMAND    ${CMAKE_COMMAND}
        ARGS       -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
        COMMENT    "Copy ${file}"
    )
ENDMACRO(copy_file)

set (files __init__.py)

install(FILES ${files} DESTINATION ${PYTHON_MODULE_BASE_DIR})

foreach(file ${files})
  copy_file(${file})
endforeach()
