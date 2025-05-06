# Moving The Brain Exported Data to Obsidian Vault

## Context

I am not a developer and a github novice (maybe that will change).  So any pointers to improving the scripts or how I am using github are welcome
I am also a windows user and I do not have access to a Mac so I am not sure how these scripts work on Macs

## How To Run

1. Download these scripts to a folder
2. Export your Brain to a folder using the JSON method (these scripts assume the folder is called "export" and is in the root folder of these scripts, this can eb configured in the python file "enduser_config.py")
3. Create a folder with where you want the converted Brain data to go - your Obsidian Vault.  This vault can be pre-configured to your needs (for example, I use dataview, excalidraw and excalibrain and Tag Wrangler with "Detect All File Extensions" configured (this allows for none-markdown or images files, like .docx, to be visible in the explorer)).
4. You need to have python installed.  I use the following modules so if the script does not run for you then you may be missing a python module that needs importing using "pip"
5. Run the script "thebrain2markdown.py" by opening a terminal and typing "python thebrain2markdown.py".
6. Open Obsidian and open the folder containing your migrated Obsidian data,

## What it Does

### Obsidian Data

- All attachments are placed in a folder called "data".  Files attached to a Brain Thought are migrated to a sub-folder called "documents", embedded images are placed in a sub-folder call "embedded images".  Any folder within your Brain are migrated as the folders and their contents into the "data" folder.
- All Thoughts are migrated to the root of the Obsidian Folder
- Types and Tags are not migrated as files so any content you held inside these objects will not be migrated
- Brain Tags are migrated to the Obsidian Property "tags".  If you have nested Tags in your Brain then these will be recreated
- Types are not currently migrated
- Labels are added as Obsidian "Aliases"
- Private or Public flags on Thoughts are migrated to the "publish" from matter with true or false for public and private respectively
- An additional property is created called exTheBrain with a value of "yes".  This is so that in the future you can see where this data originated
- All Child and Jump Throughts are added at the end of the obsidian file in the format suitable for use with Excalibrain (e.g. "Jump:: [[File]])
- All attached are listed and linked at the bottom of the file.

### Other Folders and Files Generated

- A Folder called "logs" is created.  This folder contains log files, one for each execution of the script.  I use it for debnugging purposes
- A folder called "JSONS" is created.  This contains well formatted version of export The Brain "JSON" files "links", "thoughts" and "attachments" prefixed with "TB_Refactored_"  OT
other files in this folder are generally used for debugging purposes or temporary stores

### enduser_config.py file

You can edit this file to:

- Reference the folder containing your exported Brain files and folder:
  - For Example dir_location_of_Brain_folder = "./export" looks in the root of the folders containing the python scripts for a folder called "export"
- Referncing your Obsidian Vault where you want your Brain data migrated to:
  - For Example dir_location_of_obsidian_vault = "./obsidian" uses a called "obsidian" in the root of the folder containing the python scripts
- I have found that I need to run Brain exports and migrations a number of times as I discover how my Brain is used with reference to how the migrated data works in Obsidian.  I therefore the script clears out the contents of the dir_location_of_obsidian_vault folder but leaving the contents of the Obsidian folder ".obsidian" else it would be necessary to reconfigure and load plugins after each migration.  However, you might not want to clear out the contents of the folder (maybe if you are migrating to an existing obsidian vault - which I have not tested, but should be possible, but probably quite dangerous, so do some back-ups).  Whether the obsidian vault is cleared down or not before migration is set with the variable empty_obsidian_vault_dir_prior_to_running_the_script to either true of false
- The type_to_tags is for an idea I have of migrating Brain type as tags so at the moment it doesn't do anything.