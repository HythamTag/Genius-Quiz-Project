import os
import re

import pandas as pd

from src.core.json_loader import read_json

threshold = 30
data_path = read_json('src/resources/meterial_names/Data_path.json')
data_dir = list(data_path.keys())[0]
data_file = data_path[data_dir]

img_types = ['png', 'jpg', 'bmp']
song_types = ['mp3', 'ogg', 'wav', 'm4a']



def read_data(directory):
    materials_list = read_json('src/resources/meterial_names/EN_materials.json')
    sheets_list = {}
    pos_list = []

    dir_list = os.listdir(data_dir)
    with pd.ExcelFile(directory) as reader:
        for material in materials_list:
            try:
                # sheet_list = pd.read_excel(reader, sheet_name=material).dropna(subset=['que'])
                sheet_list = pd.read_excel(reader, sheet_name=material)
                sheet_list = sheet_list[['que', 'ans', 'mc', 'type']]
                if len(sheet_list) < threshold:
                    sheet_list = sheet_list.reindex(list(range(0, threshold)))
                sheet_list['type'].fillna(value='w', inplace=True)
                sheet_list['que'].fillna(value='', inplace=True)
                sheet_list['ans'].fillna(value='', inplace=True)
                sheet_list['mc'].fillna(value='', inplace=True)

                sheets_list[material] = sheet_list
            except:
                pass

        try:
            file_paths = [os.path.join(data_dir, file) for file in dir_list if
                          file.split('.')[-1] in img_types + song_types]

            pos_list = [re.findall('\[.+\]', file_path)[-1].replace('[', '').replace(']', '').split(',') + [file_path] for
                        file_path in
                        file_paths]
            for material, row, col, path in pos_list:
                sheets_list[material].at[int(row), 'que'] = path
        except:
            pass
    return sheets_list


def main():
    data = read_data(os.path.join(data_dir, data_file))
    print(data['Historical'])
    #
    # wb = openpyxl.load_workbook(filename='Extra/trial.xlsx')
    # ws = wb.worksheets[0]
    #
    # ws.cell(row=2, column=2).value = 'a7eeeh'
    # wb.save('trial.xlsx')
    # # print(len(data[0]))
    #


if __name__ == '__main__':
    main()

