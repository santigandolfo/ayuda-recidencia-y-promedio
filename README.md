# deduccion-genero-por-nombre

## Setup

- Dependencias:  [unidecode](https://pypi.org/project/Unidecode/)

```bash
$ pip3 install unidecode
```

## Run

```bash
$ python3 program.py  sorce destination
```

## Example

```bash
$ python3 program.py agregar-columna-sexo bd_unico.csv new_bd_unico.csv

$ python3 program.py vefificar-sexo bd-grupo-1.csv destination.csv
```

La base de datos con la informacióm de los nombres hombres y mujeres fue obtenida del siguiente repositorio:
[marcboquet/spanish-names]: (https://github.com/marcboquet/spanish-names/blob/master/hombres.csv)
