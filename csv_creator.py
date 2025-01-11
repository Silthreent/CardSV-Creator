import csv
import os
import configparser

# Load the default config file, then any user defined ones
config = configparser.ConfigParser()
config.read("default_config.ini")
config.read("custom_config.ini")

# Read a single file as a row in the CSV, as a single card
def read_card_file(card_path, default_columns):
    print(f"Attempting load of '{card_path}'")

    with open(card_path) as file:
        if("#include" not in file.readline()):
            # Card was not told to be included, skip

            print("No #include, skipping")
            return []

        # Prepare the row with all the given default column data
        columns = {}
        for key, value in default_columns.items():
            # Leading @ means a built-in column with custom loading
            if(len(value) > 0 and value[0] == "@"):
                print(f"Loading built in tag {value}")
                # DIR column is set to the name of the folder it's located in
                if(value.lower() == "@dir"):
                    columns[key] = card_path.split("\\")[-2]
            # All other columns get their default value from given dict
            else:
                columns[key] = value

        # Name has custom override loading set to its filename
        columns["name"] = card_path.rsplit("\\")[-1][0:-3]

        # Begin going through the rest of the file
        for line in file:
            if "# Card Text" in line:
                # Load card text, goes until end of file now

                print("Card text found")
                for line in file:
                    # If the line has an HTML header tag, it doesn't need a new line added and needs its new line removed
                    if("<h" in line):
                        columns["text"] += line.strip()
                    # Otherwise, just replace any newlines with an HTML one
                    else:
                        columns["text"] += line.replace("\n", "<br>")
            elif line[0] == ">":
                # Load user defined column data

                split = line[1:].lower().split(":", maxsplit=1)
                print(f"Import tag '{split[0]}' found, setting to '{split[1].strip()}'")

                if split[0] in columns:
                    columns[split[0]] = split[1].strip()

    return columns

# Load the given config section as default columns
def read_config_columns(section_name, default_columns):
    if(config.has_section(section_name)):
        for tag in config[section_name]:
            # Set the default key/value pair to the config key/value
            default_columns[tag] = config[section_name][tag]

# Start creating the CSV file
def create_csv():
    # Start going through all the directories the user has chosen
    for dir in config["directories"]:
        print(f"Begin loading directory '{dir}'")

        # Create the CSV file for editing
        with open(f"{dir}.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Prepare all the columns from the config file, default and user defined ones
            default_columns = {}
            read_config_columns("columns", default_columns)
            read_config_columns(f"{dir}.columns", default_columns)
            csvwriter.writerow(default_columns)

            # Start going through the directory
            # Every file found is attempted to be loaded
            for (root, dirs, files) in os.walk(config["directories"][dir]):
                for file in files:
                    card_data = read_card_file(os.path.join(root, file), default_columns)

                    # Don't write the card if it failed to create for any reason
                    if(len(card_data) > 0):
                        csvwriter.writerow(card_data.values())

print("Starting card loader...")

create_csv()

if(len(config["directories"]) > 1):
    print("Done, CSVs created")
else:
    print("Done, CSV created")