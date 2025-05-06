import os
import shutil
import logging
import json
from datetime import datetime


def remove_invalid_character(text_string, replace_character, invalid_characters):
    """
    A utility function to remove invalid characters from a string
    and clean up leading and trailing spaces.

    Args:
        text_string (str): The input string to process.
        replace_character (str): The character to replace invalid characters with.
        invalid_characters (list): A list of characters to remove or replace.

    Returns:
        str: The cleaned string with invalid characters replaced and spaces trimmed.
    """
    if not isinstance(text_string, str):
        raise ValueError("Input must be a string")

    # Replace invalid characters
    for char in invalid_characters:
        text_string = text_string.replace(char, replace_character)

    # Remove both leading and trailing spaces
    return text_string.strip()


def clear_folder(folder_path, exclude_list=None):
    """
    A utility function to check if a folder has content and delete the content if it exists,
    while excluding specified files or folders.

    Args:
        folder_path (str): The path to the folder to clear.
        exclude_list (list): A list of file or folder names to exclude from deletion.
    """
    if exclude_list is None:
        exclude_list = []

    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            if item in exclude_list:
                logging.info(f"Skipped deletion of excluded item: {item}")
                continue

            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    # logging.info(f"Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    # logging.info(f"Deleted folder: {item_path}")
            except Exception as e:
                logging.error(f"Failed to delete {item_path}. Error: {e}")
        logging.info(
            f"Cleared content of folder: {folder_path}, excluding: {exclude_list}"
        )
    else:
        logging.info(
            f"Folder did not exist: {folder_path}. It will be created if needed."
        )


def Serialise_TBjson_files(input_files, output_directory):
    """
    Converts pseudo-JSON files to properly formatted JSON arrays and saves them to the output directory.

    Args:
        input_files (list): List of input file paths.
        output_directory (str): Path to the output directory.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process each input file
    for input_file_path in input_files:
        try:
            # Extract the original filename and prepend "TB_Refactored_"
            original_filename = os.path.basename(input_file_path)
            output_file_name = f"TB_Refactored_{original_filename}"
            output_file_path = os.path.join(output_directory, output_file_name)

            # Read the pseudo-JSON file and convert it to a proper JSON array
            with open(
                input_file_path, "r", encoding="utf-8-sig"
            ) as infile:  # Handle BOM
                lines = infile.readlines()
                json_data = [json.loads(line) for line in lines]

            # Write the properly formatted JSON array to the output file
            with open(output_file_path, "w", encoding="utf-8") as outfile:
                json.dump(json_data, outfile, indent=4)

            print(f"Converted JSON saved to: {output_file_path}")
        except Exception as e:
            print(f"An error occurred while processing {input_file_path}: {e}")


def ensure_directories_exist(base_directory, subdirectories):
    """
    Ensure that a list of subdirectories exists within a base directory.
    If a subdirectory does not exist, it is created.

    Args:
        base_directory (str): The base directory where subdirectories will be created.
        subdirectories (list): A list of subdirectory paths (relative to the base directory).

    Returns:
        None
    """
    for subdirectory in subdirectories:
        directory_path = os.path.join(base_directory, subdirectory)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logging.info(f"Created directory: {directory_path}")


def process_exported_attachments(source_dir, dest_documents, dest_images, dest_folders):
    """
    Process exported files and organize them into specified directories.

    Args:
        source_dir (str): The source directory containing exported files.
        dest_documents (str): Destination directory for documents.
        dest_images (str): Destination directory for embedded images.
        dest_folders (str): Destination directory for document folders.
    """
    # Traverse the first-level subfolders in the source directory
    for root, dirs, files in os.walk(source_dir):
        # Only process the first-level subfolders
        if root == source_dir:
            for dir_name in dirs:
                first_level_dir_path = os.path.join(root, dir_name)

                # Process files in the first-level subfolder
                for file in os.listdir(first_level_dir_path):
                    file_path = os.path.join(first_level_dir_path, file)
                    if os.path.isfile(file_path):
                        try:
                            # Skip "Notes.md" files
                            if file.lower() == "notes.md":
                                logging.info(f"Skipped file: {file_path}")
                                continue

                            # Copy files to "data/documents"
                            shutil.copy(file_path, dest_documents)
                            logging.info(
                                f"Copied file: {file_path} to {dest_documents}"
                            )
                        except Exception as e:
                            logging.error(
                                f"Failed to copy file: {file_path}. Error: {e}"
                            )

                # Process subfolders within the first-level subfolder
                for sub_dir_name in os.listdir(first_level_dir_path):
                    sub_dir_path = os.path.join(first_level_dir_path, sub_dir_name)
                    if os.path.isdir(sub_dir_path):
                        try:
                            # Check if the folder is ".data" and contains "md-images"
                            if sub_dir_name == ".data":
                                md_images_path = os.path.join(sub_dir_path, "md-images")
                                if os.path.exists(md_images_path) and os.path.isdir(
                                    md_images_path
                                ):
                                    # Copy files from ".data/md-images" to "data/embedded images"
                                    for image_file in os.listdir(md_images_path):
                                        image_file_path = os.path.join(
                                            md_images_path, image_file
                                        )
                                        if os.path.isfile(image_file_path):
                                            shutil.copy(
                                                image_file_path,
                                                dest_images,
                                            )
                                            logging.info(
                                                f"Copied image file: {image_file_path} to {dest_images}"
                                            )
                            elif sub_dir_name != ".data":
                                # Copy other subfolders to "data/document_folders" (including their contents)
                                destination_folder_path = os.path.join(
                                    dest_folders, sub_dir_name
                                )
                                shutil.copytree(
                                    sub_dir_path,
                                    destination_folder_path,
                                    dirs_exist_ok=True,
                                )
                                logging.info(
                                    f"Copied folder: {sub_dir_path} to {destination_folder_path}"
                                )
                        except Exception as e:
                            logging.error(
                                f"Failed to process subfolder: {sub_dir_path}. Error: {e}"
                            )


def serialise_dicts_to_json(output_files):
    """
    Serialize a dictionary of JSON data to specified file paths.

    Args:
        output_files (dict): A dictionary where keys are file paths and values are data to serialize.
    """
    for file_path, data in output_files.items():
        try:
            with open(file_path, "w", encoding="utf-8") as outfile:
                json.dump(data, outfile, indent=4)
            logging.info(f"Serialized data to {file_path}")
        except Exception as e:
            logging.error(f"Failed to serialize data to {file_path}. Error: {e}")


def setup_logging(log_directory="./logs", log_prefix="migration log"):
    """
    Sets up logging by creating a log directory (if it doesn't exist) and generating
    a timestamped log file for each execution.

    Args:
        log_directory (str): The directory where log files will be stored.
        log_prefix (str): The prefix for the log file name.

    Returns:
        str: The path to the log file being used.
    """
    # Ensure the log directory exists
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Generate a timestamped log file name
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_directory, f"{log_prefix}_{current_time}.log")

    # Configure logging
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Log initialization message
    logging.info("Logging initialized. Log file created.")

    return log_file
