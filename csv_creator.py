import csv
import os
import configparser

config = configparser.ConfigParser()
config.read("default_config.ini")
config.read("custom_config.ini")

def read_card_file(card_path):
    print(f"Attempting load of '{card_path}'")

    with open(card_path) as file:
        if("#include" not in file.readline()):
            print("No #include, skipping")
            return []

        columns = {}
        for tag in config["columns"]:
            columns[tag] = config["columns"][tag]

        columns["name"] = card_path.rsplit("\\")[-1][0:-3]

        for line in file:
            if "# Card Text" in line:
                print("Card text found")
                for line in file:
                    columns["text"] += line.strip() + "\\n"
                columns["text"] = columns["text"][:-2]
            elif line[0] == ">":
                split = line[1:].strip().lower().rsplit(": ")
                print(f"Import tag '{split[0]}' found, setting to '{split[1]}'")

                if split[0] in columns:
                    columns[split[0]] = split[1]

    return columns

def create_csv():
    with open("card_list.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        columns = []
        for tag in config["columns"]:
            columns.append(tag)
        csvwriter.writerow(columns)
        
        for (root, dirs, files) in os.walk(config["loading"]["FolderPath"]):
            for file in files:
                card_data = read_card_file(os.path.join(root, file))

                if(len(card_data) > 0):
                    csvwriter.writerow(card_data.values())

print("Starting card loader...")

create_csv()

print("Done, CSV created")