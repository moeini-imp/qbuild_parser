import unittest
import os
import sys

def extract_tests(test_suite_or_case):
    test_names = []
    for test in test_suite_or_case:
        if isinstance(test, unittest.TestCase):
            # Split the full name and take the last part
            test_name_parts = test.id().split('.')
            test_names.append(test_name_parts[-1])
        elif isinstance(test, unittest.TestSuite):
            # Recursively extract test names from nested suites
            nested_test_names, _ = extract_tests(test)
            test_names.extend(nested_test_names)

    num_tests = len(test_names)
    return test_names, num_tests

def load_tests_from_file(file_path):
    # Dynamically load tests from a specified file
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(file_path), pattern=os.path.basename(file_path))
    return suite

def discover_and_analyze_tests(start_dir="."):
    test_patterns = ["test.py", "tests/test.py", "test_*.py", "tests/test_*.py"]
    
    discovered_tests = []
    for pattern in test_patterns:
        if "tests/" in pattern:
            folder_path, file_pattern = pattern.split("/")
            file_path = os.path.join(folder_path, file_pattern)
            
            # Adjust the Python path temporarily to include the tests folder
            sys.path.append(folder_path)
            
            try:
                suite = load_tests_from_file(file_path)
            finally:
                # Remove the temporary path modification
                sys.path.remove(folder_path)
        else:
            suite = unittest.defaultTestLoader.discover(start_dir, pattern=pattern)
            
        print(f"Discovered Test Files using pattern '{pattern}':")
        for test in suite:
            print(test)
        discovered_tests.extend(suite)

    combined_suite = unittest.TestSuite(discovered_tests)
    
    test_names, num_tests = extract_tests(combined_suite)
    return test_names, num_tests

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    test_names, num_tests = discover_and_analyze_tests(current_dir)

    print("\nTest Names:")
    for name in test_names:
        print(name)

    print("\nNumber of Tests:", num_tests)
