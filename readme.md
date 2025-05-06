# Instructions for Transferring The Brain Exported Data to an Obsidian Vault

## Context

Please note that I am not a developer and possess only basic knowledge of GitHub, though I am open to suggestions for improving the scripts or my use of GitHub. Additionally, as a Windows user without access to a Mac, I cannot confirm the functionality of these scripts on Mac systems.

## Procedure

1. **Download the Scripts**: Save the provided scripts to a designated folder.

2. **Export Brain Data**: Utilize the JSON method to export your Brain data to a folder. The scripts assume this folder is named "export" and is located in the root directory of the scripts. This configuration can be adjusted in the Python file `enduser_config.py`.

3. **Prepare Obsidian Vault**: Establish a folder for the converted Brain data, which will serve as your Obsidian Vault. This vault can be pre-configured to suit your preferences, such as incorporating plugins like Dataview, Excalidraw, Excalibrain, and Tag Wrangler with "Detect All File Extensions" enabled to accommodate non-markdown or image files.

4. **Python Installation**: Ensure Python is installed on your system. The script requires specific modules, which may need to be imported using `pip` if the script fails to execute.

5. **Execute the Script**: Launch the script `thebrain2markdown.py` by opening a terminal and entering the command `python thebrain2markdown.py`.

6. **Access Obsidian**: Open Obsidian and navigate to the folder containing your migrated data.

## Functionality

### Obsidian Data

* All attachments are organized into a folder named "data". Files attached to a Brain Thought are transferred to a sub-folder called "documents", while embedded images are placed in a sub-folder named "embedded images". Any folders within your Brain are migrated into the "data" folder along with their contents.

* All Thoughts are transferred to the root of the Obsidian Folder.

* Types and Tags are not migrated as files; thus, any content within these objects will not be transferred.

* Brain Tags are converted to the Obsidian Property "tags". Nested Tags in your Brain will be recreated accordingly.

* Types are not currently migrated.

* Labels are converted to Obsidian "Aliases".

* Private or Public flags on Thoughts are migrated to the "publish" property with true or false values for public and private, respectively.

* An additional property named `exTheBrain` is created with a value of "yes" to indicate the data's origin.

* All Child and Jump Thoughts are appended at the end of the Obsidian file in a format compatible with Excalibrain (e.g., `Jump:: [[File]]`).

* All attachments are listed and linked at the bottom of the file.

### Additional Folders and Files

* A folder named "logs" is created to store log files for each script execution, primarily for debugging purposes.

* A folder named "JSONS" is created to contain well-formatted versions of The Brain's exported JSON files, such as "links", "thoughts", and "attachments", prefixed with "TB_Refactored_". Other files in this folder are generally used for debugging or temporary storage.

### Configuration File: `enduser_config.py`

You may modify this file to:

#### `dir_location_of_Brain_folder`

* Specify the folder containing your exported Brain files and folders. For example, `dir_location_of_Brain_folder = "./export"` searches the root directory of the scripts for a folder named "export".

#### `dir_location_of_obsidian_vault`

* Specify the location of your Obsidian Vault for migrating Brain data. For example, `dir_location_of_obsidian_vault = "./obsidian"` uses a folder named "obsidian" in the root directory of the scripts.

#### `empty_obsidian_vault_dir_prior_to_running_the_script`

* The script is designed to clear the contents of the `dir_location_of_obsidian_vault` folder, excluding the ".obsidian" folder, to avoid reconfiguring and loading plugins after each migration. However, you may choose not to clear the folder, especially if migrating to an existing Obsidian vault. This option is controlled by setting the variable `empty_obsidian_vault_dir_prior_to_running_the_script` to either true or false.

#### `types_to_tags`

* The `types_to_tags` variable is used to indicate that whether you want Brain Types migrated as tags in Obsidian.

#### `types_prepend_text`

* If you set `types_to_tags` as True then text assigned to this variable is prepended to the tag name so that it can be identified in Obsidian tag lists

## File Wrangling

THis migration script may not do all that you need and more data wrangling is required.  So rather than script every edge case and create an overly complex end user configuration file it might be best to use some existing obsidian plugins.  I have found the following useful (they can be found via the community plugin browser):

* `Tag Wrangler`:  refactoring tags
* `Find orphaned files and broken links`:  I had many thoughts with very little content which then created files in Obsidian.  I used this to find and delete these files and leave behind link references without files, so should I need them at later date I can click the link and create one