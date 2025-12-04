cmake_minimum_required(VERSION 3.20)

if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.27)
    cmake_policy(SET CMP0148 NEW)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 20)

project(${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 REQUIRED)
find_package(uproot-custom REQUIRED)

# ==============================
#    Declare the C++ module
# ==============================
pybind11_add_module(pyjuno_cpp
    mod.cc
)
target_link_libraries(pyjuno_cpp PRIVATE uproot-custom)

# Install the module to the package directory
if(DEFINED SKBUILD_PROJECT_NAME)
    install(
        TARGETS pyjuno_cpp
        LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME}
    )
endif()
