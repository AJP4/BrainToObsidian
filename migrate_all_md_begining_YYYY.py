import os
import shutil
import re


def move_numeric_files(source_dir, target_dir, extension):
    """
    Moves files with numeric filenames matching patterns "YYYY", "YYYY MM", "YYYY MM DD"
    from source_dir to target_dir. Only files with the specified extension are considered.
    If a file contains no text (empty or only whitespace), it is deleted instead of being moved.

    Args:
        source_dir (str): The source directory to search for files.
        target_dir (str): The target directory to move files to.
        extension (str): The file extension to filter by (e.g., 'md', 'jpg').

    Prints:
        The number of files searched, moved, and deleted.
    """
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Regex to match valid numeric date patterns: YYYY, YYYY MM, YYYY MM DD
    valid_date_pattern = re.compile(r"^\d{4}( \d{2})?( \d{2})?$")

    files_searched = 0
    files_moved = 0
    files_deleted = 0

    # Only process files in the source directory
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)

        # Check if it's a file and has the specified extension
        if os.path.isfile(file_path) and file.lower().endswith(f".{extension}"):
            files_searched += 1

            # Check if the filename matches the valid date pattern
            filename_without_extension = os.path.splitext(file)[0]
            if valid_date_pattern.match(filename_without_extension):
                # Check if the file contains text
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                    if content:  # File has text content
                        destination_path = os.path.join(target_dir, file)
                        try:
                            # Move the file to the target directory
                            shutil.move(file_path, destination_path)
                            files_moved += 1
                        except Exception as e:
                            print(f"Error moving file {file_path}: {e}")
                    else:  # File is empty or contains only whitespace
                        try:
                            os.remove(file_path)
                            files_deleted += 1
                        except Exception as e:
                            print(f"Error deleting file {file_path}: {e}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    # Print summary
    print(f"Files searched: {files_searched}")
    print(f"Files moved: {files_moved}")
    print(f"Files deleted: {files_deleted}")


# Example usage
if __name__ == "__main__":
    source_dir = "./obsidian"  # Replace with your actual source directory
    target_dir = "./obsidian/calendar"  # Replace with your actual target directory
    extension = "md"  # Replace with your desired file extension
    move_numeric_files(source_dir, target_dir, extension)
