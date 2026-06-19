# ETL Pipeline

## Описание проекта

Проект реализует ETL-пайплайн на Python для загрузки данных из файлов (CSV, JSON, Excel, XML) в PostgreSQL с разделением на staging и core слои.

---

## Архитектура ETL пайплайна

```mermaid
flowchart LR

A[Data Sources: CSV / JSON / Excel / XML]

B[Staging Layer]

C[Validation Layer - cleaning + checks]

D[Core Layer - business data]

E[Analytics Layer - SQL / reports]

A --> B --> C --> D --> E

C --> C1[NULL handling]
C --> C2[Deduplication]
C --> C3[FK validation]

```
## Слои данных

### Staging
- сырые данные

### Core
- очищенные данные
- бизнес-правила
- проверка FK

---

## ETL процесс

### Staging
- загрузка файлов в staging таблицы
- TRUNCATE перед загрузкой

### Core
- чтение staging
- clean_* функции
- фильтрация FK
- загрузка в core

---

## ER Diagram (Core Layer)

```mermaid
erDiagram

    CUSTOMERS {
        int customer_id PK
        string full_name
        string email
        string phone
        string city
        date created_at
    }

    PRODUCTS {
        int product_id PK
        string product_name
        string category
        numeric price
        string currency
        boolean is_active
    }

    ORDERS {
        int order_id PK
        int customer_id FK
        int product_id FK
        int quantity
        numeric unit_price
        string currency
        timestamp order_timestamp
        string status
    }

    PAYMENTS {
        int payment_id PK
        int order_id FK
        string payment_method
        numeric amount
        string currency
        timestamp payment_timestamp
    }

    EVENTS {
        string event_id PK
        int customer_id FK
        int product_id FK
        string event_type
        timestamp event_timestamp
    }

    CUSTOMERS ||--o{ ORDERS : places
    PRODUCTS  ||--o{ ORDERS : contains
    ORDERS    ||--o{ PAYMENTS : has
    CUSTOMERS ||--o{ EVENTS : generates
    PRODUCTS  ||--o{ EVENTS : triggers
```
---

## Запуск проекта

### 1. Установить зависимости
```bash
pip install -r requirements.txt
```
### 2. Создать `.env`

```env
DB_USER=...
DB_PASSWORD=...
DB_IP=...
DB_PORT=...
DB_NAME=...
```
3. Запуск
Проект запускается через единый входной файл:
```bash
python main.py
```
## Структура проекта

```text
project/
├── data/
├── ddl/
├── dml/
├── sql/
├── src/
├── .gitignore
└── README.md
├── requirements.txt
```
---
