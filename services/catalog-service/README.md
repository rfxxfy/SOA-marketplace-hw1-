# Catalog Service

Микросервис управления товарным каталогом маркетплейса. Отвечает за CRUD товаров продавцов и резервирование остатков при оформлении заказов.

## API

| Метод | Путь | Описание |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/products` | Создать товар |
| GET | `/api/v1/products` | Список товаров (фильтры: `category`, `seller_id`) |
| GET | `/api/v1/products/{id}` | Получить товар |
| PATCH | `/api/v1/products/{id}` | Обновить товар |
| DELETE | `/api/v1/products/{id}` | Удалить товар |
| POST | `/api/v1/products/{id}/reserve` | Зарезервировать остаток (для Order Service) |

Интерактивная документация: http://localhost:8000/docs

## Запуск

Из корня репозитория:

```bash
docker compose up --build
```

## Пример запроса

```bash
# Создать товар
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "seller_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Wireless Headphones",
    "description": "Noise cancelling",
    "category": "electronics",
    "price": 4999.99,
    "stock": 100
  }'

# Health check
curl http://localhost:8000/health
```

## Связь с архитектурой

Catalog Service — один из контейнеров на [C4 Container Diagram](../../docs/c4/02-containers.md). Order Service вызывает `/reserve` синхронно при оформлении заказа; события `ProductUpdated` публикуются в RabbitMQ для синхронизации Elasticsearch (в полной реализации).
