import os
import json
from shutil import copyfile
from TheBrainConstants import ThoughtKind, LinkKind, LinkMeaning
import enduser_config as config


def convert_types_to_tags(thoughts_file, links_file, backup_folder):
    """
    Converts objects in TB_Refactored_thoughts.json and TB_Refactored_links.json based on the specified rules:
    1. Converts thoughts with ThoughtKind = TYPE to ThoughtKind = TAG and prepends "TYPE_" to their "Name".
    2. Converts links with LinkMeaning = TYPE_TO_THOUGHT to LinkMeaning = TAG_TO_THOUGHT and changes LinkKind to LINK_TYPE.
    3. Converts links with LinkMeaning = TYPE_TO_TYPE to LinkMeaning = TAG_TO_TAG and changes LinkKind to LINK_TYPE.

    Saves the original JSON files to a folder called "Original Refactored JSONS" and saves the amended files back to their original locations.
    """

    # Ensure backup folder exists
    os.makedirs(backup_folder, exist_ok=True)

    # Backup original files
    copyfile(thoughts_file, os.path.join(backup_folder, "TB_Refactored_thoughts.json"))
    copyfile(links_file, os.path.join(backup_folder, "TB_Refactored_links.json"))

    # Load JSON data
    with open(thoughts_file, "r", encoding="utf-8") as f:
        thoughts_data = json.load(f)

    with open(links_file, "r", encoding="utf-8") as f:
        links_data = json.load(f)

    # Process thoughts
    for thought in thoughts_data:
        if thought.get("Kind") == ThoughtKind.TYPE:
            thought["Kind"] = ThoughtKind.TAG
            if "Name" in thought:
                thought["Name"] = f"{config.types_prepend_text}{thought['Name']}"

    # Process links
    for link in links_data:
        if link.get("Meaning") == LinkMeaning.TYPE_TO_THOUGHT:
            link["Meaning"] = LinkMeaning.TAG_TO_THOUGHT
            link["Kind"] = LinkKind.LINK_TYPE
        elif link.get("Meaning") == LinkMeaning.TYPE_TO_TYPE:
            link["Meaning"] = LinkMeaning.TAGS_TO_TAGS
            link["Kind"] = LinkKind.LINK_TYPE

    # Save updated JSON data back to the original files
    with open(thoughts_file, "w", encoding="utf-8") as f:
        json.dump(thoughts_data, f, indent=4, ensure_ascii=False)

    with open(links_file, "w", encoding="utf-8") as f:
        json.dump(links_data, f, indent=4, ensure_ascii=False)

    print("Conversion completed. Original files have been backed up.")


def refactor_check_boxes(dir_location_of_obsidian_vault):
    """
    Goes through all .md files in the specified folder and replaces:
    - Lines starting with '+' with '[x]'
    - Lines starting with '-' with '[ ]'
    Only processes content below the YAML frontmatter (enclosed by '---').
    Logs the files that were amended.
    """
    print(f"Refactoring checkboxes in: {dir_location_of_obsidian_vault}")
    for root, _, files in os.walk(dir_location_of_obsidian_vault):
        for file in files:
            if file.endswith(".md"):  # Process only .md files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    modified = False
                    updated_lines = []
                    inside_yaml = (
                        False  # Track whether we are inside the YAML frontmatter
                    )

                    for line in lines:
                        # Detect YAML frontmatter boundaries
                        if line.strip() == "---":
                            inside_yaml = not inside_yaml
                            updated_lines.append(line)
                            continue

                        # Only process lines outside the YAML frontmatter
                        if not inside_yaml:
                            if line.startswith("+"):
                                updated_lines.append(line.replace("+", "- [x]", 1))
                                modified = True
                            elif line.startswith("-"):
                                updated_lines.append(line.replace("-", "- [ ]", 1))
                                modified = True
                            else:
                                updated_lines.append(line)
                        else:
                            updated_lines.append(line)

                    if modified:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.writelines(updated_lines)
                            print(f"Amended file, checkboxes in: {file_path}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    print(f"Refactored checkboxes in: {dir_location_of_obsidian_vault}")
