# set(CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE ON)
add_library(spa SHARED SPA/spa.c SPA/spa.h)

add_executable(spa_tester SPA/spa_tester.c)
target_link_libraries(spa_tester PRIVATE spa)
target_include_directories(spa_tester PRIVATE ${PROJECT_SOURCE_DIR}/src)
