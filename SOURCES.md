# Источники

Проверено 1 сентября 2026 года. Для лабораторных использованы официальные руководства продуктов и документация учебных репозиториев. Ссылки в карточках работ ведут на конкретные разделы.

## MySQL 8.4

- [Установка в Windows](https://dev.mysql.com/doc/refman/8.4/en/windows-installation.html)
- [Запуск как службы Windows](https://dev.mysql.com/doc/refman/8.4/en/windows-start-service.html)
- [Файлы параметров](https://dev.mysql.com/doc/refman/8.4/en/option-files.html)
- [Журнал ошибок](https://dev.mysql.com/doc/refman/8.4/en/error-log.html)
- [CREATE USER](https://dev.mysql.com/doc/refman/8.4/en/create-user.html)
- [GRANT](https://dev.mysql.com/doc/refman/8.4/en/grant.html)
- [LOAD DATA](https://dev.mysql.com/doc/refman/8.4/en/load-data.html)
- [EXPLAIN](https://dev.mysql.com/doc/refman/8.4/en/explain.html)
- [Использование индексов](https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html)
- [CREATE PROCEDURE](https://dev.mysql.com/doc/refman/8.4/en/create-procedure.html)
- [CREATE TRIGGER](https://dev.mysql.com/doc/refman/8.4/en/create-trigger.html)
- [Переменные состояния сервера](https://dev.mysql.com/doc/refman/8.4/en/server-status-variables.html)

## PostgreSQL 18

- [Роли базы данных](https://www.postgresql.org/docs/18/database-roles.html)
- [Средства наблюдения и статистические представления](https://www.postgresql.org/docs/18/monitoring-stats.html)

## Наблюдение

- [Конфигурация Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [Prometheus mysqld_exporter](https://github.com/prometheus/mysqld_exporter/blob/main/README.md)
- [Создание панели Grafana](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/create-dashboard/)
- [Пороговые значения Grafana](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/configure-thresholds/)
- [Запросы и условия правил оповещения](https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rules/queries-conditions/)

## Лекции

- [3 курс — МДК.07.01](https://olgakraven.github.io/2026-UIABD3-lecture/)
- [4 курс — МДК.07.01](https://olgakraven.github.io/2026-UIABD4-lecture/)

## Демонстрационный экзамен

- [КИМ 09.02.07-5-2027 — специалист по информационным системам](https://bom.firpo.ru/Public/6506)
- Том 1 и официальные приложения использованы для проверки шести заданий, продолжительности и границ междисциплинарного покрытия.
- Учебные варианты в репозитории не копируют закрытые экзаменационные варианты и не заменяют официальные приложения КИМ.

## Ограничения

- Установка, восстановление и тесты выполняются только в учебной среде.
- Варианты конфигурации сервера являются учебной расчётной моделью и не заменяют нагрузочное тестирование.
- Имена метрик exporter зависят от версии; студент фиксирует фактическое имя серии и метки.
- MySQL — основная платформа курса; PostgreSQL используется для предметного сравнения, а не как взаимозаменяемый синтаксис.
- Пять работ 8 семестра поддерживают эксплуатационные критерии, но полная готовность к КИМ подтверждается только сквозным выполнением заданий 1–6.
