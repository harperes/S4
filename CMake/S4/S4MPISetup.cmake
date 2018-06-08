# Maintainer: harperic

##################################
## Find MPI
# INCLUDE_DIRECTORIES(/opt/local/include/mpich-mp)
# LINK_DIRECTORIES(/opt/local/lib/mpich-mp)
if (ENABLE_MPI)
    # the package is needed
    find_package(MPI REQUIRED)

    mark_as_advanced(MPI_EXTRA_LIBRARY)
    mark_as_advanced(MPI_LIBRARY)
    mark_as_advanced(OMPI_INFO)

    if (MPI_LIBRARY MATCHES mpich)
        # find out if this is MVAPICH2
        get_filename_component(_mpi_library_dir ${MPI_LIBRARY} PATH)
        find_program(MPICH2_VERSION
            NAMES mpichversion mpich2version
            HINTS ${_mpi_library_dir} ${_mpi_library_dir}/../bin
        )
        if (MPICH2_VERSION)
            execute_process(COMMAND ${MPICH2_VERSION}
                            OUTPUT_VARIABLE _output)
        endif()
    elseif(MPI_LIBRARY MATCHES libmpi)
        # find out if this is OpenMPI
        get_filename_component(_mpi_library_dir ${MPI_LIBRARY} PATH)
        find_program(OMPI_INFO
            NAMES ompi_info
            HINTS ${_mpi_library_dir} ${_mpi_library_dir}/../bin
        )
        if (OMPI_INFO)
            execute_process(COMMAND ${OMPI_INFO}
                            OUTPUT_VARIABLE _output)
        endif()
    endif()
    if (ENABLE_MPI)
        # add include directories
        include_directories(${MPI_C_INCLUDE_PATH})
    endif()
endif (ENABLE_MPI)

# set(MPI_INC /opt/local/include/mpich-mp)
# set(MPI_LIB /opt/local/lib/mpich-mp "-lstdc++ -lmpi_cxx")
# include_directories(${MPI_INC})
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DHAVE_MPI ${MPI_INC}")

