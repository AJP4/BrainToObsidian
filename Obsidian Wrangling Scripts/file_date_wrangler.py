import os
import re
import logging


def rename_files_to_iso8601(directory, test_mode=True):
    """
    Renames files in the specified directory to follow the ISO 8601 date format (YYYY-MM or YYYY-MM-DD).

    Args:
        directory (str): The path to the directory containing the files to rename.
        test_mode (bool): If True, only prints the proposed changes without renaming files.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("rename_files_to_iso8601.log"),
            logging.StreamHandler(),
        ],
    )

    # Regex patterns for matching date formats
    patterns = [
        (
            re.compile(r"^(\d{4}) (\d{2}) (\d{2})(.*)$"),
            r"\1-\2-\3\4",
        ),  # YYYY MM DD -> YYYY-MM-DD
        (re.compile(r"^(\d{4}) (\d{2})(.*)$"), r"\1-\2\3"),  # YYYY MM -> YYYY-MM
    ]

    logging.info(f"Starting file renaming in directory: {directory}")
    logging.info(f"Test mode is {'ON' if test_mode else 'OFF'}")

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        original_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(original_path):
            continue

        new_filename = filename
        for pattern, replacement in patterns:
            new_filename = pattern.sub(replacement, new_filename)
            if new_filename != filename:
                break  # Stop after the first successful match

        if new_filename != filename:
            new_path = os.path.join(directory, new_filename)
            if test_mode:
                logging.info(f"Test: Would rename '{original_path}' to '{new_path}'")
            else:
                try:
                    os.rename(original_path, new_path)
                    logging.info(f"Renamed '{original_path}' to '{new_path}'")
                except Exception as e:
                    logging.error(f"Failed to rename '{original_path}': {e}")

    logging.info("File renaming process completed.")


# Example usage
if __name__ == "__main__":
    # Specify the directory containing the files to rename
    directory = "E:/Brains/Dad/calendar"  # Replace with your actual directory path

    # Set test_mode to True to preview changes without renaming files
    test_mode = False

    rename_files_to_iso8601(directory, test_mode)
