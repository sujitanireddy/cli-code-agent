import os

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)
    full_path_abspath = os.path.abspath(full_path)
    working_directory_abspath = os.path.abspath(working_directory)

    #Making sure LLM has some guardrails: we never want it to be able to perform any work outside the "working_directory" we give it.
    if full_path_abspath.startswith(working_directory_abspath):

        if not os.path.isdir(full_path_abspath):
            return f'Error: "{directory}" is not a directory'

        try:
            dir_list = os.listdir(full_path_abspath)

            lines = []

            for item in dir_list:
                item_path = os.path.join(full_path_abspath, item)
                lines.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"Error: {e}"
          
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'