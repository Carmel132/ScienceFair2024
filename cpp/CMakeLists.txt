cmake_minimum_required(VERSION 3.10)

# Define the project name and the programming language.
project(ScienceFair LANGUAGES CXX)

# Specify the C++ standard.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include the project's own header files.
include_directories(${PROJECT_SOURCE_DIR}/include)

# Include the SDL2 header directory.
include_directories("C:/Users/User/vclib/C++/SDL2-2.0.16/include")

# Collect all the .cpp files in the src directory.
file(GLOB SRC_FILES "${PROJECT_SOURCE_DIR}/src/*.cpp")

# Also collect main.cpp (assumed to be in the root).
file(GLOB ROOT_FILES "${PROJECT_SOURCE_DIR}/*.cpp")

# Create the executable.
add_executable(${PROJECT_NAME} ${ROOT_FILES} ${SRC_FILES})

# Specify the SDL2 library directory in lib/x64.
link_directories("C:/Users/User/vclib/C++/SDL2-2.0.16/lib/x64")
# Enable C++ 17
#target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)
# Link against the SDL2 libraries.
target_link_libraries(${PROJECT_NAME}
    "C:/Users/User/vclib/C++/SDL2-2.0.16/lib/x64/SDL2main.lib"
    "C:/Users/User/vclib/C++/SDL2-2.0.16/lib/x64/SDL2.lib"
)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
