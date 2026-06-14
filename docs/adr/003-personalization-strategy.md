# ADR-003: Стратегия персонализации ленты

## Статус

Принято

## Контекст

Покупатели ожидают релевантную ленту товаров. Полноценный ML-recommender (collaborative filtering на матрице user×item) требует большого объёма данных и инфраструктуры обучения моделей, недоступной на раннем этапе.

## Решение

Реализовать **гибридное rule-based ранжирование** с возможностью эволюции в ML:

```
score(product, user) =
    w_pop  × popularity_7d(product)
  + w_cat  × category_affinity(user, product.category)
  + w_rec  × recency_boost(user.recent_views, product.category)
  − w_div  × diversity_penalty(feed_so_far, product.category)
```

Параметры по умолчанию: `w_pop=0.3`, `w_cat=0.4`, `w_rec=0.2`, `w_div=0.1`.

**Cold start:** для пользователей без истории возвращается лента `popularity_7d` с равномерным микшированием категорий.

**Профиль пользователя** (Redis hash):

- `category_weights`: `{ "electronics": 0.8, "books": 0.3 }`
- `recent_views`: deque последних 50 product_id
- обновляется по событиям `ProductViewed`, `OrderCompleted`

## Альтернативы

| Вариант | Плюсы | Минусы |
|---|---|---|
| Без персонализации (только sort by date) | Тривиально | Плохой UX, низкая конверсия |
| Deep learning recommender | Максимальная релевантность | Cold start, инфраструктура |
| **Rule-based hybrid** | Быстрый запуск, интерпретируемость | Потолок качества ниже ML |

## Последствия

- Feed Service — отдельный контейнер, масштабируется горизонтально.
- A/B-тесты весов через feature flags (LaunchDarkly / собственный сервис).
- При накоплении данных (>100k interactions) — добавить embedding-based reranker без смены API.
