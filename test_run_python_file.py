from functions.run_python_file import run_python_file

test_cases = [
("calculator", "main.py"),
("calculator", "main.py", ["3 + 5"]),
("calculator", "tests.py"),
("calculator", "../main.py"),
("calculator", "nonexistent.py"),
("calculator", "lorem.txt")
]

def main():
  for working_directory, file_path, *args in test_cases:
    result = run_python_file(working_directory, file_path, args[0] if len(args) > 0 else None)
    print(f"Result for running '{file_path}':\n{result}\n")

if __name__ == "__main__":
  main()