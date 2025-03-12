import os
import shutil

content_files = 0
files_to_remove = []

# First check all files
for file in os.listdir("stitch_functions"):
    file_path = os.path.join("stitch_functions", file)
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            if len(content) > 5:
                content_files += 1
            # Ad files with content length less than 5 to the files_to_remove list
            else:
                files_to_remove.append(file_path)
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Now remove the files with content length less than 5
for file_path in files_to_remove:
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error removing {file_path}: {e}")

print(f"Kept {content_files} files with content length > 5")
print(f"Removed {len(files_to_remove)} files with content length ≤ 5")