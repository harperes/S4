######################
# Perform setup to make a target into a functional python module
macro(setup_pymodule target)
set_target_properties(${target} PROPERTIES PREFIX "")
if (APPLE)
    set_target_properties(${target} PROPERTIES SUFFIX ".so")
endif(APPLE)
# target_link_libraries(${target} ${PYTHON_LIBRARIES} ${TBB_LIBRARY})
target_link_libraries(${target} ${PYTHON_LIBRARIES})
# fix_tbb_rpath(${target})
fix_conda_python(${target})
endmacro(setup_pymodule)
#####################

# file(GLOB_RECURSE PXIS ${CMAKE_CURRENT_SOURCE_DIR}/../freud/*.pxi)
# file(GLOB_RECURSE PYXS ${CMAKE_CURRENT_SOURCE_DIR}/../freud/*.pyx)

# set(PYX_CPPS ${CMAKE_CURRENT_SOURCE_DIR}/../freud/_freud.cpp)

set(ENABLE_CYTHON OFF CACHE BOOL "Regenerate cython sources")
if(ENABLE_CYTHON)
  foreach(pyx IN LISTS PYXS)
    file(RELATIVE_PATH pyx_rel ${CMAKE_CURRENT_SOURCE_DIR} ${pyx})
    string(REPLACE ".pyx" ".cpp" cpp_rel "${pyx_rel}")
    set(cpp_out "${CMAKE_CURRENT_SOURCE_DIR}/${cpp_rel}")
    add_custom_command(OUTPUT ${cpp_out}
                       COMMAND ${CYTHON_EXECUTABLE} -X boundscheck=False -o ${cpp_out} -w ${CMAKE_CURRENT_SOURCE_DIR}/../freud --cplus ${pyx}
                       DEPENDS ${pyx} ${PXIS})
    set_source_files_properties(${cpp_out} PROPERTIES GENERATED TRUE)
    list(APPEND CYTHON_SOURCES ${cpp_out})
  endforeach(pyx in LISTS PYXS)
else(ENABLE_CYTHON)
  set(CYTHON_SOURCES ${PYX_CPPS})
endif(ENABLE_CYTHON)

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
# add_library(S4 MODULE ${SOURCES} ${CYTHON_SOURCES})
# add_library(S4 STATIC ${SOURCES})
add_library(libS4 OBJECT ${SOURCES})
# target_link_libraries(S4 ${LUA_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})
add_executable(S4 $<TARGET_OBJECTS:libS4> main_lua.c)
target_link_libraries(S4 ${LUA_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB})

# these may work; unsure
# add_library(_S4 MODULE ${SOURCES} main_python.c)
# target_link_libraries(_S4 ${PYTHON_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})
# set_target_properties(_S4 PROPERTIES PREFIX "")
# set_target_properties(_S4 PROPERTIES SUFFIX ".so")
# fix_conda_python(_S4)

# set_target_properties(luaS4 PROPERTIES LINK_FLAGS "-static")
# target_link_libraries(luaS4 S4)
# setup_pymodule(S4)

# Make Lua Frontend
# set_source_files_properties(main_lua.c PROPERTIES COMPILE_DEFINITIONS NO_IMPORT_ARRAY)
# add_executable(luaS4 main_lua.c)
# target_link_libraries(luaS4 ${LUA_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})

# INSTALL(TARGETS _freud
  # LIBRARY DESTINATION freud
  # )