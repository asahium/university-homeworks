# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /app/extra/clion/bin/cmake/linux/bin/cmake

# The command to remove a file.
RM = /app/extra/clion/bin/cmake/linux/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/algorithms_and_data_structures.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/algorithms_and_data_structures.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/algorithms_and_data_structures.dir/flags.make

CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.o: CMakeFiles/algorithms_and_data_structures.dir/flags.make
CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.o: ../3/A.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.o -c /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/3/A.cpp

CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/3/A.cpp > CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.i

CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/3/A.cpp -o CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.s

# Object files for target algorithms_and_data_structures
algorithms_and_data_structures_OBJECTS = \
"CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.o"

# External object files for target algorithms_and_data_structures
algorithms_and_data_structures_EXTERNAL_OBJECTS =

algorithms_and_data_structures: CMakeFiles/algorithms_and_data_structures.dir/3/A.cpp.o
algorithms_and_data_structures: CMakeFiles/algorithms_and_data_structures.dir/build.make
algorithms_and_data_structures: CMakeFiles/algorithms_and_data_structures.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable algorithms_and_data_structures"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/algorithms_and_data_structures.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/algorithms_and_data_structures.dir/build: algorithms_and_data_structures
.PHONY : CMakeFiles/algorithms_and_data_structures.dir/build

CMakeFiles/algorithms_and_data_structures.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/algorithms_and_data_structures.dir/cmake_clean.cmake
.PHONY : CMakeFiles/algorithms_and_data_structures.dir/clean

CMakeFiles/algorithms_and_data_structures.dir/depend:
	cd /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/cmake-build-debug /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/cmake-build-debug /home/wurm/Documents/GitHub/second-year/algorithms-and-data-structures/cmake-build-debug/CMakeFiles/algorithms_and_data_structures.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/algorithms_and_data_structures.dir/depend

