cmake_minimum_required(VERSION 3.0.0)
project(sun_earth_geometry VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 11)

# set default output path
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/bin")
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/lib")
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/arch")

include(CMakePrintHelpers)

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
# add_subdirectory(tests)

add_subdirectory(python)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)