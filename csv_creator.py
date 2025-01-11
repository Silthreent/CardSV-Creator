import csv
import os
import configparser

# Load the default config file, then any user defined ones
config = configparser.ConfigParser()
config.read("default_config.ini")
config.read("custom_config.ini")

# Read a single file as a row in the CSV, as a single card
def read_card_file(card_path):
    print(f"Attempting load of '{card_path}'")

    with open(card_path) as file:
        if("#include" not in file.readline()):
            # Card was not told to be included, skip

            print("No #include, skipping")
            return []

        # Prepare the row with all the default column data
        columns = {}
        for tag in config["columns"]:
            # Leading @ means a built-in column with custom loading
            if(tag[0] == "@"):
                print(f"Loading built in tag {tag}")
                # DIR column is set to the name of the folder it's located in
                if(tag.lower() == "@dir"):
                    columns[config["columns"][tag]] = card_path.split("\\")[-2]
            # All other columns get their default value from config
            else:
                columns[tag] = config["columns"][tag]

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

                split = line[1:].strip().lower().rsplit(": ")
                print(f"Import tag '{split[0]}' found, setting to '{split[1]}'")

                if split[0] in columns:
                    columns[split[0]] = split[1]

    return columns

# Start creating the CSV file
def create_csv():
    # Start going through all the directories the user has chosen
    for dir in config["directories"]:
        print(f"Begin loading directory '{dir}'")

        # Create the CSV file for editing
        with open(f"{dir}.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Load all columns from the config file, default and user defined ones
            columns = []
            for tag in config["columns"]:
                # Leading @ means it's a built-in column
                # The name of the column becomes the value of the config entry
                if(tag[0] == "@"):
                    columns.append(config["columns"][tag])
                # All other column names become the key
                else:
                    columns.append(tag)
            csvwriter.writerow(columns)

            # Start going through the directory, defined in the config file
            # Every file found is attempted to be loaded
            for (root, dirs, files) in os.walk(config["directories"][dir]):
                for file in files:
                    card_data = read_card_file(os.path.join(root, file))

                    # Don't write the card if it failed to create for any reason
                    if(len(card_data) > 0):
                        csvwriter.writerow(card_data.values())

print("Starting card loader...")

create_csv()

print("Done, CSV created")