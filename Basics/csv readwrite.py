import csv

mydict = [{'branch': 'COE', 'cgpa': '9.0', 'name': 'Nikhil', 'year': '2'},
          {'branch': 'COE', 'cgpa': '9.1', 'name': 'Sanchit', 'year': '2'},
          {'branch': 'IT', 'cgpa': '9.3', 'name': 'Aditya', 'year': '2'},
          {'branch': 'SE', 'cgpa': '9.5', 'name': 'Sagar', 'year': '1'},
          {'branch': 'MCE', 'cgpa': '7.8', 'name': 'Prateek', 'year': '3'},
          {'branch': 'EP', 'cgpa': '9.1', 'name': 'Sahil', 'year': '2'}]

rows = [['Pratik', 'COE', '2', '9.0'],
        ['Sujan', 'COE', '2', '9.1'], ]


fields = ['name', 'branch', 'year', 'cgpa']

filename = "university_records.csv"

with open(filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    csvwriter = csv.writer(csvfile)
    writer.writeheader()
    writer.writerows(mydict)
    csvwriter.writerows(rows)


with open(filename, mode='r')as file:

    csvFile = csv.reader(file)

    for lines in csvFile:
        print(lines[0])
