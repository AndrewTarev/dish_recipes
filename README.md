# Приложение "Recipes of dishes"

Это приложение создано для пользователей, которые ищут или хотят поделиться рецептами блюд.


## Функциональность

1. *Регистрация, авторизация, аутентификация*: реализовано с помощью библиотеки Fastapi-Users.


2. *Создание суперпользователя*: Суперпользователь добавляет список блюд, а так же может манипулировать акаунтами пользователей.


3. *Создание рецептов*: Аутонтифицированый пользователь может создавать свои рецепты блюд, изменять их и просматривать 
   чужие рецкпты
  

4. *Кэширование* Реализовано кэширование запросов с помощью Redis.


## В проекте были использованы такие библиотеки:
1. FastApi
2. PostgresQL
3. SqlAlchemy(async)
4. Alembic
5. Pytest
6. Docker
7. Fastapi-Users
8. Redis
9. Poetry

## Установка

1. Клонируйте репозиторий на вашу локальную машину:  
   git clone https://github.com/AndrewTarev/parking_app.git


2. Запустите docker-compose командой: 
   docker compose build
   docker compose up