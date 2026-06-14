# ADR-002: Событийная интеграция для уведомлений и персонализации

## Статус

Принято

## Контекст

При смене статуса заказа нужно:

1. уведомить покупателя (email);
2. обновить профиль персонализации (категории покупок);
3. опционально — уведомить продавца.

Синхронные вызовы из Order Service к Notification Service и Feed Service увеличивают latency оформления заказа и создают каскадные сбои.

## Решение

Использовать **RabbitMQ** как брокер доменных событий. Order Service публикует события `OrderCreated`, `OrderStatusChanged`; подписчики обрабатывают их независимо.

Формат события — JSON CloudEvents-подобная обёртка:

```json
{
  "type": "OrderStatusChanged",
  "order_id": "uuid",
  "user_id": "uuid",
  "status": "shipped",
  "items": [{"product_id": "...", "category_id": "..."}],
  "occurred_at": "2026-06-14T12:00:00Z"
}
```

## Альтернативы

| Вариант | Плюсы | Минусы |
|---|---|---|
| Синхронные REST-вызовы | Простота | Coupling, рост latency |
| Kafka | Высокий throughput, replay | Избыточен на старте |
| **RabbitMQ** | Простая routing-модель, at-least-once | Нет long-term log retention |

## Последствия

- Уведомления доставляются с задержкой в секунды — приемлемо для email.
- Notification Service реализует **idempotent consumer** (dedup по `event_id`).
- При падении подписчика сообщения остаются в очереди до ack — нужен dead-letter queue для poison messages.
