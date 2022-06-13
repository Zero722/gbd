import os, csv

def check_folder(folder):
    if(not os.path.isdir(folder)):
        os.mkdir(folder)

def mapping(json_files, folder):
    dict = {}
    for i in range(len(json_files)):
        dict[json_files[i]] = i+1

    with open(folder + '\dict.csv', 'w', newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["FN", "Index"])
        for key, value in dict.items():
            writer.writerow([key, value])

    return dict

def convert_to_csv(df, folder, file_name):
    df.to_csv(folder + "\\" + file_name)

