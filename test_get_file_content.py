from functions.get_file_content import get_file_content

test_cases = [
  ("calculator", "main.py"),
  ("calculator", "pkg/calculator.py"),
  ("calculator", "/bin/cat"),
  ("calculator", "pkg/does_not_exist.py"),
]

def main():
  # Test with various file paths
  for working_directory, file_path in test_cases:
    result = get_file_content(working_directory, file_path)
    print(f"Result for '{file_path}':\n{result}\n")

if __name__ == "__main__":
    main()