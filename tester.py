from enum import Flag
import time
import os
from pathlib import Path


INPUT_FILES_FOLDER = "./tests/in/"
OUTPUT_FILES_FOLDER = "./tests/out/"
TEST_PREFIX = "sol"

IN_TEST_SUFIX = ".in"
OUT_TEST_SUFIX = ".out"

EXECUTABLE_PATH = "./sol.exe"
# Leave empty if you want to compile the executable manually
SOURCE_PATH = "sol.cpp"
COMPILE_COMMAND = "g++ -std=c++17 -O2 -o"
ALWAYS_COMPILE = False

STOP_ON_FAIL = True


class Test:
    [staticmethod]
    def is_valid_test(input_file_name: str) -> bool:
        output_file_name = input_file_name.replace(IN_TEST_SUFIX, OUT_TEST_SUFIX)
        valid_input = Test.is_valid_input(input_file_name)
        valid_output = Test.is_valid_output(output_file_name)

        return valid_input and valid_output


    [staticmethod]
    def is_valid_input(input_file_name: str) -> bool:
        valid_sufix =  IN_TEST_SUFIX in input_file_name
        valid_prefix = TEST_PREFIX in input_file_name

        return valid_sufix and valid_prefix


    [staticmethod]
    def is_valid_output(output_file_name: str) -> bool:
        output_file_path = OUTPUT_FILES_FOLDER + output_file_name
        return os.path.isfile(output_file_path)
            

    def __init__(self, input_file_name) -> None:
        pass


    def run_test(self) -> bool:
        pass


class Tester:
    def __init__(self) -> None:
        self.tests = []
        self.check_executable() # return path or create one.


    def check_executable(self) -> None:
        if EXECUTABLE_PATH == "":
            raise Exception("No executable path specified")

        should_compile = ALWAYS_COMPILE or not os.path.isfile(EXECUTABLE_PATH)

        if should_compile:
            self.compile_executable()
        
    
    def compile_executable(self) -> None:
        if SOURCE_PATH == "":
            raise Exception("No source code path specified - it is required to compile the executable.\nIf you do not want to compile the executable, check your settings.")

        if os.path.isfile(EXECUTABLE_PATH):
            os.remove(EXECUTABLE_PATH)

        os.system(COMPILE_COMMAND + " " + EXECUTABLE_PATH + " " + SOURCE_PATH)
        print("Source compiled to " + EXECUTABLE_PATH)


    def add_all_tests(self) -> None:
        for element in os.listdir(INPUT_FILES_FOLDER):
            file_with_path = INPUT_FILES_FOLDER + element
            if os.path.isfile(file_with_path):
                self.add_test(element)


    def add_test(self, input_file_name: str) -> None:
        if Test.is_valid_test(input_file_name):
            self.tests.append(Test(input_file_name))
            print("Added test: " + input_file_name)


    def run_all_tests(self) -> None:
        pass


if __name__ == "__main__":
    tester = Tester()
