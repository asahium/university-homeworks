cmake_minimum_required(VERSION 3.13)

project(caos)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_C_FLAGS "-fsanitize=address")

include_directories(.)

set(CONTEST 23)
set(CONTEST_TASK 4)

set(CHECK 9)
set(CHECK_TASK 3)

set(contest contest_${CONTEST}_${CONTEST_TASK})
set(check check_${CHECK}_${CHECK_TASK})

add_executable(${contest} ${CONTEST}/${CONTEST_TASK}.c)
add_executable(${check} 0_checks/${CHECK}/${CHECK_TASK}.c )

target_link_libraries(${contest} dl m pthread)
target_link_libraries(${check} dl m pthread)

