import sys
import re
import json
import argparse
from tqdm import tqdm
from typing import List

class Information:
    '''
               Объект класса Information содержит запись с информацией о пользователе.
               Attributes
               ----------
                 email : str
                   электронная почта пользователя
                 weight : str
                   вес пользователя
                 snils : str
                   идентефикатор пользователя
                 passport_series : str
                   серия паспорта пользователя
                 occupation : str
                   профессия пользователя
                 age : str
                   возраст пользователя
                 political_views : str
                   политические взгляды пользователя
                 worldview : str
                   мировоззрение/религия пользователя
                 address : str
                   адрес пользователя
            '''
    email: str
    weight: str
    snils: str
    passport_series: str
    occupation: str
    age: str
    political_views: str
    worldview: str
    address: str

    def  __init__(self, dic: dict):
        self.email = dic['email']
        self.weight = dic['weight']
        self.snils = dic['snils']
        self.passport_series = dic['passport_series']
        self.occupation = dic['occupation']
        self.age = dic['age']
        self.political_views = dic['political_views']
        self.worldview = dic['worldview']
        self.address = dic['address']

class InformationEncoder(json.JSONEncoder):
    def default(self,obj):
        return obj.__dict__


class Validator:
    '''
            Объект класса Validator является валидатором записей.
            Проверяет записи на корректность.
            Attributes
            ----------
              notes : List[Entry]
                Список записей
    '''

    notes: List[Information]

    def __init__(self, notes: List[Information]):
        self.notes = []
        for i in notes:
            self.notes.append(Information(i))

    def parse_note(self, notes: Information) -> List[str]:

        '''
                        Осуещствляет проверку корректности одной записи
                        Returns
                        -------
                          List[str]:
                            Список неверных ключей в записи
        '''
        incorrect_keys = []
        if self.check_email(notes.email) == 0:
            incorrect_keys.append('email')
        elif self.check_weight(notes.weight) == 0:
            incorrect_keys.append('weight')
        elif self.check_snils(notes.snils) == 0:
            incorrect_keys.append('snils')
        elif self.check_passport_series(notes.passport_series) == 0:
            incorrect_keys.append('passport_series')
        elif self.check_occupation(notes.occupation) == 0:
            incorrect_keys.append('occupation')
        elif self.check_age(notes.age) == 0:
            incorrect_keys.append('age')
        elif self.check_political_views(notes.political_views) == 0:
            incorrect_keys.append('political_views')
        elif self.check_worldview(notes.worldview) == 0:
            incorrect_keys.append('worldview')
        elif self.check_address(notes.address) == 0:
            incorrect_keys.append('address')

        return incorrect_keys

    def parse(self) -> (List[List[str]], List[Information]):

        '''
                Осуществляет проверку корректности записей
                Returns
                -------
                  (List[List[str]], List[Entry]):
                    Пара: cписок списков неверных записей по названиям ключей и список верных записей
        '''

        incorrect_n = []
        correct_n = []
        for i in self.notes:
            incorrect_keys = self.parse_note(i)
            if len(incorrect_keys) != 0:
                incorrect_n.append(incorrect_keys)
            else:
                correct_n.append(i)
        #print(incorrect_n)
        return (incorrect_n, correct_n)


    def check_email(self, email: str) -> bool:
        """"Функция, которая провереряет электронную почту на валидность"""
        pattern = r"^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$"
        if re.match(pattern, email):
            return True
        return False


    def check_weight(self, weight:str) -> bool:
        """""Функция, которая провереряет вес на валидность"""

        try:
            weight = float(weight)
        except ValueError:
            return False
        return 30 < weight < 250


    def check_snils(self, snils:str) -> bool:
        """"Функция, которая провереряет номер СНИЛСа на валидность"""

        pattern = "^\\d{11}$"
        if re.match(pattern, snils):
            return True
        return False


    def check_passport_series(self, passport:str) -> bool:
        """""Функция, которая провереряет Серии паспортов на валидность"""

        pattern = "^(\d{2})+\s+(\d{2})$"
        if re.match(pattern, str(passport)):
            return True
        return False


    def check_occupation(self, occupation:str) -> bool:
        """Функция, которая провереряет профессии на валидность"""

        pattern = r"^([а-яА-Я]|[a-zA-Z]|-| ){3,}$"
        if re.match(pattern, occupation):
            return True
        return False


    def check_age(self, age:str) -> bool:
        """"Функция, которая проверяет возраста людей на валидность"""

        try:
            age_1 = int(age)
        except ValueError:
            return False
        return 14 <= age_1 < 100

    def check_political_views(self, political_views:str) -> bool:
        """"Функция, которая провереряет политические взгляды людей на валидность"""

        pattern = r"^.+(?:ие|ые)$"
        if re.match(pattern, political_views):
            return True
        return False


    def check_worldview(self,worldview:str ) -> bool:
        """"Функция, которая провереряет вероисповедания на валидность"""

        pattern = "^.*[П|А|К|С|Б|И]*(?:изм|анство)$"
        if re.match(pattern, worldview):
            return True
        return False


    def check_address(self, address:str) -> bool:
        """""Функция, которая провереряет адреса на валидность"""

        pattern = "^[\w\s\.\d-]* \d+$"
        #r"(?:ул\.|Аллея) (?:им[\.\s]|)[^\s]+ [^\s]*(?:\s|)\d+"
        if re.match(pattern,address):
            return True
        return False

def summary(result: List[List[str]], filename: str = ''):
    '''
          Предоставляет итоговую информацию об ошибках в записях
          Parameters
          ----------
            result : List[List[str]]
              Список списков неверных записей по названиям ключей
    '''
    all_errors_count = 0
    errors_count = {
        "email": 0,
        "weight": 0,
        "snils": 0,
        "passport_series": 0,
        "occupation": 0,
        "age": 0,
        "political_views": 0,
        "worldview": 0,
        "address": 0,
    }
    for i in result:
        all_errors_count += 1
        for j in i:
            errors_count[j] += 1

    if filename == '':
        print('\n Ошибок в файле %d\n' % all_errors_count)
        print('Ошибки по типам: ')
        for key in errors_count.keys():
            print(key, errors_count[key], sep=' ')

    else:
        with open(filename, 'w') as file:
            file.write('Ошибок в файле  %d\n' % all_errors_count)
            for key in errors_count.keys():
                file.write(key + '\t' + str(errors_count[key]) + '\n')


def save_in_json(data: List[Information] , filename: str):
    with open(filename,'w',encoding='windows-1251') as output_file:
        json.dump(data,output_file,cls=InformationEncoder,ensure_ascii=False,indent=4)


if len(sys.argv) != 1:
    parser = argparse.ArgumentParser(description='Make users\' valid information.')
    parser.add_argument('-input_file', nargs=1, type=str, default="81.txt")
    parser.add_argument('-output_file', nargs=1, type=str, default="result.txt")
    args = parser.parse_args()

    input_file = args.input_file[0]
    output_file = args.output_file[0]
else:
    input_file = '81.txt'
    output_file = 'result.txt'

validator = Validator([])

with tqdm(range(100), colour='blue', ncols=100) as progressbar:
    data = json.load(open(input_file, encoding='windows-1251'))
    progressbar.update(25)
    validator = Validator(data)
    progressbar.update(35)
    invalid,valid = validator.parse()
    progressbar.update(70)
    """
    print('')
    progressbar.update(90)
    """
    summary(invalid, output_file)
    save_in_json(valid, 'correct_data.txt')