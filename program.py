#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import unidecode

def generate_list_of_male_female_and_shared_names_2(males_path, females_path):
    male_names = set()
    female_names = set()
    shared_names = set()
    with open(males_path) as males_file:
        for name in males_file:
            name = unidecode.unidecode(name.strip()).lower()
            male_names.add(name)
    with open(females_path) as females_file:
        for name in females_file:
            name = unidecode.unidecode(name.strip()).lower()
            female_names.add(name)

    for name in male_names:
        if name in female_names:
            shared_names.add(name)
    for name in shared_names:
        if name in female_names:
            male_names.remove(name)
            female_names.remove(name)

    return male_names, female_names, shared_names

def write_file(new_table_path, new_table):
    with open(new_table_path, "w") as new_file:
        for line in new_table:
            new_file.write("%s\n" % line)


def verify_sex(path, out_path, males_path, females_path):
    new_table = []
    male_names , female_names, shared_names = generate_list_of_male_female_and_shared_names_2(males_path, females_path)
    with open(path) as file:
        table_csv = csv.reader(file, delimiter=",")
        next(table_csv)
        for surname,name,id,speciality,average,location,score,sex,nationality in table_csv:
            first_name = unidecode.unidecode(name.split()[0] ).lower()
            my_sex = get_sex(name, male_names , female_names, shared_names)
            if str(sex) != str(my_sex):
                line = "%s != %s, %s %s" % (my_sex, sex, name, surname)
                new_table.append(line)
                print(line)
    write_file(out_path, new_table)

def get_sex(name, male_names , female_names, shared_names):
    sex = None
    first_name = unidecode.unidecode(name.split()[0] ).lower()
    if first_name in shared_names:
        if len(name.split())>1:
            second_name = unidecode.unidecode(name.split()[1] ).lower()
            if second_name in male_names:
                sex = 0
            elif second_name in female_names:
                sex = 1
            else:
                sex = "ND"
        else:
            sex = "ND"
    elif first_name in male_names:
        sex = 0
    elif first_name in female_names:
        sex = 1
    else:
        sex = "ND"
    return sex

def add_sex_to_table(table_path, new_table_path, males_path, females_path):
        new_table = []
        male_names, female_names, shared_names = generate_list_of_male_female_and_shared_names_2(males_path, females_path)
        number_of_undefined = 0
        with open(table_path, 'r', encoding='latin-1') as table_file:
            table_csv = csv.reader(table_file, delimiter=",")
            next(table_csv)
            for surname,name,id,speciality,average,location,score,nationality in table_csv:
                sex= get_sex(name, male_names , female_names, shared_names)
                if sex == "ND":
                    number_of_undefined += 1
                line = (surname,name,id,speciality,average,location,score,nationality,sex)
                str_line = line = ','.join(map(str, line))
                new_table.append(str_line)

        print("Number of undefined names: %s" % number_of_undefined)

        write_file(new_table_path, new_table)

#add_sex_to_table("bd_unico.csv", "new_bd_unico.csv","hombres.csv", "mujeres.csv")
verify_sex("BD GRUPO 1.xlsx - BD Unico.csv", "different.csv","hombres.csv", "mujeres.csv")
