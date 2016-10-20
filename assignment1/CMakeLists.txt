cmake_minimum_required(VERSION 3.3)
project(assignment1)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    classifier.c
    headers.h
    predicates.c)

add_executable(assignment1 ${SOURCE_FILES})