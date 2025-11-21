import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    
    #paths
    full_path = os.path.join(working_directory, file_path)
    full_path_abspath = os.path.abspath(full_path)
    working_directory_abspath = os.path.abspath(working_directory)

    #Making sure LLM has some guardrails: we never want it to be able to perform any work outside the "working_directory" we give it.
    if full_path_abspath.startswith(working_directory_abspath):
        
        if not os.path.isfile(full_path_abspath):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        try:
            with open(full_path_abspath, "r") as f:
                file_content_string = f.read()
            
                if len(file_content_string) > MAX_CHARS:
                    truncated_file_content_string = file_content_string[:MAX_CHARS]
                    return truncated_file_content_string + (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
                
                return file_content_string
        
        except Exception as e:
            return f"Error: {e}"

    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'