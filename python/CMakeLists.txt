pybind11_add_module(sun_earth_geometry main.cpp spa_interface.cpp)

if(APPLE)
    set_target_properties(sun_earth_geometry PROPERTIES
       BUILD_RPATH "@loader_path" 
    )
elseif(UNIX)
    set_target_properties(sun_earth_geometry PROPERTIES
       BUILD_RPATH "${ORIGIN}" 
    )
endif()

target_link_libraries(sun_earth_geometry PRIVATE spa)

target_include_directories(sun_earth_geometry PUBLIC ${PROJECT_SOURCE_DIR}/src)
# # EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# # define (VERSION_INFO) here.
target_compile_definitions(sun_earth_geometry PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})