from main import get_data, col_names
import os
from rich import print




def transpose_data(data):
    output = {c: [] for c in col_names}
    for row in data:
        for i,icon in enumerate(row['icons']):
            if icon:
                output[col_names[i]].append(icon)
    return output


def main():
    data = get_data()
    print("Got data: {} rows".format(len(data)))
    data = transpose_data(data)
    print("Data transposed")

    for i,c in enumerate(col_names):
        file_count = len(os.listdir(c))
        valid = len(data[c]) == file_count
        print(c, valid)

if __name__ == '__main__':
    main()
