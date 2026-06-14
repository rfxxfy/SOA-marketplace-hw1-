# SOA Marketplace — HW1

Проектирование архитектуры цифрового маркетплейса: C4-диаграммы, ADR и развёрнутый микросервис в Docker.

## Структура репозитория

```
docs/
  architecture.md          # Обзор архитектуры, потоки данных
  c4/
    01-context.md          # C4 Level 1 — System Context
    02-containers.md       # C4 Level 2 — Containers
    03-components-order.md # C4 Level 3 — Order Service Components
  adr/                     # Architecture Decision Records
services/
  catalog-service/         # Catalog Service (FastAPI + PostgreSQL)
docker-compose.yml         # Запуск Catalog Service
```

## Быстрый старт

```bash
docker compose up --build
```

После запуска:

- Health check: http://localhost:8000/health
- Swagger UI: http://localhost:8000/docs

## Архитектура

Маркетплейс построен как **микросервисная система** из 6 сервисов:

| Сервис | Назначение |
|---|---|
| User Service | Покупатели и продавцы, роли |
| **Catalog Service** | Товарный каталог (реализован в Docker) |
| Feed Service | Персонализированная лента |
| Order Service | Оформление и статусы заказов |
| Payment Service | Расчёт и учёт платежей |
| Notification Service | Уведомления о статусах |

Подробнее: [docs/architecture.md](docs/architecture.md)

## C4-диаграммы

1. [System Context](docs/c4/01-context.md) — система и внешние акторы
2. [Containers](docs/c4/02-containers.md) — микросервисы и инфраструктура
3. [Components (Order Service)](docs/c4/03-components-order.md) — детализация сервиса заказов

Диаграммы в формате Mermaid C4 — рендерятся в GitHub и VS Code.

## Архитектурные решения (ADR)

| ADR | Тема |
|---|---|
| [001](docs/adr/001-microservices.md) | Микросервисная архитектура |
| [002](docs/adr/002-event-driven-integration.md) | Событийная интеграция (RabbitMQ) |
| [003](docs/adr/003-personalization-strategy.md) | Стратегия персонализации ленты |
| [004](docs/adr/004-database-per-service.md) | Database per service |
| [005](docs/adr/005-api-gateway.md) | API Gateway |

## Реализованный сервис

**Catalog Service** — REST API для управления товарами продавцов:

```bash
curl http://localhost:8000/health
```

См. [services/catalog-service/README.md](services/catalog-service/README.md)
