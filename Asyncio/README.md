# Asyncio

## **Задача**: выгружать из API персонажей Start Wars и загружать в базу данных.
Документация по API находится здесь: [SWAPI](https://swapi.dev/documentation#people).

- Необходимо выгрузить cледующие поля:
- id - ID персонажа
- birth_year
- eye_color
- films - строка с названиями фильмов через запятую
- gender
- hair_color
- height
- homeworld
- mass
- name
- skin_color
- species - строка с названиями типов через запятую
- starships - строка с названиями кораблей через запятую
- vehicles - строка с названиями транспорта через запятую  

Данные по каждому персонажу необходимо загрузить в любую базу данных.
Выгрузка из апи и загрузка в базу должна происходить асинхронно.


Результатом работы будет:

1. скрипт миграции базы данных
2. скрипт загрузки данных из API в базу  

В базу должны быть загружены все персонажи

## Документация по проекту

Проект запускать через `main.py`

Установить зависимости:

```bash
pip install -r requirements.txt
```

Необходимо создать базу postgres в docker, используя `docker-compose.yml`: 
`порт: 5431` 

Переменные окружения:

```bash
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
```
