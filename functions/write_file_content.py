import os
from google.genai import types

def write_file(working_directory, file_path, content):
    
    #paths
    full_path = os.path.join(working_directory, file_path)
    full_path_abspath = os.path.abspath(full_path)
    working_directory_abspath = os.path.abspath(working_directory)

    #Making sure LLM has some guardrails: we never want it to be able to perform any work outside the "working_directory" we give it.
    if full_path_abspath.startswith(working_directory_abspath):
        try:

            #extracting directory name from the full file path
            dir_name = os.path.dirname(full_path_abspath)
            os.makedirs(dir_name, exist_ok=True)
            
            with open(full_path_abspath, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
        except Exception as e:
            return f"Error: {e}"

    else:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    

#tells the LLM how to use the above function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes text content to a file within a restricted working directory. "
        "Ensures the target path is inside the given working_directory, creates "
        "any missing parent directories, and overwrites the file with the "
        "provided content. Returns a success message with the number of "
        "characters written, or an error message if validation or writing fails."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Base directory that defines the allowed sandbox. The "
                    "target file must reside within this directory."
                ),
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to write, relative to working_directory "
                    "or an absolute path that still lies under it."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["working_directory", "file_path", "content"],
    ),
)