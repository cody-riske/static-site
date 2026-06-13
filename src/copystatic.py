import os
import shutil

def copy_directory_recursive(source_dir, dest_dir):
    """
    Recursively copies all contents from source_dir to dest_dir.
    Cleans the dest_dir before starting if it is the top-level call.
    """
    # Delete destination directory if it exists to ensure a clean copy
    if os.path.exists(dest_dir):
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
        
    # Recreate the clean destination directory
    os.mkdir(dest_dir)

    # Iterate through all items in the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            # Log and copy the file
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            # Log and recursively handle the subdirectory
            print(f"Creating directory: {dest_path}")
            copy_directory_recursive(source_path, dest_path)
