import zipfile

# Path to the zip file
zip_path = 'archive.zip'

# Path to the directory to extract files to
extract_to = 'output_directory'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)