# ADR-004: Database per service

## Статус

Принято

## Контекст

В микросервисной архитектуре сервисы должны быть автономными. Общая база данных создаёт скрытые зависимости: изменение схемы одного домена ломает другие сервисы.

## Решение

Каждый сервис владеет **собственной PostgreSQL-базой**:

| Сервис | База | Основные сущности |
|---|---|---|
| User Service | `users_db` | users, roles, sessions |
| Catalog Service | `catalog_db` | products, categories, stock |
| Order Service | `orders_db` | orders, order_items |
| Payment Service | `payments_db` | payments, ledger_entries |

Межсервисные данные передаются через API или события, **не через JOIN между БД**.

Elasticsearch — read-модель для Catalog Service (CQRS-lite для поиска).

Redis — общий инфраструктурный кэш для Feed Service (не source of truth).

## Альтернативы

| Вариант | Плюсы | Минусы |
|---|---|---|
| Shared database | Простые отчёты | Coupling, невозможность независимого деплоя |
| Shared schema, separate schemas | Компромисс | Всё ещё одна точка отказа |
| **Database per service** | Изоляция, независимость | Eventual consistency, дублирование данных |

## Последствия

- Отчёты по выручке собираются через Payment Service API или read-replica + ETL.
- Product snapshot денormalизуется в Order Service при создании заказа (цена на момент покупки).
- Миграции схем — только внутри owning-сервиса (Alembic/Flyway).
