# Создание REST API на FastAPI часть I

## **Задача**: Нужно написать на fastapi и докеризировать сервис объявлений купли/продажи.

Должны быть реализованы следующе методы:  

- Создание: POST /advertisement
- Обновление: PATCH /advertisement/{advertisement_id}
- Удаление: DELETE /advertisement/{advertisement_id}
- Получение по id: GET  /advertisement/{advertisement_id}
- Поиск по полям: GET /advertisement?{query_string}

У объявления должны быть следующие поля:

- заголовок
- описание
- цена
- автор
- дата создания  

Результатом работы является API, написанное на FastAPI.
  


## Документация по проекту  

Проект запускается с помощью docker, используя файл `docker-compose.yml`
(`хост: db`, `порт: 5432`) - команда `docker-compose up`

Проверить работу сервиса можно через `client.py`



Переменные окружения:

```bash
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_HOST (db)
- POSTGRES_PORT (5432)
```
