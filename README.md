# ADMIN AI VK BOT
Этот проект представляет собой `Django` админку для управления базой данных `ВКонтакте бота`.
Проект включает:

- `Админку Django` для удобного управления пользователями, чатами и сообщениями.
- `API` для получения, создания и обновления данных о пользователях, чатах и сообщениях.
- `Статистику` по активности пользователей и чатов.

Проект полностью разворачивается в `Docker`, команды вынесены в `Makefile` для удобного использования.


## Необходимые зависимости
- [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Redis](https://redis.io/)
- [GNU Make](https://www.gnu.org/software/make/)


## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/username/repo-name.git
   cd repo-name
    ```

2. Установите все необходимые пакеты в разделе `Необходимые зависимости`.

3. Создайте файл .env по примеру из .env.example:

    ```bash 
    DJANGO_SECRET_KEY=secret-key
    DJANGO_PORT=8000
    ...
    ```

## Управление через Makefile

В проекте используется `Makefile` для удобного запуска и управления приложением.  
Перед запуском убедитесь, что в `.env` заданы все необходимые переменные.

### Доступные команды

| Команда             | Описание |
|---------------------|----------|
| `make app`          | Запустить приложение в Docker (с пересборкой образа, в фоне). |
| `make app-down`     | Остановить и удалить контейнеры. |
| `make app-logs`     | Посмотреть логи контейнера приложения. |
| `make app-shell`    | Открывает shell (bash) внутри контейнера приложения для ручного выполнения команд. |
| `make migrations`   | Создает новые миграции Django (`python manage.py makemigrations`) внутри контейнера. |
| `make migrate`      | Применяет миграции базы данных Django (`python manage.py migrate`) внутри контейнера. |
| `make app-down`     | Остановить и удалить контейнеры. |
| `make superuser`    | Создает суперпользователя Django (`python manage.py createsuperuser`) внутри контейнера. |
| `make collectstatic`| Собирает статические файлы Django (`python manage.py collectstatic`) внутри контейнера. |
| `make test`         | Запускает тесты проекта с помощью pytest внутри контейнера. |


### Пример использования
```bash
# Запуск приложения
make app

# Просмотр логов
make app-logs

# Остановка
make app-down

# Запуск тестов
make test
```
