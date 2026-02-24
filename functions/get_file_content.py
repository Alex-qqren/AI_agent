import os
from config import *

def get_file_content(working_directory, file_path):
  try:
    working_directory_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([working_directory_abs, target_file_path]) != working_directory_abs:
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file_path, 'r') as f:
      content = f.read(MAX_CHARS)
      if f.read(1):
        content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    return content
      
  except Exception as e:
    return f"Error: {str(e)}"