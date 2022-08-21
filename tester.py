from genericpath import isfile
import time
from os import system
from os import remove
from os import listdir
from os import path

# Time taken is an aproximation.
TIME_LIMIT_S = 1
INPUT_FILES_FOLDER = "tests/in/"
OUTPUT_FILES_FOLDER = "tests/out/"
TEST_PREFIX = "sol"

IN_TEST_SUFIX = ".in"
OUT_TEST_SUFIX = ".out"

EXECUTABLE_PATH = "sol.exe"
# Leave empty if you want to compile the executable manually
SOURCE_PATH = "sol.cpp"
COMPILE_COMMAND = "g++ -std=c++17 -O2 -o"
ALWAYS_COMPILE = False

STOP_ON_FAIL = True
SHOW_FILE_DIFF = True
TRIM = 15


# Custom checker can be defined here.
# Test runner takes `or` of answer_checker and program_output==file_output
def answer_checker(input_file: str, program_output_file: str) -> bool: 
    return False


class Colors:
    RED = "1;31;40"
    M_RED = "0;30;41"
    GREEN = "1;32;40"
    M_GREEN = "0;30;42"

    [staticmethod]
    def add_color(text: str, color_code: str) -> str:
        return "\x1b[" + color_code + "m" + text + "\x1b[0m"

class Test:
    TEMP_OUT_FILE_NAME = "temp.out"

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
        return path.isfile(output_file_path)
            

    def __init__(self, input_file_name) -> None:
        self.input_file_path = INPUT_FILES_FOLDER + input_file_name
        self.output_file_path = OUTPUT_FILES_FOLDER + input_file_name.replace(IN_TEST_SUFIX, OUT_TEST_SUFIX)
        self.test_output_path = OUTPUT_FILES_FOLDER + Test.TEMP_OUT_FILE_NAME

        self.test_name = input_file_name.replace(IN_TEST_SUFIX, "")
        self.command = EXECUTABLE_PATH + " < " + self.input_file_path + " > " + self.test_output_path


    def run_test(self) -> bool:
        start_time = time.time()
        system(self.command)
        end_time = time.time()

        time_elapsed = max(round(end_time - start_time, 3)-0.05, 0)
        if time_elapsed > TIME_LIMIT_S:
            self.tle_message(time_elapsed)
            return False

        if not self.check_output() and not answer_checker(self.input_file_path, self.test_output_path):
            self.print_wa()
            if SHOW_FILE_DIFF:
                self.print_diff()
            
            return False

        print(Colors.add_color("✅ Test " + self.test_name + " passed in " + str(time_elapsed) + " s", Colors.GREEN))
        return True

    
    def check_output(self) -> bool:
        expected = ""
        actual = ""

        with open(self.output_file_path, "r") as file:
            expected = file.read().strip()
        
        with open(self.test_output_path, "r") as file:
            actual = file.read().strip()

        return expected == actual

    
    def print_wa(self) -> None:
        print(Colors.add_color("❌ ❌ Test " + self.test_name + " failed - wrong answer", Colors.RED))
        print(Colors.add_color("❌ ❌ The input file was: " + self.input_file_path, Colors.RED))
        print("Input file contents: ")
        Test.print_file(self.input_file_path)
        

    def tle_message(self, time_elapsed: float) -> None:
        print(Colors.add_color("❌ 🕘 Test " + self.test_name + " timed out in " + str(time_elapsed) + " s", Colors.RED))
        print(Colors.add_color("❌ 🕘 The input file was: " + self.input_file_path, Colors.RED))


    def print_diff(self) -> None:
        with open(self.output_file_path, "r") as file:
            expected = file.readlines()
        
        with open(self.test_output_path, "r") as file:
            actual = file.readlines()

        print("\nDifferences in output:")
        lines_to_show = min(min(len(expected), len(actual)), TRIM)
        for i in range(lines_to_show):
            Test.print_line_diff(expected[i], actual[i], i+1)

        if len(expected) > len(actual):
            print("\n" + Colors.add_color("❌ ❌ The output has more lines than the expected output", Colors.RED))
        if len(expected) < len(actual):
            print("\n" + Colors.add_color("❌ ❌ The output has less lines than the expected output", Colors.RED))

    
    def print_line_diff(line_expected: str, line_actual: str, line_nr: int) -> None:    
        correct_line = str(line_nr) + "\t| "
        incorrect_line = "\t| "

        line_expected = line_expected.strip()
        line_actual = line_actual.strip()

        if line_expected == line_actual:
            print(correct_line + line_expected)
            return

        (line_expected, line_actual) = Test.fill_minning_length(line_expected, line_actual)

        for i in range(len(line_actual)):
            if line_expected[i] == line_actual[i]:
                correct_line += Colors.add_color(line_expected[i], Colors.GREEN)
                incorrect_line += Colors.add_color(line_actual[i], Colors.RED)
            else:
                correct_line += Colors.add_color(line_expected[i], Colors.M_GREEN)
                incorrect_line += Colors.add_color(line_actual[i], Colors.M_RED)

        print("-"*50)
        print(correct_line)
        print(incorrect_line)

    
    [staticmethod]
    def fill_minning_length(line_expected: str, line_actual: str):
        if len(line_expected) < len(line_actual):
            line_expected += " " * (len(line_actual) - len(line_expected))
        elif len(line_expected) > len(line_actual):
            line_actual += " " * (len(line_expected) - len(line_actual))

        return (line_expected, line_actual)


    [staticmethod]
    def print_file(file_path: str) -> None:
        with open(file_path, "r") as file:
            contents = file.readlines()
            for i in range(min(len(contents), TRIM)):
                print(str(i+1) + "\t| " + contents[i].strip())

            if len(contents) > TRIM:
                print("...")
                print("Rest of the file can be found in " + file_path + "\n")


class Tester:
    def __init__(self) -> None:
        self.tests = []
        self.check_executable() # return path or create one.


    def check_executable(self) -> None:
        if EXECUTABLE_PATH == "":
            raise Exception("No executable path specified")

        should_compile = ALWAYS_COMPILE or not path.isfile(EXECUTABLE_PATH)

        if should_compile:
            self.compile_executable()
        
    
    def compile_executable(self) -> None:
        if SOURCE_PATH == "":
            raise Exception("No source code path specified - it is required to compile the executable.\nIf you do not want to compile the executable, check your settings.")

        if path.isfile(EXECUTABLE_PATH):
            remove(EXECUTABLE_PATH)

        system(COMPILE_COMMAND + " " + EXECUTABLE_PATH + " " + SOURCE_PATH)
        print("Source compiled to " + EXECUTABLE_PATH)


    def add_all_tests(self) -> int:
        for element in listdir(INPUT_FILES_FOLDER):
            file_with_path = INPUT_FILES_FOLDER + element
            if path.isfile(file_with_path):
                self.add_test(element)

        print("Tests found: " + str(len(self.tests)))
        return len(self.tests)


    def add_test(self, input_file_name: str) -> None:
        if Test.is_valid_test(input_file_name):
            self.tests.append(Test(input_file_name))


    def run_all_tests(self) -> int:
        correct_tests = 0

        for test in self.tests:
            result = test.run_test()
            correct_tests += result
            if not result and STOP_ON_FAIL:
                break

        return correct_tests
        

if __name__ == "__main__":
    tester = Tester()
    test_num = tester.add_all_tests()
    success_tests = tester.run_all_tests()

    # Remove the temporary files
    if path.isfile(OUTPUT_FILES_FOLDER + Test.TEMP_OUT_FILE_NAME):
        remove(OUTPUT_FILES_FOLDER + Test.TEMP_OUT_FILE_NAME)

    if success_tests != 0:
        if test_num == success_tests:
            print(Colors.add_color("\n✅ All tests passed ✅", Colors.GREEN))
        else:
            print(Colors.add_color("\n❌ Percentage of tests passed: " + str(round(success_tests*100 / test_num, 2)) + "% ❌", Colors.RED))
