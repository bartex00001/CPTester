import time
import os
from trace import Trace


INPUT_FILES_PATH = "./tests/in/"
OUTPUT_FILES_PATH = "./tests/out/"
TEST_PREFIX = "sol"

IN_TEST_SUFIX = ".in"
OUT_TEST_SUFIX = ".out"

EXECUTABLE_PATH = "./sol.exe"

STOP_ON_FAIL = True


class Test:
    def __init__(self) -> None:
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

    def check_test(self, file_name: str) -> bool:
        pass
    
    def run_all_tests(self) -> None:
        pass


if __name__ == "__main__":
    pass