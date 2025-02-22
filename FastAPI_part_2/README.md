# Создание REST API на FastAPI часть II

## **Задача**: Вам нужно доработать проект из предыдущего задания «Создание REST API на FastApi» часть 1:

1. Добавить роут POST /login. В теле запроса должен передаваться JSON с именем пользователя и паролем.vv 
Роут возвращает токен. В дальнейшем токен будет использоваться для авторизации. Срок действия токена - 48 часов.   
Если клиент предоставил неверный логин пароль сервис должен выдать ошибку 401.  


2. Добавить роуты для управления пользователями:  
   - GET /user/{user_id?}
   - POST /user
   - PATCH /user/{user_id}
   - DELETE /user/{user_id}  

    Пользователи должны принадлежать одной из следующих групп: user, admin  


3. Права неавторизованного пользователя (клиент может токен не передавать):  
   - Создание пользователя POST /user
   - Получение пользователя по id GET /user/{user_id}
   - Получение объявления по id GET /advertisement/{advertisement_id}
   - Поиск объявления по полям GET /advertisement?{query_string}  
   

4. Права авторизованного пользователя с группой user:  
   - все права неавторизованного пользователя
   - обновление своих данных PATCH /user/{user_id}
   - удаление себя DELETE /user/{user_id}
   - создание объявления POST /advertisement
   - обновление своего объявления PATCH /advertisement/{advertisement_id}
   - удаление своего объявления DELETE /advertisement/{advertisement_id}  
   

5. Права авторизованного пользователя с группой admin:  
   - любые действия с любыми сущностям   
  
    Если у пользователя недостаточно прав для выполнения операции, то возвращается ошибка 403  


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
