import csv

def read_card_file(card_path):
    info = ["", 0, ""]
    info[0] = card_path[0:-3]
    info[1] = 1

    with open("Test Card.md") as file:
        for line in file:
            if "# Card Text" in line:
                print("text found")
                for line in file:
                    info[2] = line

    return info

def create_csv():
    with open("card_list.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["name", "count", "text"])
        
        card_data = read_card_file("Test Card.md")
        csvwriter.writerow(card_data)

print("Starting card loader...")
create_csv()