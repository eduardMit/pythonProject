import csv

with open('Cafenele.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)

    row_number = 0

    for row in reader:
        if row_number == 0:
            table_header = row
        else:
            for i in range(1, len(table_header)):
                print(f"Coffee {table_header[i]} rating {row[i]}")
            print()
            print("="*10)

        row_number += 1
    csv_file.close()
