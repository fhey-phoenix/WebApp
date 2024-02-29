import os
import subprocess
from zipfile import ZipFile

def create_zipfile(zip_filename, source_folders, source_files):
    # Delete the zip file if it exists
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print(f"Deleted existing zip file: {zip_filename}")

    # Create a new zip file
    with ZipFile(zip_filename, 'w') as zipf:
        # Add specific folders to the zip file
        for folder in source_folders:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path))

        # Add specific files to the zip file
        for file in source_files:
            zipf.write(file, os.path.basename(file))

    print(f"Zip file created successfully: {zip_filename}")

# Specify the name of the new zip file
new_zip_filename = 'wa-phx-01.zip'

# Specify the folders and files to include in the zip file
folders_to_include = ['config','handlers','utils', 'privategpt']
files_to_include = ['app.py',
                    'requirements.txt']

print("Zipping files...")
# Call the function to create the new zip file
create_zipfile(new_zip_filename, folders_to_include, files_to_include)
print("Zipping complete")

print("Deploying to Azure...")
command_to_run = 'az webapp deployment source config-zip -g rg-managed-phx -n wa-phx-01 --src wa-phx-01.zip --verbose'
# Run the command'

subprocess.run(command_to_run, shell=True)
