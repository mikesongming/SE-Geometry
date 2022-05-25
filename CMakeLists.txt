cmake_minimum_required(VERSION 3.16.0)

project(FSEG VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 11)

cmake_policy(SET CMP0095 NEW)
# cmake_policy(SET CMP0068 NEW)
include(CMakePrintHelpers)

# set default output path
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/bin")

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

add_subdirectory(src)
add_subdirectory(python)

# enable_testing()
# add_subdirectory(tests)

# set(CPACK_PROJECT_NAME ${PROJECT_NAME})
# set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
# include(CPack)
