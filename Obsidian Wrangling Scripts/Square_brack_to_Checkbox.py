# This has already been implemented in migration_functions.py

import os
import re
import logging


def replace_checkboxes_in_markdown(folder_path, test_mode=True):
    """
    Searches all markdown files in the specified folder and subfolders for lines starting with "[ ]"
    and replaces them with "- [ ]".

    Args:
        folder_path (str): The path to the folder containing markdown files.
        test_mode (bool): If True, only prints the proposed changes without modifying files.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("replace_checkboxes.log"),
            logging.StreamHandler(),
        ],
    )

    # Regex pattern to match lines starting with "[ ]"
    checkbox_pattern = re.compile(r"^\[ \]")

    logging.info(f"Starting checkbox replacement in folder: {folder_path}")
    logging.info(f"Test mode is {'ON' if test_mode else 'OFF'}")

    # Iterate through all markdown files in the folder and subfolders
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):  # Process only markdown files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    modified = False
                    updated_lines = []

                    for line in lines:
                        if checkbox_pattern.match(
                            line
                        ):  # Match lines starting with "[ ]"
                            updated_lines.append(line.replace("[ ]", "- [ ]", 1))
                            modified = True
                        else:
                            updated_lines.append(line)

                    if modified:
                        if test_mode:
                            logging.info(
                                f"Test: Would update checkboxes in '{file_path}'"
                            )
                        else:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.writelines(updated_lines)
                            logging.info(f"Updated checkboxes in '{file_path}'")

                except Exception as e:
                    logging.error(f"Failed to process file '{file_path}': {e}")

    logging.info("Checkbox replacement process completed.")


# Example usage below
if __name__ == "__main__":
    # Specify the folder containing markdown files
    folder_path = "./obsidian"  # Replace with your actual folder path

    # Set test_mode to True to preview changes without modifying files
    test_mode = False

    replace_checkboxes_in_markdown(folder_path, test_mode)
