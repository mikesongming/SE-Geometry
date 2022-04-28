pybind11_add_module(_sun_earth_geometry main.cpp spa_analyzer.cpp)

if(APPLE)
    set_target_properties(_sun_earth_geometry PROPERTIES
       BUILD_RPATH "@loader_path" 
    )
elseif(UNIX)
    set_target_properties(_sun_earth_geometry PROPERTIES
       BUILD_RPATH "${ORIGIN}" 
    )
endif()

target_link_libraries(_sun_earth_geometry PRIVATE spa)
target_include_directories(_sun_earth_geometry PRIVATE ${PROJECT_SOURCE_DIR}/src)

# # SDIST_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# # define (VERSION_INFO) here.
target_compile_definitions(_sun_earth_geometry PRIVATE VERSION_INFO=${SDIST_VERSION_INFO})