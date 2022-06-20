# set(CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE ON)
add_library(spa SHARED SPA/spa.c SPA/spa.h)

add_executable(spa_tester SPA/spa_tester.c)
cmake_print_variables(CMAKE_CURRENT_BINARY_DIR)
set_target_properties(spa_tester PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY          ${CMAKE_CURRENT_BINARY_DIR}/bin
        RUNTIME_OUTPUT_DIRECTORY_DEBUG    ${CMAKE_CURRENT_BINARY_DIR}/bin
        RUNTIME_OUTPUT_DIRECTORY_RELEASE  ${CMAKE_CURRENT_BINARY_DIR}/bin
)
target_link_libraries(spa_tester PRIVATE spa)
target_include_directories(spa_tester PRIVATE ${PROJECT_SOURCE_DIR}/src)
