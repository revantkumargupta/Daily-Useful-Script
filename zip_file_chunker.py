import zipfile
import os

# Path to the ZIP file
zip_file_path = "" #put filename or path here

# Check the number of files and total size
file_list = []

with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    for zip_info in zip_file.infolist():
        file_list.append((zip_info.filename, zip_info.file_size))

# Split files into 50GB chunks
chunk_size = 50 * (1024 ** 3)  # 50GB in bytes
chunks = []
current_chunk = []
current_size = 0

for filename, filesize in file_list:
    if current_size + filesize > chunk_size and current_chunk:
        chunks.append(current_chunk)
        current_chunk = []
        current_size = 0
    current_chunk.append((filename, filesize))
    current_size += filesize

if current_chunk:
    chunks.append(current_chunk)

# Prompt user to select a chunk
print(f"\nTotal number of chunks: {len(chunks)}")
print("Select a chunk to extract:")
for i in range(len(chunks)):
    print(f"{i + 1}: {len(chunks[i])} files, {sum(f[1] for f in chunks[i]) / (1024 ** 3):.2f} GB")

selection = int(input("Enter your choice (1, 2, 3, ...): ")) - 1

# Create a folder for the selected chunk and extract files
if 0 <= selection < len(chunks):
    folder_name = f"{selection + 1}"
    os.makedirs(folder_name, exist_ok=True)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for filename, filesize in chunks[selection]:
            zip_file.extract(filename, path=folder_name)
            print(f"Extracted: {filename}")
else:
    print("Invalid selection. Exiting.")


