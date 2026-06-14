# C4 Level 2 — Containers

Диаграмма контейнеров описывает основные deployable-единицы системы и их взаимодействие.

```mermaid
C4Container
    title Container Diagram — Маркетплейс

    Person(buyer, "Покупатель")
    Person(seller, "Продавец")

    System_Boundary(marketplace, "Маркетплейс") {
        Container(gateway, "API Gateway", "Kong / NGINX", "Маршрутизация, аутентификация, rate limiting")
        Container(user_svc, "User Service", "FastAPI", "Пользователи, роли, профили")
        Container(catalog_svc, "Catalog Service", "FastAPI", "Товары, категории, остатки")
        Container(feed_svc, "Feed Service", "Python", "Персонализированная лента")
        Container(order_svc, "Order Service", "FastAPI", "Корзина, заказы, статусы")
        Container(payment_svc, "Payment Service", "FastAPI", "Расчёт сумм, транзакции, комиссия")
        Container(notify_svc, "Notification Service", "Python", "Email/push уведомления")

        ContainerDb(user_db, "User DB", "PostgreSQL", "Пользователи и роли")
        ContainerDb(catalog_db, "Catalog DB", "PostgreSQL", "Товары и категории")
        ContainerDb(order_db, "Order DB", "PostgreSQL", "Заказы и позиции")
        ContainerDb(payment_db, "Payment DB", "PostgreSQL", "Платежи и ledger")
        ContainerDb(redis, "Redis", "Redis", "Профили персонализации, кэш")
        ContainerDb(search, "Search Index", "Elasticsearch", "Полнотекстовый поиск товаров")
        ContainerQueue(broker, "Message Broker", "RabbitMQ", "Доменные события")
    }

    System_Ext(payment_provider, "Платёжный провайдер")
    System_Ext(email_provider, "Email-провайдер")

    Rel(buyer, gateway, "HTTPS")
    Rel(seller, gateway, "HTTPS")

    Rel(gateway, user_svc, "REST")
    Rel(gateway, catalog_svc, "REST")
    Rel(gateway, feed_svc, "REST")
    Rel(gateway, order_svc, "REST")
    Rel(gateway, payment_svc, "REST")

    Rel(user_svc, user_db, "SQL")
    Rel(catalog_svc, catalog_db, "SQL")
    Rel(catalog_svc, search, "Index sync")
    Rel(order_svc, order_db, "SQL")
    Rel(order_svc, catalog_svc, "Reserve stock", "REST")
    Rel(order_svc, payment_svc, "Create payment", "REST")
    Rel(payment_svc, payment_db, "SQL")
    Rel(payment_svc, payment_provider, "Charge", "HTTPS")

    Rel(feed_svc, redis, "User profiles")
    Rel(feed_svc, catalog_svc, "Product search", "REST")
    Rel(feed_svc, broker, "Subscribe: ProductViewed")

    Rel(order_svc, broker, "Publish: OrderCreated, OrderStatusChanged")
    Rel(catalog_svc, broker, "Publish: ProductUpdated")
    Rel(notify_svc, broker, "Subscribe: order events")
    Rel(notify_svc, email_provider, "Send email", "HTTPS")
```

## Описание контейнеров

| Контейнер | Ответственность |
|---|---|
| **API Gateway** | Единая точка входа, JWT-валидация, маршрутизация к сервисам |
| **User Service** | Регистрация, аутентификация, роли `buyer` / `seller` |
| **Catalog Service** | CRUD товаров, управление остатками, индексация в Elasticsearch |
| **Feed Service** | Ранжирование ленты на основе профиля пользователя в Redis |
| **Order Service** | Жизненный цикл заказа: `created → paid → shipped → delivered` |
| **Payment Service** | Расчёт итога с комиссией, вызов провайдера, бухгалтерский ledger |
| **Notification Service** | Подписка на события заказов, отправка email |

## Синхронное vs асинхронное взаимодействие

- **Синхронно (REST):** оформление заказа требует немедленной проверки остатков и создания платежа.
- **Асинхронно (RabbitMQ):** уведомления, обновление профиля персонализации, синхронизация поискового индекса.
