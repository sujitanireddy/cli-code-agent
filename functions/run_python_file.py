import os
import subprocess

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
