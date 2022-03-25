add_executable(spa_tester spa_tester.c)
target_link_libraries(spa_tester PRIVATE spa)
target_include_directories(spa_tester PRIVATE ${PROJECT_SOURCE_DIR}/src)