pybind11_add_module(_fseg main.cpp algorithm.cpp spa_calculator.cpp)

if(APPLE)
    set_target_properties(_fseg PROPERTIES
       BUILD_RPATH "@loader_path"
    )
elseif(UNIX)
    set_target_properties(_fseg PROPERTIES
       BUILD_RPATH "${ORIGIN}"
    )
endif()

# target_link_libraries(_fseg PRIVATE spa)
target_link_libraries(_fseg PRIVATE date::date-tz spa)
target_include_directories(_fseg PRIVATE include ${PROJECT_SOURCE_DIR}/src/external)

# # SDIST_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# # define (VERSION_INFO) here.
target_compile_definitions(_fseg PRIVATE VERSION_INFO=${SDIST_VERSION_INFO})
