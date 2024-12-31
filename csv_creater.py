import csv
import os

def read_card_file(card_path):
    info = ["", 0, ""]
    info[0] = card_path.rsplit("\\")[-1][0:-3]
    info[1] = 1

    print(f'Attempting load of "{info[0]}"')
    with open(card_path) as file:
        if("#include" not in file.readline()):
            print("No #include, skipping")
            return []

        for line in file:
            if "# Card Text" in line:
                print("Card text found")
                for line in file:
                    info[2] = line

    return info

def create_csv():
    with open("card_list.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["name", "count", "text"])
        
        for (root, dirs, files) in os.walk("TestCards"):
            for file in files:
                card_data = read_card_file(os.path.join(root, file))

                if(len(card_data) > 0):
                    csvwriter.writerow(card_data)

print("Starting card loader...")
create_csv()