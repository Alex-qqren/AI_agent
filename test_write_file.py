from functions.write_file import write_file

test_cases = [
  ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
  ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
  ("calculator", "/tmp/temp.txt", "this should not be allowed")
]

def main():
  for working_directory, file_path, content in test_cases:
    result = write_file(working_directory, file_path, content)
    print(f"Result for writing to '{file_path}':\n{result}\n")

if __name__ == "__main__":
  main()
