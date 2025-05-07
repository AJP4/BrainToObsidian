import os
import re
import logging


def convert_date_links_in_markdown(folder_path, test_mode=True):
    """
    Searches all markdown files in the specified folder for links in the format [[YYYY MM DD]]
    and converts them to [[YYYY-MM-DD]].

    Args:
        folder_path (str): The path to the folder containing markdown files.
        test_mode (bool): If True, only prints the proposed changes without modifying files.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("convert_date_links.log"),
            logging.StreamHandler(),
        ],
    )

    # Regex pattern to match [[YYYY MM DD]] links
    date_link_pattern = re.compile(r"\[\[(\d{4}) (\d{2}) (\d{2})\]\]")

    logging.info(f"Starting date link conversion in folder: {folder_path}")
    logging.info(f"Test mode is {'ON' if test_mode else 'OFF'}")

    # Iterate through all markdown files in the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):  # Process only markdown files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Replace [[YYYY MM DD]] with [[YYYY-MM-DD]]
                    updated_content = date_link_pattern.sub(
                        lambda match: f"[[{match.group(1)}-{match.group(2)}-{match.group(3)}]]",
                        content,
                    )

                    if updated_content != content:
                        if test_mode:
                            logging.info(f"Test: Would update links in '{file_path}'")
                        else:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(updated_content)
                            logging.info(f"Updated links in '{file_path}'")

                except Exception as e:
                    logging.error(f"Failed to process file '{file_path}': {e}")

    logging.info("Date link conversion process completed.")


# Example usage
if __name__ == "__main__":
    # Specify the folder containing markdown files
    folder_path = "E:/Brains/Dad/files"  # Replace with your actual folder path

    # Set test_mode to True to preview changes without modifying files
    test_mode = False

    convert_date_links_in_markdown(folder_path, test_mode)
