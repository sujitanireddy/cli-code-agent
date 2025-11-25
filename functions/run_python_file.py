import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    
    #paths
    full_path = os.path.join(working_directory, file_path)
    full_path_abspath = os.path.abspath(full_path)
    working_directory_abspath = os.path.abspath(working_directory)

    #Making sure LLM has some guardrails: we never want it to be able to perform any work outside the "working_directory" we give it.
    common = os.path.commonpath([working_directory_abspath, full_path_abspath])

    if common != working_directory_abspath:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path_abspath):
        return f'Error: File "{file_path}" not found.'
        
    if not full_path_abspath.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
        
    #preparing the args for passing into subprocess function
    cmd = ["python3", full_path_abspath]
    for arg in args:
        cmd.append(arg)

    try:
        completed_process = subprocess.run(cmd, cwd=working_directory, timeout=30, capture_output=True, text=True)

        if completed_process.stdout.strip() == '' and completed_process.stderr.strip() == '':
            return "No output produced."

        result_string = f'STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}'
            
        if completed_process.returncode != 0:
            result_string += f" Process exited with code {completed_process.returncode}"
            return result_string
        
        return result_string

    except Exception as e:
        return f"Error: executing Python file: {e}" 


#tells the LLM how to use the above function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Safely executes a Python file within a restricted working directory. "
        "Verifies that the target file is inside the given working_directory, "
        "exists, and has a .py extension, then runs it with optional "
        "command-line arguments using python3. Returns a combined string "
        "containing STDOUT and STDERR, or a clear error message if execution "
        "fails, the file is invalid, or no output is produced."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Absolute or relative path to the directory that defines "
                    "the allowed execution sandbox. The script must reside "
                    "within this directory."
                ),
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the Python file to execute, relative to the "
                    "working_directory (or an absolute path that still lies "
                    "inside it)."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of command-line argument strings to pass "
                    "to the Python script."
                ),
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["working_directory", "file_path"],
    ),
)