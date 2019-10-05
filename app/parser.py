import os
import csv

def parse_file(file=None):
    """
    :param file: file provided by user with list of id and names
    :return Array of dictionaries with id and name
    """
    if file is not None:
        f = file.splitlines()
        return get_dict(f)
    else:
        dirpath = os.getcwd()
        f = open(dirpath + '/app/static/companies.csv', 'rt', encoding="latin-1")
        reader = csv.reader(f, delimiter=',', quotechar='"')
        return get_dict_companies(reader)

def get_dict(file):
    """
    :param file: csv file provided by the user
    :return Array of dictionaries with id and name of the file provided
    """

    result = []
    for line in file:
        id, name = line.split(',')
        # Skip first line
        if id != 'id':
            result.append({ 'id': id, 'name': name })

    return result

def get_dict_companies(reader):
    """
    :param reader: csv reader
    :return Array of dictionaries with id and name of the file provided
    """

    result = []
    for line in reader:
        # Skip first line
        if line[0] != 'id':
            result.append({ 'id': line[0], 'name': line[1] })

    return result
