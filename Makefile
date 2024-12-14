CC = g++
CFLAGS = -Wall -g -I./cpp/include  # Add include directory under cpp folder

# Specify the source and object directories
SRC_DIR = cpp/src
INCLUDE_DIR = cpp/include
OBJ_DIR = obj

# Create a list of all source files in cpp/src, including main.cpp
SRCS = $(wildcard $(SRC_DIR)/*.cpp) cpp/main.cpp

# Generate the corresponding object files in the obj directory
OBJ = $(SRCS:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)

TARGET = ScienceFair


COMPILER_FLAGS = -w
LINKER_FLAGS = -lSDL2

# Rule to link object files into the executable
$(TARGET): $(OBJ)
	$(CC) $(OBJ) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(TARGET)

# Rule to compile each source file into an object file
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp  # Match files in src/ and place obj in obj/
	@mkdir -p $(OBJ_DIR)  # Ensure the object directory exists
	$(CC) $(CFLAGS) -c $< -o $@  # Compile the .cpp into .o

# Clean the build (remove object files and executable)
clean:
	rm -rf $(OBJ_DIR) $(TARGET)
