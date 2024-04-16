cmake_minimum_required (VERSION 2.6)
project(SBIGDriver)

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -fPIC -g") 

add_executable(SBIGDriver main.cpp)

include_directories(SBIGDriver /usr/local/include)
target_link_libraries(SBIGDriver /usr/local/lib/libdlapi.dylib /usr/local/lib/libcfitsio.a m curl)
