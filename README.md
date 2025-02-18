# Тестовое задание

Решение, которое позволяет:
* хранить информацию о состоянии счета абонента
* производить операции с счетом абонента
* по запросу выдавать текущие параметры счета абонента


Счет абонента состоит из следующих сущностей:
* уникальный номер абонента (uuid v4) - номер счета
* ФИО абонента (string) - фамилия, имя и отчество абонента, написанные кириллицей или латиницей
* текущий баланс на счете (int) - текущие денежные средства на счетеабонента (рубли и копейки)
* холды на счете (int) - арезервированные к выполнению операции насчете (рубли и копейки)
* статус счета (bool) - определяет возможность проведения операций посчету (закрыт — нельзя, открыт — можно)


### Методы API
* `GET  /api/ping` (работоспособность сервиса)
* `POST  /api/add` (пополнение баланса)
> Формат запроса:
```
{
    "addition": {
        "uuid": <account_uuid>,
        "additional_sum": <int:sum>
    }
}
```

* `POST  /api/substract` (уменьшение баланса)
> Формат запроса:
```
{
    "addition": {
        "uuid": <account_uuid>,
        "subtraction_sum": <int:sum>
    }
}
```
* `GET  /api/status` (остаток по балансу, открыт счет или закрыт)
> Формат запроса:
```
{
    "addition": {
        "uuid": <account_uuid>
    }
}
```

### Техническая информация об эксплуатации:
* Все сервисы разворачиваются, используя docker-compose.
* Сборка образов и разворачивание контейнеров осуществляется через bash-скрипт `run.sh`.
* При   падении   контейнера   приложения производится автоматический перезапуск контейнера 3 раза.
* Для публикации канала обмена c сервисом использован nginx как reverse-proxy (80 порт).

## Запуск
еред запуском убедитесь, что у вас установлен `docker-compose`
* `./run.sh`

Приложение доступно на `127.0.0.1:80`