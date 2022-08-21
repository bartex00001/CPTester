import time
import os
from pathlib import Path


INPUT_FILES_PATH = "./tests/in/"
OUTPUT_FILES_PATH = "./tests/out/"
TEST_PREFIX = "sol"

IN_TEST_SUFIX = ".in"
OUT_TEST_SUFIX = ".out"

EXECUTABLE_PATH = "./sol.exe"

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
        output_file = Path(OUTPUT_FILES_PATH + output_file_name)
        return os.path.isfile(output_file)
            

    def __init__(self, input_file_name) -> None:
        pass

    def run_test(self) -> bool:
        pass


class Tester:
    def __init__(self) -> None:
        pass

    def add_all_tests(self) -> None:
        # listdir() to get all elements in a directory
        # to check if element is a file isfile(path_to_file)
        pass
    
    def add_test(self, input_file_name: str) -> None:
        pass

    def run_all_tests(self) -> None:
        pass


if __name__ == "__main__":
    print(Test.is_valid_test("sol001.out"))