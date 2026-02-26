import os
from google.genai import types

def write_file(working_directory, file_path, content):
  try:
    working_directory_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.commonpath([working_directory_abs, target_file_path]) != working_directory_abs:
      return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file_path):
      return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    with open(target_file_path, 'w') as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f"Error: {str(e)}"
  

schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Writes content to a specified file relative to the working directory, creating any necessary directories. Overwrites existing files.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Path of the file to write to relative to the working directory."
      ),
      "content": types.Schema(
        type=types.Type.STRING,
        description="Content to write into the file."
      )
    },
    required=["file_path", "content"]
  )
)