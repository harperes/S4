# - Find LUA
# Find installed LUA libraries

if (LUA_INCLUDES)
   set(LUA_FIND_QUIETLY TRUE)
endif (LUA_INCLUDES)

find_path(LUA_INCLUDES lua)
find_library(LUA_LIBRARIES NAMES lua)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(LUA DEFAULT_MSG LUA_LIBRARIES LUA_INCLUDES)

mark_as_advanced(LUA_LIBRARIES LUA_INCLUDES)