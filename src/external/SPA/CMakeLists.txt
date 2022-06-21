# set(CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE ON)
add_library(spa SHARED spa.c spa.h)

add_executable(spa_tester spa_tester.c)
cmake_print_variables(CMAKE_CURRENT_BINARY_DIR)
# use PROJECT_BINARY_DIR
set_target_properties(spa_tester PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY          ${PROJECT_BINARY_DIR}/bin
        RUNTIME_OUTPUT_DIRECTORY_DEBUG    ${PROJECT_BINARY_DIR}/bin
        RUNTIME_OUTPUT_DIRECTORY_RELEASE  ${PROJECT_BINARY_DIR}/bin
)
target_link_libraries(spa_tester PRIVATE spa)
# target_include_directories(spa_tester PRIVATE ${PROJECT_SOURCE_DIR}/src/SPA)
