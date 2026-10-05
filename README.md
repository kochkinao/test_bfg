# Job Management Service

Тестовое задание на Junior Python-разработчика.

## Реализовано

- доменный слой: `Job`, `JobStatus`, история переходов;
- граф допустимых переходов статусов;
- абстракция `JobRepository`;
- `InMemoryJobRepository`;
- `JobService`;
- REST API на FastAPI;
- Pydantic-схемы запросов и ответов;
- зависимости через `Depends`;
- централизованная обработка ошибок;
- unit-тесты;
- API-тесты.

Всего: 10 проходящих тестов.

## API

- `POST /jobs`
- `GET /jobs/{job_id}`
- `GET /jobs?status=...`
- `POST /jobs/{job_id}/assign`
- `POST /jobs/{job_id}/status`

## Ошибки

- `JobNotFoundError` → 404
- `InvalidStatusTransitionError` → 409
- `InvalidJobDataError` → 422

Для `InvalidJobDataError` выбран код 422, так как ошибка связана с некорректными входными данными.

## Запуск

```bash
uv sync
uv run uvicorn test_task.main:app --reload
```

## Тесты
```bash
uv run pytest
```

## Не реализовано

Из-за ограничения по времени не реализованы:
- `SqlAlchemyJobRepository`;
- PostgreSQL;
- `docker-compose.yml`;
- integration-тесты;

Приоритет был отдан доменному слою, сервису, InMemory-репозиторию, API и тестам.

В задании не было ограничений на использование ИИ-инструментов. ChatGPT использовался как помощник для контроля прогресса, сверки реализации с требованиями тестового задания и выявления пропущенных требований.
Ссылка на диалог: https://chatgpt.com/share/6ac38b3b-5ee0-83ed-b94b-cc28f9177dd5