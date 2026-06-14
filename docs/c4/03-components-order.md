# C4 Level 3 — Components (Order Service)

Детализация внутренней структуры **Order Service** — сервиса, координирующего оформление заказов.

```mermaid
C4Component
    title Component Diagram — Order Service

    Container(gateway, "API Gateway", "Kong", "API Gateway")
    Container(catalog_svc, "Catalog Service", "FastAPI", "Catalog")
    Container(payment_svc, "Payment Service", "FastAPI", "Payments")
    ContainerDb(order_db, "Order DB", "PostgreSQL", "Orders")
    ContainerQueue(broker, "Message Broker", "RabbitMQ", "Events")

    Container_Boundary(order_svc, "Order Service") {
        Component(order_api, "Order API", "FastAPI Router", "REST endpoints: /orders, /cart")
        Component(order_app, "Order Application", "Python", "Use cases: create, cancel, update status")
        Component(cart_mgr, "Cart Manager", "Python", "In-memory/Redis cart per session")
        Component(stock_client, "Stock Client", "HTTP Client", "Reserve/release stock in Catalog")
        Component(payment_client, "Payment Client", "HTTP Client", "Initiate payment")
        Component(order_repo, "Order Repository", "SQLAlchemy", "Persistence layer")
        Component(event_publisher, "Event Publisher", "aio-pika", "Publish domain events")
        Component(state_machine, "Order State Machine", "Python", "Valid status transitions")
    }

    Rel(gateway, order_api, "REST", "HTTPS")
    Rel(order_api, order_app, "Calls")
    Rel(order_app, cart_mgr, "Uses")
    Rel(order_app, stock_client, "Uses")
    Rel(order_app, payment_client, "Uses")
    Rel(order_app, order_repo, "Uses")
    Rel(order_app, state_machine, "Uses")
    Rel(order_app, event_publisher, "Uses")
    Rel(order_repo, order_db, "SQL")
    Rel(stock_client, catalog_svc, "REST")
    Rel(payment_client, payment_svc, "REST")
    Rel(event_publisher, broker, "AMQP")
```

## Компоненты

| Компонент | Назначение |
|---|---|
| **Order API** | HTTP-слой: валидация запросов, маппинг DTO |
| **Order Application** | Оркестрация сценариев: создание заказа, отмена, смена статуса |
| **Cart Manager** | Корзина покупателя до оформления (Redis, TTL 7 дней) |
| **Stock Client** | Резервирование и освобождение остатков через Catalog Service |
| **Payment Client** | Создание платежа и polling статуса |
| **Order Repository** | CRUD заказов и позиций в PostgreSQL |
| **State Machine** | Допустимые переходы: `created→paid→shipped→delivered`, `*→cancelled` |
| **Event Publisher** | Публикация `OrderCreated`, `OrderStatusChanged` в RabbitMQ |

## Машина состояний заказа

```mermaid
stateDiagram-v2
    [*] --> created: POST /orders
    created --> paid: payment confirmed
    created --> cancelled: timeout / user cancel
    paid --> shipped: seller ships
    paid --> cancelled: refund
    shipped --> delivered: delivery confirmed
    delivered --> [*]
    cancelled --> [*]
```
