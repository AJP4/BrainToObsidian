import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("refactor_check_boxes.log"), logging.StreamHandler()],
)


def refactor_check_boxes(dir_location_of_obsidian_vault):
    """
    Goes through all .md files in the specified folder and replaces:
    - Lines starting with '+' with '[x]'
    - Lines starting with '-' with '[ ]'
    Logs the files that were amended.
    """
    for root, _, files in os.walk(dir_location_of_obsidian_vault):
        for file in files:
            if file.endswith(".md"):  # Process only .md files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    modified = False
                    updated_lines = []
                    for line in lines:
                        if line.startswith("+"):
                            updated_lines.append(line.replace("+", "[x]", 1))
                            modified = True
                        elif line.startswith("-"):
                            updated_lines.append(line.replace("-", "[ ]", 1))
                            modified = True
                        else:
                            updated_lines.append(line)

                    if modified:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.writelines(updated_lines)
                        logging.info(f"Amended file: {file_path}")

                except Exception as e:
                    logging.error(f"Error processing file {file_path}: {e}")


# Example usage
if __name__ == "__main__":
    dir_location_of_obsidian_vault = "./obsidian"  # Replace with your actual directory
    refactor_check_boxes(dir_location_of_obsidian_vault)
