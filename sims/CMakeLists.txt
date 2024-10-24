cmake_minimum_required(VERSION 3.22)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(mc C)
set(CMAKE_C_STANDARD 99)


add_executable(
    ${PROJECT_NAME}
    main.c
    monte_carlo.c
)

target_compile_definitions(${CMAKE_PROJECT_NAME} PUBLIC $<$<CONFIG:Debug>:DEBUG>)
target_compile_options(${CMAKE_PROJECT_NAME} PUBLIC -g -O0)
target_include_directories(${CMAKE_PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

