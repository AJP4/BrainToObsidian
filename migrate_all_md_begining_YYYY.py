import os
import shutil
import re


def move_numeric_files(source_dir, target_dir, extension, target_empty_files_folder):
    """
    Processes files in the source_dir:
    - If the filename matches YYYY, YYYY MM, or YYYY MM DD and has content after the YAML frontmatter, move it to target_dir.
    - If the file is empty after the YAML frontmatter, delete it.
    - If the filename does not match YYYY, YYYY MM, or YYYY MM DD and is empty after the YAML frontmatter, move it to target_empty_files_folder.
    - Otherwise, leave the file where it is.

    Args:
        source_dir (str): The source directory to search for files.
        target_dir (str): The target directory to move files to.
        extension (str): The file extension to filter by (e.g., 'md', 'jpg').
        target_empty_files_folder (str): The folder to move files without content after YAML.

    Prints:
        The number of files searched, moved, deleted, and left untouched.
    """
    # Ensure the target directories exist
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(target_empty_files_folder, exist_ok=True)

    # Regex to match valid numeric date patterns: YYYY, YYYY MM, YYYY MM DD
    valid_date_pattern = re.compile(r"^\d{4}( \d{2})?( \d{2})?$")

    files_searched = 0
    files_moved = 0
    files_deleted = 0
    files_to_empty_folder = 0
    files_untouched = 0

    # Only process files in the source directory
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)

        # Check if it's a file and has the specified extension
        if os.path.isfile(file_path) and file.lower().endswith(f".{extension}"):
            files_searched += 1

            # Check if the filename matches the valid date pattern
            filename_without_extension = os.path.splitext(file)[0]
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Extract content after the YAML frontmatter
                inside_yaml = False
                content_after_yaml = []
                for line in lines:
                    if line.strip() == "---":
                        inside_yaml = not inside_yaml
                    elif not inside_yaml:
                        content_after_yaml.append(line.strip())

                # Determine the action to take
                if valid_date_pattern.match(filename_without_extension):
                    if any(content_after_yaml):  # File has content after YAML
                        destination_path = os.path.join(target_dir, file)
                        shutil.move(file_path, destination_path)
                        files_moved += 1
                    else:  # File is empty after YAML
                        os.remove(file_path)
                        files_deleted += 1
                else:
                    if not any(content_after_yaml):  # File is empty after YAML
                        destination_path = os.path.join(target_empty_files_folder, file)
                        shutil.move(file_path, destination_path)
                        files_to_empty_folder += 1
                    else:  # File has content, leave it untouched
                        files_untouched += 1
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    # Print summary
    print(f"Files searched: {files_searched}")
    print(f"Files moved to target_dir: {files_moved}")
    print(f"Files deleted: {files_deleted}")
    print(f"Files moved to empty files folder: {files_to_empty_folder}")
    print(f"Files left untouched: {files_untouched}")


# Example usage
if __name__ == "__main__":
    source_dir = "./obsidian"  # Replace with your actual source directory
    target_dir = "./obsidian/calendar"  # Replace with your actual target directory
    target_empty_files_folder = (
        "./obsidian/empty_files"  # Replace with your empty files folder
    )
    extension = "md"  # Replace with your desired file extension
    move_numeric_files(source_dir, target_dir, extension, target_empty_files_folder)
