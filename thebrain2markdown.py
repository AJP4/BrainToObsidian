import json
import os
import logging
from datetime import datetime
import yaml  # Add this import for YAML serialization
from TheBrainConstants import (
    ThoughtKind,
    ThoughtAccessType,
    LinkKind,
    LinkMeaning,
    LinkRelation,
    LinkDirection,
    AttachmentType,
    AttachmentNoteType,
    AttachmentSourceType,
)
import re
import utility as util
import enduser_config as config
import migration_functions as mig_funcs


# Directories for file migration
TheBrain_export_dir = config.dir_location_of_Brain_folder

# Directories for file migration
obsidian_vault_directory = config.dir_location_of_obsidian_vault
output_directory = "./JSONS"

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define input files and output directory
path_to_TheBrain_JSON_files = [
    os.path.join(TheBrain_export_dir, "links.json"),
    os.path.join(TheBrain_export_dir, "attachments.json"),
    os.path.join(TheBrain_export_dir, "thoughts.json"),
]  # Add more files as needed


# Paths to refactored input JSON files
thoughts_path = "./JSONS/TB_Refactored_thoughts.json"
links_path = "./JSONS/TB_Refactored_links.json"
attachments_path = "./JSONS/TB_Refactored_Attachments.json"

# Invalid file characters
invalid_file_characters = ["/", "*", "?", "|", "\\", '"', "<", ">", ":", ";", "#", "@"]
# List of common image file extensions
file_extensions_images = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg"]

# filepaths for outputting dictionaries created as json files for use and/or debugging
Links_json_output_file_path = "./JSONS/links_json.json"


# Configure logging
# Set up logging
log_file = util.setup_logging(log_directory="./logs", log_prefix="migration")
print(f"Log file created: {log_file}")


# Initialize dictionaries
nodes_json = {}
list_of_thoughts = {}
list_of_tags = {}
list_of_types = {}
links_json = {}
attachments_json = {}


# Clear the obsidian vault directory if required
if config.empty_obsidian_vault_dir_prior_to_running_the_script:
    # Check if the directory exists before clearing it
    if os.path.exists(obsidian_vault_directory):
        # Clear the content of the obsidian vault directory, excluding ".obsidian"
        # retain obsidian config files
        util.clear_folder(obsidian_vault_directory, [".obsidian"])
    else:
        # Create the directory if it doesn't exist
        os.makedirs(obsidian_vault_directory)
        logging.info(f"Created directory: {obsidian_vault_directory}")


# clear down the obsidian vault directory
util.clear_folder(output_directory)

# convert TheBrain JSON files to a format suitable for Obsidian
# and save them in the output directory
util.Serialise_TBjson_files(path_to_TheBrain_JSON_files, output_directory)


# create subdirectories in the obsidian vault directory

destination_dir_documents = os.path.join(obsidian_vault_directory, "data/documents")
destination_dir_embedded_images = os.path.join(
    obsidian_vault_directory, "data/embedded images"
)
destination_dir_document_folders = os.path.join(
    obsidian_vault_directory, "data/document_folders"
)

for directory in [
    destination_dir_documents,
    destination_dir_embedded_images,
    destination_dir_document_folders,
]:
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")


# move attacchment in the export Brain directory to the obsidian vault directory
util.process_exported_attachments(
    TheBrain_export_dir,
    destination_dir_documents,
    destination_dir_embedded_images,
    destination_dir_document_folders,
)


# Process links.json to build relationships
def create_links_json_dic(links_path, links_json):
    try:
        with open(links_path, "r", encoding="utf-8") as links_file:
            data = json.load(links_file)
            for item in data:
                node_id = item["ThoughtIdA"]
                if item["Meaning"] != LinkMeaning.NOTTHING:
                    links_json.setdefault(node_id, [])
                    links_json[node_id].append(
                        {
                            "ID": item["ThoughtIdB"],
                            "relation_type": item["Relation"],
                            "relation_key": item["Relation"],
                            "meaning_key": item["Meaning"],
                            "direction_key": item["Direction"],
                            "kind": item["Kind"],
                        }
                    )
    except Exception as e:
        logging.error(f"Failed to process links.json. Error: {e}")


# Process attachments.json to map attachments to nodes
def create_attachments_json_dic(attachments_path, attachments_json):
    try:
        with open(attachments_path, "r", encoding="utf-8-sig") as attachments_file:
            data = json.load(attachments_file)
            for item in data:
                node_id = item["SourceId"]
                attachments_json.setdefault(node_id, [])
                attachments_json[node_id].append(
                    {
                        "location": item["Location"],
                        "name": item["Name"],
                        "type": item["Type"],
                        "source_type": item["SourceType"],
                        "note_type": item["NoteType"],
                    }
                )
    except Exception as e:
        logging.error(f"Failed to process attachments.json. Error: {e}")


# Process thoughts.json to build nodes and their metadata
def create_thoughts_json_dic_with_links_attachments(
    thoughts_path,
    invalid_file_characters,
    nodes_json,
    list_of_thoughts,
    list_of_tags,
    list_of_types,
    links_json,
    attachments_json,
):
    try:
        with open(thoughts_path, "r", encoding="utf-8-sig") as thoughts_file:
            thought_object = json.load(thoughts_file)
            for thought in thought_object:
                node_id = thought["Id"]
                nodes_json[node_id] = {
                    "ID": node_id,
                    "Name": util.remove_invalid_character(
                        thought["Name"], "", invalid_file_characters
                    ),
                    "Kind": thought["Kind"],
                    "TypeId": thought.get("TypeId", ""),
                    "ACType": thought.get("ACType", ThoughtAccessType.PUBLIC),
                    "Label": thought.get("Label", ""),
                    "ForgottenDateTime": thought.get("ForgottenDateTime", ""),
                    "Links": [],
                    "Attachments": [],
                }

                # Add relationships
                for link in links_json.get(node_id, []):
                    nodes_json[node_id]["Links"].append(link)

                # Add attachments
                if thought["Kind"] == ThoughtKind.THOUGHT:
                    for attachment in attachments_json.get(node_id, []):
                        nodes_json[node_id]["Attachments"].append(attachment)

                # Categorize nodes
                if nodes_json[node_id]["Kind"] == ThoughtKind.TAG:
                    list_of_tags[node_id] = {
                        "ID": node_id,
                        "Name": nodes_json[node_id]["Name"],
                        "TagName": util.remove_invalid_character(
                            thought["Name"], "_", invalid_file_characters
                        ),
                        "Links": nodes_json[node_id]["Links"],
                    }
                elif nodes_json[node_id]["Kind"] == ThoughtKind.TYPE:
                    list_of_types[node_id] = {
                        "ID": node_id,
                        "Name": nodes_json[node_id]["Name"],
                        "Links": nodes_json[node_id]["Links"],
                    }
                else:
                    list_of_thoughts[node_id] = {
                        "ID": node_id,
                        "Name": nodes_json[node_id]["Name"],
                    }
    except Exception as e:
        logging.error(f"Failed to process thoughts.json. Error: {e}")


def clean_tag_names(list_of_tags):
    """
    Clean the TagName property in the list_of_tags dictionary.
    Removes leading and trailing spaces, replaces inline spaces with underscores,
    and removes leading underscores.
    """
    for node_id, node_data in list_of_tags.items():
        if "TagName" in node_data:
            # Remove leading and trailing spaces, replace inline spaces with "_"
            cleaned_tag_name = node_data["TagName"].strip().replace(" ", "_")
            # Remove leading underscores
            cleaned_tag_name = cleaned_tag_name.lstrip("_")
            node_data["TagName"] = cleaned_tag_name


def build_breadcrumb_path(node_id, list_of_tags, current_path=None):
    """
    Recursively build the breadcrumb path for a given node ID by traversing up the tree.
    """
    if current_path is None:
        current_path = []

    # Get the current node
    current_node = list_of_tags.get(node_id)
    if not current_node:
        return current_path

    # Prepend the current node's TagName to the path (already cleaned)
    current_path.insert(0, current_node["TagName"])

    # Find parent nodes by checking which tags reference this node in their Links
    for parent_id, parent_data in list_of_tags.items():
        for link in parent_data.get("Links", []):
            if (
                link.get("ID") == node_id
                and link.get("meaning_key") == LinkMeaning.TAGS_TO_TAGS
            ):  # Parent-child relationship
                # Recursively build the path for the parent node
                return build_breadcrumb_path(parent_id, list_of_tags, current_path)

    return current_path


def process_tag_type_names(list_of_tags, types_prepend_text):
    """
    Updates the TagName property in the list_of_tags dictionary.
    If a TagName starts with the types_prepend_text string, it removes all occurrences
    of the types_prepend_text and prepends the result with types_prepend_text + "/".
    """
    for node_id, node_data in list_of_tags.items():
        tag_name = node_data.get("TagName", "")
        if tag_name.startswith(types_prepend_text):
            # Remove all occurrences of types_prepend_text
            updated_tag_name = tag_name.replace(types_prepend_text, "")
            # Prepend the result with types_prepend_text + "/"
            node_data["TagName"] = f"{types_prepend_text}/{updated_tag_name}"


def generate_markdown_files(
    nodes_json, list_of_tags, links_json, thoughts_json, source_dir, output_dir
):
    """
    Generate markdown files for high-level objects in nodes_json with Kind == THOUGHT,
    excluding those with Thought Kind equal to 2.
    """
    logging.info("Generating markdown files...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for node_id, node_data in nodes_json.items():
        # Skip nodes with Thought Kind equal to 2
        if node_data["Kind"] == ThoughtKind.TYPE:
            logging.info(f"Skipped node: {node_id} with Kind == 2")
            continue

        # Skip nodes with a non-empty ForgottenDateTime
        if node_data["ForgottenDateTime"]:
            logging.info(f"Skipped node: {node_id} with non-empty ForgottenDateTime")
            continue

        # Only process high-level objects with Kind == THOUGHT
        if node_data["Kind"] != ThoughtKind.THOUGHT:
            continue

        # Create the markdown file name
        file_name = f"{node_data['Name']}.md"
        file_path = os.path.join(output_dir, file_name)

        logging.info(f"Processing node: {node_id}, Name: {node_data['Name']}")

        try:
            with open(file_path, "w", encoding="utf-8") as md_file:
                # Prepare YAML frontmatter data
                yaml_data = {}

                # Add tags
                tags = [
                    tag_data["TagName"]
                    for tag_data in list_of_tags.values()
                    for link in tag_data.get("Links", [])
                    if link.get("ID") == node_id
                    and link.get("meaning_key") == LinkMeaning.TAG_TO_THOUGHT
                ]
                if tags:
                    yaml_data["tags"] = tags

                # Add ACType
                if "ACType" in node_data:
                    yaml_data["publish"] = (
                        "true"
                        if node_data["ACType"] == ThoughtAccessType.PUBLIC
                        else "false"
                    )

                # create a frontmatter key to indicated that this is a TheBrain export
                yaml_data["exTheBrain"] = "yes"

                # Add Labels as aliases
                if "Label" in node_data:
                    yaml_data["aliases"] = node_data.get("Label")

                # Write YAML frontmatter
                md_file.write("---\n")
                yaml.dump(yaml_data, md_file, default_flow_style=False)
                md_file.write("---\n\n")

                # Add markdown attachments (Notes.md)
                notes_path = os.path.join(source_dir, node_id, "Notes.md")
                logging.info(f"Looking for Notes.md at: {notes_path}")
                if os.path.exists(notes_path):
                    logging.info(f"Notes.md found at: {notes_path}")
                    with open(notes_path, "r", encoding="utf-8") as notes_file:
                        notes_content = notes_file.read()
                        # Replace [****](brain://****) with [[****]]
                        notes_content = re.sub(
                            r"\[([^\]]+)\]\(brain://[^\)]+\)", r"[[\1]]", notes_content
                        )
                        # Replace local image references with ![[filename|200]]
                        notes_content = re.sub(
                            r"!\[.*?\]\(\.data/md-images/([^/]+\.(?:png|jpg|jpeg|gif|bmp|tiff|svg))(?:#.*)?\)",
                            r"\n![[\1|200]]",
                            notes_content,
                        )
                        md_file.write(notes_content)
                        md_file.write("\n\n")
                else:
                    logging.warning(f"Notes.md not found for node: {node_id}")

                # Append references to attachments
                for attachment in node_data.get("Attachments", []):
                    logging.info(f"Processing attachment: {attachment}")
                    if (
                        attachment["type"] == AttachmentType.INTERNAL_FILE
                        and attachment["source_type"] == AttachmentSourceType.ATTACHMENT
                        and attachment["note_type"] == AttachmentNoteType.ATTACHMENT
                    ):
                        md_file.write(f"[[{attachment['name']}]]\n")
                    elif (
                        attachment["type"] == AttachmentType.SUB_FILE
                        and attachment["source_type"] == AttachmentSourceType.ATTACHMENT
                        and attachment["note_type"] == AttachmentNoteType.ATTACHMENT
                    ):
                        md_file.write(f"![[{attachment['name']}]]\n")
                    elif (
                        attachment["type"] == AttachmentType.EXTERNAL_URL
                        and attachment["source_type"] == AttachmentSourceType.ATTACHMENT
                        and attachment["note_type"] == AttachmentNoteType.ATTACHMENT
                    ):
                        md_file.write(
                            f"[{attachment['name']}]({attachment['location']})\n"
                        )

                # Add child and jump links based on links_json
                if node_id in links_json:
                    for link in links_json[node_id]:
                        if link.get("meaning_key") == LinkMeaning.THOUGHT_TO_THOUGHT:
                            related_id = link.get("ID")
                            relation = link.get("relation_type")
                            if related_id in thoughts_json:
                                related_name = thoughts_json[related_id]["Name"]
                                if (
                                    relation == LinkRelation.PARENT_TO_CHILD
                                ):  # Child link
                                    md_file.write(f"child:: [[{related_name}]]\n")
                                elif relation == LinkRelation.JUMP:  # Jump link
                                    md_file.write(f"jump:: [[{related_name}]]\n")

            logging.info(f"Markdown file created: {file_path}")

        except Exception as e:
            logging.error(f"Failed to create markdown file for {node_id}. Error: {e}")


if config.types_to_tags:
    mig_funcs.convert_types_to_tags(
        thoughts_path, links_path, output_directory + "/originals"
    )

create_links_json_dic(links_path, links_json)
create_attachments_json_dic(attachments_path, attachments_json)
create_thoughts_json_dic_with_links_attachments(
    thoughts_path,
    invalid_file_characters,
    nodes_json,
    list_of_thoughts,
    list_of_tags,
    list_of_types,
    links_json,
    attachments_json,
)

clean_tag_names(list_of_tags)

# Update the "TagName" property for each node
for node_id, node_data in list_of_tags.items():
    breadcrumb_path = build_breadcrumb_path(node_id, list_of_tags)
    # Join the breadcrumb path with "/" and update the "TagName"
    node_data["TagName"] = "/".join(breadcrumb_path)

# remove repetitive occurances of the prend text for Types and add a single prepend text as a prefix
if config.types_to_tags:
    process_tag_type_names(list_of_tags, config.types_prepend_text)

# Save the updated tags_json back to a file
output_path = "./JSONS/updated_tags_json.json"
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(list_of_tags, outfile, indent=4)


# Serialize dictionaries to JSON files


# Call the function with the output files
output_files = {
    "./JSONS/nodes_json.json": nodes_json,
    "./JSONS/thoughts_json.json": list_of_thoughts,
    "./JSONS/tags_json.json": list_of_tags,
    "./JSONS/types_json.json": list_of_types,
    "./JSONS/links_json.json": links_json,
}
util.serialise_dicts_to_json(output_files)

print("Generating Markdown files...")
generate_markdown_files(
    nodes_json,
    list_of_tags,
    links_json,
    list_of_thoughts,
    TheBrain_export_dir,
    obsidian_vault_directory,
)

print("Markdown files generated successfully.")
