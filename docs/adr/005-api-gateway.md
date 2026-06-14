# ADR-005: API Gateway как единая точка входа

## Статус

Принято

## Контекст

Клиентам (web, mobile) неудобно знать адреса 6+ микросервисов. Нужна централизованная аутентификация, rate limiting и единый TLS-terminator.

## Решение

Развернуть **API Gateway** (Kong или NGINX + lua) перед всеми сервисами:

- Маршрутизация: `/api/v1/users/*` → User Service, `/api/v1/products/*` → Catalog Service и т.д.
- JWT-валидация на gateway; сервисы доверяют заголовку `X-User-Id` от gateway (mTLS между gateway и сервисами).
- Rate limiting: 100 req/min для анонимных, 1000 req/min для авторизованных.
- CORS, request logging, correlation ID (`X-Request-Id`).

## Альтернативы

| Вариант | Плюсы | Минусы |
|---|---|---|
| BFF per client | Оптимизация под mobile/web | N BFF-сервисов |
| Service mesh only (Istio) | mTLS, observability | Не заменяет routing для клиентов |
| **API Gateway + mesh** | Полный контроль edge + internal | Два слоя инфраструктуры |

## Последствия

- Gateway — single point of failure → минимум 2 реплики за load balancer.
- OpenAPI-спецификации агрегируются в единый portal (Swagger UI).
- В dev-окружении gateway можно заменить прямым обращением к сервисам через docker-compose profiles.
