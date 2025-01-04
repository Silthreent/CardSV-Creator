import csv
import os
import configparser

# Load the default config file, then any user defined ones
config = configparser.ConfigParser()
config.read("default_config.ini")
config.read("custom_config.ini")

def read_card_file(card_path):
    print(f"Attempting load of '{card_path}'")

    with open(card_path) as file:
        # Card was not told to be included, skip
        if("#include" not in file.readline()):
            print("No #include, skipping")
            return []

        # Prepare the row with all the default column data
        columns = {}
        for tag in config["columns"]:
            columns[tag] = config["columns"][tag]

        columns["name"] = card_path.rsplit("\\")[-1][0:-3]

        # Begin going through the rest of the file
        for line in file:
            if "# Card Text" in line:
                # Load card text, goes until end of file now

                print("Card text found")
                for line in file:
                    # If the line has an HTML header tag, it doesn't need a new line added
                    if("<h" in line):
                        columns["text"] += line.strip()
                    # Otherwise, just replace any newlines with an escape character'd one so it loads correctly
                    else:
                        columns["text"] += line.replace("\n", "\\n")
            elif line[0] == ">":
                # Load user defined column data

                split = line[1:].strip().lower().rsplit(": ")
                print(f"Import tag '{split[0]}' found, setting to '{split[1]}'")

                if split[0] in columns:
                    columns[split[0]] = split[1]

    return columns

# Start creating the CSV file
def create_csv():
    # Create the CSV file for editing
    with open("card_list.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Load all columns from the config file, default and user defined ones
        columns = []
        for tag in config["columns"]:
            columns.append(tag)
        csvwriter.writerow(columns)
        
        # Start going through the directory, defined in the config file
        # Every file found is attempted to be loaded
        for (root, dirs, files) in os.walk(config["loading"]["FolderPath"]):
            for file in files:
                card_data = read_card_file(os.path.join(root, file))

                # Don't write the card if it failed to create for any reason
                if(len(card_data) > 0):
                    csvwriter.writerow(card_data.values())

print("Starting card loader...")

create_csv()

print("Done, CSV created")