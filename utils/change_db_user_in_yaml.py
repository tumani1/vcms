# coding: utf-8
import yaml
from os.path import abspath


def change(file_name):
    with open(abspath(file_name), 'r') as file:
        data = yaml.load(file)
    with open(abspath(file_name), 'w') as file:
        data['postgresql']['username'] = 'pgadmin'
        data['postgresql']['password'] = 'qwerty'
        yaml.safe_dump(data, file)

change('../configs/db.yaml')