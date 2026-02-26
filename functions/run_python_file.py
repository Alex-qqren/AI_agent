import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
  try:
    working_directory_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([working_directory_abs, target_file_path]) != working_directory_abs:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
      return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file_path.endswith('.py'):
      return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file_path]
    
    if args:
      command.extend(args)

    sub_process_result = subprocess.run(
      command, 
      cwd=working_directory_abs, 
      capture_output=True,
      text=True, 
      timeout=30
      )

    output_string = []
    if sub_process_result.returncode != 0:
      output_string.append(f"Process exited with code {sub_process_result.returncode}")
    if not sub_process_result.stderr and not sub_process_result.stdout:
      output_string.append("No output produced")
    if sub_process_result.stdout:
      output_string.append(f"STDOUT:\n{sub_process_result.stdout}")
    if sub_process_result.stderr:
      output_string.append(f"STDERR:\n{sub_process_result.stderr}")
    return "\n".join(output_string)

  except Exception as e:
    return f"Error: executing Python file: {e}"
  