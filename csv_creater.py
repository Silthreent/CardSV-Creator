import csv
import os

def read_card_file(card_path, info):
    info["name"] = card_path.rsplit("\\")[-1][0:-3]

    print(f'Attempting load of "{info["name"]}"')
    with open(card_path) as file:
        if("#include" not in file.readline()):
            print("No #include, skipping")
            return []

        for line in file:
            if "# Card Text" in line:
                print("Card text found")
                for line in file:
                    info["text"] = line
            elif line[0] == ">":
                split = line[1:].strip().lower().rsplit(": ")
                print(f"Import tag '{split[0]}' found, setting to '{split[1]}'")

                if split[0] in info:
                    info[split[0]] = split[1]

    return info

def create_csv():
    with open("card_list.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["name", "count", "text", "cost"])
        
        for (root, dirs, files) in os.walk("TestCards"):
            for file in files:
                card_data = read_card_file(os.path.join(root, file), {"name": "", "count": 1, "text": "", "cost": 0})

                if(len(card_data) > 0):
                    csvwriter.writerow(card_data.values())

print("Starting card loader...")
create_csv()