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

# set(ENABLE_CYTHON OFF CACHE BOOL "Regenerate cython sources")
# if(ENABLE_CYTHON)
#   foreach(pyx IN LISTS PYXS)
#     file(RELATIVE_PATH pyx_rel ${CMAKE_CURRENT_SOURCE_DIR} ${pyx})
#     string(REPLACE ".pyx" ".cpp" cpp_rel "${pyx_rel}")
#     set(cpp_out "${CMAKE_CURRENT_SOURCE_DIR}/${cpp_rel}")
#     add_custom_command(OUTPUT ${cpp_out}
#                        COMMAND ${CYTHON_EXECUTABLE} -X boundscheck=False -o ${cpp_out} -w ${CMAKE_CURRENT_SOURCE_DIR}/../freud --cplus ${pyx}
#                        DEPENDS ${pyx} ${PXIS})
#     set_source_files_properties(${cpp_out} PROPERTIES GENERATED TRUE)
#     list(APPEND CYTHON_SOURCES ${cpp_out})
#   endforeach(pyx in LISTS PYXS)
# else(ENABLE_CYTHON)
#   set(CYTHON_SOURCES ${PYX_CPPS})
# endif(ENABLE_CYTHON)

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
# add_library(S4 MODULE ${SOURCES} ${CYTHON_SOURCES})
# add_library(S4 STATIC ${SOURCES})
add_library(libS4 OBJECT ${SOURCES})
# target_link_libraries(S4 ${LUA_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})
add_executable(luaS4 $<TARGET_OBJECTS:libS4> main_lua.c)
target_link_libraries(luaS4 ${LUA_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB})

# these may work; unsure
# add_library(_S4 MODULE ${SOURCES} main_python.c)
# target_link_libraries(_S4 ${PYTHON_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})
# set_target_properties(_S4 PROPERTIES PREFIX "")
# set_target_properties(_S4 PROPERTIES SUFFIX ".so")
# fix_conda_python(_S4)

# this is already done
add_library(testS4 SHARED ${SOURCES})
target_link_libraries(testS4 ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})
# this should work; doesn't seem to...
# set_target_properties(testS4 PROPERTIES
#   MACOSX_RPATH "/Users/harperic/.local/lib/python3.6/site-packages/S4/libtestS4.dylib"
#   BUILD_WITH_INSTALL_RPATH TRUE
#   INSTALL_RPATH_USE_LINK_PATH TRUE
#   INSTALL_RPATH "/Users/harperic/.local/lib/python3.6/site-packages/S4/libtestS4.dylib")
# set_target_properties(testS4 PROPERTIES INSTALL_RPATH ${PYTHON_MODULE_BASE_DIR})
pybind11_add_module(_S4 ${CMAKE_CURRENT_SOURCE_DIR}/new_python.cpp)
target_link_libraries(_S4 PRIVATE testS4 ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})

# set_target_properties(S4 PROPERTIES PREFIX "poop")


# set_target_properties(S4 PROPERTIES INSTALL_RPATH_USE_LINK_PATH FALSE)
# try this fix
# if (APPLE)
  # get_target_property(_target_exe testS4 LOCATION)
# add_custom_command(TARGET S4 POST_BUILD
    # COMMAND install_name_tool ARGS -change libtestS4.dylib $<TARGET_FILE:testS4> $<TARGET_FILE:S4>)
  # add_custom_command(TARGET testS4 POST_BUILD
    # COMMAND install_name_tool ARGS -id "@rpath/libtestS4.dylib" libtestS4.dylib)
# endif(APPLE)

# message("$<TARGET_FILE:testS4>")
# target_link_libraries(luaS4 S4)
# setup_pymodule(S4)

# set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# Make Lua Frontend
# set_source_files_properties(main_lua.c PROPERTIES COMPILE_DEFINITIONS NO_IMPORT_ARRAY)
# add_executable(luaS4 main_lua.c)
# target_link_libraries(luaS4 ${LUA_LIBRARIES} ${vecLib_LINKER_LIBS} ${FFTW3_LIB} ${MPI_LIBRARY})

# I need to fix this since this apparently isn't correct...
INSTALL(TARGETS testS4
  LIBRARY DESTINATION ${PYTHON_MODULE_BASE_DIR}
  )
INSTALL(TARGETS _S4
  LIBRARY DESTINATION ${PYTHON_MODULE_BASE_DIR}
  )

# this works...enough...it's incredibly crummy right now now, but it "works"
# try to use the "rpath" change, then use the rpath as the "handle" to institute the correct change...
if (APPLE)
  add_custom_command(TARGET _S4
    POST_BUILD COMMAND
    # ${CMAKE_INSTALL_NAME_TOOL} -change "/Users/harperic/build/S4/cpp/libtestS4.dylib" "/Users/harperic/.local/lib/python3.6/site-packages/S4/libtestS4.dylib" $<TARGET_FILE:S4>)
    ${CMAKE_INSTALL_NAME_TOOL} -change "${CMAKE_CURRENT_BINARY_DIR}/libtestS4.dylib" "${CMAKE_INSTALL_PREFIX}/${PYTHON_MODULE_BASE_DIR}/libtestS4.dylib" $<TARGET_FILE:_S4>)
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
