import qtest_parser
import os
import json
import argparse

def get_test_info(project_path):
    test_names = qtest_parser.test_names
    num_tests = len(test_names)
    return test_names, num_tests

def create_tester_config():
    parser = argparse.ArgumentParser(description='Create tester_config.json for a project.')

    # Step 1: Get the path to the project folder
    parser.add_argument('project_path', type=str, help='Path to the project folder')

    # Step 2: Get the Python version
    parser.add_argument('--python_version', choices=['3.9', '3.10', '3.11', '3.12'], required=True,
                        help='Choose Python version (3.9 to 3.12)')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Use args.project_path as the project path
    project_path = os.path.abspath(args.project_path)

    # Step 3: Show files in the project folder
    files = [f for f in os.listdir(project_path) if os.path.isfile(os.path.join(project_path, f))]
    
    print('Files in the project folder:')
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    # Step 4: Get the solution signature
    solution_signature = input("\nEnter the solution signature path or file name: ")

    # Step 5: Add the number of tests
    test_names, num_tests = get_test_info(project_path)
    print(f"\nNumber of Tests: {num_tests}")

    # Step 6: Write the package parts
    packages = []
    for test_name in test_names:
        score = float(input(f"Enter score for {test_name}: "))
        
        use_aggregator = input(f"Use aggregator for {test_name}? (yes/no): ").lower() == 'yes'
        aggregator = input(f"Choose aggregator for {test_name} (sum/divide/multiply): ") if use_aggregator else None
        
        package = {
            "name": test_name,
            "score": score,
            "tests": [test_name],
        }
        if use_aggregator:
            package["aggregator"] = aggregator
        
        packages.append(package)

    # Step 7: Add can_submit_single_file option
    can_submit_single_file = input("Add can_submit_single_file option (true/false): ").lower() == 'true'
    
    # Step 8: If can_submit_single_file is true, add single_file_path and solution file path
    single_file_path = ""
    solution_file_path = ""
    if can_submit_single_file:
        single_file_path = input("Enter single_file_path: ")
        solution_file_path = input("Enter solution file path: ")

    # Step 9: Get the content of the valid_files file
    valid_files_content = []
    print("\nEnter the content of valid_files. Type 'end' on a new line to finish:")
    while True:
        line = input()
        if line.lower() == 'end':
            break
        valid_files_content.append(line)

    # Step 10: Create the tester_config dictionary
    tester_config = {
        "version": 2,
        "solution_signature": solution_signature,
        "number_of_tests": num_tests,
    }

    # Add can_submit_single_file and single_file_path only if true
    if can_submit_single_file:
        tester_config["can_submit_single_file"] = True
        tester_config["single_file_path"] = single_file_path
        tester_config["solution_file_path"] = solution_file_path

    # Step 11: Write the tester_config.json file
    tester_config_path = os.path.join(project_path, 'tester_config.json')
    with open(tester_config_path, 'w') as json_file:
        json.dump(tester_config, json_file, indent=2)

    # Step 12: Write the valid_files file
    valid_files_path = os.path.join(project_path, 'valid_files')
    with open(valid_files_path, 'w') as valid_files_file:
        valid_files_file.write('\n'.join(valid_files_content))

    # Step 13: Add the package parts to the tester_config dictionary
    tester_config["packages"] = packages

    # Step 14: Write the tester_config.json file
    tester_config_path = os.path.join(project_path, 'tester_config.json')
    with open(tester_config_path, 'w') as json_file:
        json.dump(tester_config, json_file, indent=2)

    # Step 15: Write the valid_files file
    valid_files_path = os.path.join(project_path, 'valid_files')
    with open(valid_files_path, 'w') as valid_files_file:
        valid_files_file.write('\n'.join(valid_files_content))

    print("\nTester configuration and valid_files created successfully!")
if __name__ == '__main__':
    create_tester_config()