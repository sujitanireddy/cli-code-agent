import os

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