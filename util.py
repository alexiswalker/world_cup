import csv

def load_data():
    with open('results.csv', newline='') as result_file:
        reader = csv.reader(result_file)
        for row in reader:
            print(row[2])

if __name__ == '__main__':
    load_data()
