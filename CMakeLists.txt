cmake_minimum_required(VERSION 3.16.0)

project(FSEG)

set(CMAKE_CXX_STANDARD 11)

cmake_policy(SET CMP0095 NEW)
# cmake_policy(SET CMP0068 NEW)
include(CMakePrintHelpers)

if (MSVC)
    # Tell cmake we want it to automate generating an export stub for the dll
    SET(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

    # /Zc:preprocessor enables a token-based preprocessor that conforms to C99 and C++11 and later standards
    # /Zc:preprocessor option is available starting with VS2019 version 16.5
    # (according to https://docs.microsoft.com/en-us/cpp/build/reference/zc-preprocessor)
    # That version is equivalent to _MSC_VER==1925
    # (according to https://docs.microsoft.com/en-us/cpp/preprocessor/predefined-macros)
    # CMake's ${MSVC_VERSION} is equivalent to _MSC_VER
    # (according to https://cmake.org/cmake/help/latest/variable/MSVC_VERSION.html#variable:MSVC_VERSION)
    if (MSVC_VERSION GREATER_EQUAL 1925)
        cmake_print_variables(MSVC_VERSION)
        add_compile_options(/Zc:preprocessor)
    else()
        message(FATAL_ERROR "MSVC compiler before VS2019 Update5 are not supported")
    endif()

else()
    # link math.h
    LINK_LIBRARIES(m)
endif()


find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
    message(STATUS "Set up ccache ...")
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ccache) # Less useful to do it for linking, see edit2
endif(CCACHE_FOUND)

# fetch pybind11 when building
set(FETCHCONTENT_UPDATES_DISCONNECTED ON CACHE BOOL "Disable updating fetched content")

include(FetchContent)
FetchContent_Declare(pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.9.2
)
FetchContent_MakeAvailable(pybind11)

add_subdirectory(src)

# enable_testing()
# add_subdirectory(tests)
