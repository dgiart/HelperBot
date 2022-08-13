import csv
import sys
# from flask_wtf
from flask_wtf import FlaskForm
def write_to_csv(citizenDataToDb):
    citizen_info = ['fio', 'phone']
    with open('citizens.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=citizen_info)
        writer.writeheader()
        writer.writerows(citizenDataToDb)


if __name__ == '__main__':
    # help("modules")
    print (FlaskForm)
    # x = '1.'
    # i = int(x)
    # print(i)
    # data = [{'fio': 'art', 'phone': '123'}, {'fio': 'bob', 'phone': '456'}]
    # write_to_csv(data)