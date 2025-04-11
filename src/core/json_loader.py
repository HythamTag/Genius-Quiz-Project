import json

En_materials_list = ['Geography',
                     'Historical',
                     'Literature',
                     'Science',
                     'General',
                     'Sports',
                     'Technology',
                     'Brain',
                     'Cinema',
                     'Songs',
                     'Sites',
                     'Promptitude',
                     'Pressure',
                     'Penalties',
                     'Luck_Wheel']

Ar_materials_list = ['جغرافيا',
                     'تاريخ',
                     'أدب',
                     'علوم',
                     'معلومات عامة',
                     'رياضة',
                     'تكنولوجيا',
                     'قدرات ذهنية',
                     'سينما و مسرح',
                     'أغاني و موسيقي',
                     'لوحات و معالم',
                     'سرعة بديهة',
                     'تحت ضغط',
                     'ضربات جزاء',
                     'عجلة الحظ']

En2Ar_material_dic = {key: value for key, value in zip(En_materials_list,Ar_materials_list)}


def read_json(filepath):
    with open(filepath, "r") as read_file:
        return json.load(read_file)


def main():
    print("Started Reading JSON file")

    with open("meterial_names/En2Ar_materials.json", "w") as write_file:
        json.dump(En2Ar_material_dic, write_file)

    # with open(r"meterial_names/Ar_materials.json", "r") as read_file:
    #     print("Converting JSON encoded data into Python dictionary")
    #     developer = json.load(read_file)
    #     print(developer)

        # print("Decoded JSON Data From File")
        # for key, value in developer.items():
        #     print(key, ":", value)
        # print("Done reading json file")


if __name__ == "__main__":
    main()
