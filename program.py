#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import unidecode


# Input: The path of the male names table and the female names
# Output: Three sets, one for the male names, one for the female names
# and one for all the names which were originally in both tables
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

# Input: List of the elements to be writen in the file
# Output: CSV file with the elements from the table
def write_file(new_table_path, new_table):
    with open(new_table_path, "w") as new_file:
        for line in new_table:
            new_file.write("%s\n" % line)

# Input: The name of the person, the path of the male names table
# and the path of the female names
# Output: The estimated sex of the person given their name
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

# Input: The source path of the source table, a path for
# the generated table, the path of the male names table
# and the path of the female names
# Output: A new table with every person whos sex diferes from
# the sex originally given in the table
# The source file must have the following columns:
# surname,name,id,speciality,average,location,score,sex,nationality
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
    write_file(out_path, new_table)

# Input: The source path of the source table, a path for
# the generated table, the path of the male names table
# and the path of the female names
# Output: A new table with a new column specifying the sex
# of the people in original table
# The source file must have the following columns:
# surname,name,id,speciality,average,location,score,nationality
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

        write_file(new_table_path, new_table)


def main(function, source, destination):

    if function == "agregar-columna-sexo":
        add_sex_to_table(source, destination,"hombres.csv", "mujeres.csv")
    elif function == "vefificar-sexo":
        verify_sex(source, destination,"hombres.csv", "mujeres.csv")

def parse_input(params):

    if len(params) != 4:
        print("Error: cantidad insuficiente de parámetros")
        print("Formato: program.py [function] [source] [destination]")
        return None

    function = params[1]
    source = params[2]
    destination = params[3]

    return {
            "function": function,
            "source": source,
            "destination": destination,
    }

if __name__ == "__main__":

    params = parse_input(sys.argv)

    if params is not None:
        main(params["function"],
             params["source"],
             params["destination"])
