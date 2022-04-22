cmake_minimum_required(VERSION 3.16.0)

project(sun_earth_geometry VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 11)

cmake_policy(SET CMP0095 NEW)

# set default output path
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/bin")

# cmake_policy(SET CMP0068 NEW)
include(CMakePrintHelpers)

# set(CMAKE_SKIP_BUILD_RPATH TRUE)                 # 编译时加上RPATH
# set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)         # 编译时RPATH不使用安装的RPATH
# set(CMAKE_INSTALL_RPATH "")                       # 安装RPATH为空
# set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)      # 安装的执行文件不加上RPATH

find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
    message(STATUS "Set up ccache ...")
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ccache) # Less useful to do it for linking, see edit2
endif(CCACHE_FOUND)

find_package(pybind11 CONFIG)
if(pybind11_FOUND)
    message(STATUS "Found pybind11")
endif(pybind11_FOUND)

# include_directories(src/SPA)
# file(GLOB_RECURSE SPA_SRC src/SPA/spa.c src/SPA/spa.h)

add_subdirectory(src)
add_subdirectory(python)

# enable_testing()
# add_subdirectory(tests)

# set(CPACK_PROJECT_NAME ${PROJECT_NAME})
# set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
# include(CPack)
