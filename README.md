**Сначала нужно установить все необходимые зависимости из файла ```"requirements.txt"```** (```pip install -r requirements.txt```)

**Для миграций с помощью Alembic использовать следующие команды:**
1. ```alembic init alembic (для создание папки для миграций)```;
2. ```alembic revision --autogenerate -m "Initial comm."```;
3. ```alembic upgrade head```