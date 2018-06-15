macro(fix_conda_python target)
if (_using_conda AND APPLE)
get_filename_component(_python_lib_file ${PYTHON_LIBRARY} NAME)
add_custom_command(TARGET ${target} POST_BUILD
                          COMMAND install_name_tool ARGS -change ${_python_lib_file} ${PYTHON_LIBRARY} $<TARGET_FILE:${target}>)
endif (_using_conda AND APPLE)
endmacro()
