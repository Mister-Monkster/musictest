# Развертывание проекта
## 1.  Запуск сервисов
```docker-compose up -d --build```
## 2. Проверка работы
* FastAPI: Откройте http://localhost:8000/docs (Swagger UI)

* PostgreSQL: Проверьте подключение:

```docker-compose exec db psql -U postgres -d app_db```

## 3. Применение миграций

```docker-compose exec app alembic upgrade head```

