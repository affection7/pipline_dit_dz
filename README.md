# ETL Pipeline

## 📌 Описание проекта

Проект реализует ETL-пайплайн на Python для загрузки данных из файлов (CSV, JSON, Excel, XML) в PostgreSQL с разделением на staging и core слои.

---

## 🏗️ ETL Pipeline Architecture

```mermaid
flowchart LR

%% ======================
%% SOURCES
%% ======================
A[📂 Data Sources<br/>CSV / JSON / Excel / XML]

%% ======================
%% STAGING LAYER
%% ======================
B[🟡 Staging Layer<br/>Raw tables in PostgreSQL]

%% ======================
%% TRANSFORMATION
%% ======================
C[⚙️ ETL Processing<br/>Pandas cleaning + validation]

%% ======================
%% CORE LAYER
%% ======================
D[🟢 Core Layer<br/>Cleaned & validated tables]

%% ======================
%% RELATIONSHIPS
%% ======================
A -->|load with pandas| B
B -->|extract staging data| C
C -->|FK validation + cleaning| D

%% optional internal detail
C -.-> C1[Customer validation]
C -.-> C2[Product validation]
C -.-> C3[Order integrity checks]
```
## 🗄️ Слои данных

### Staging
- сырые данные
- минимальные преобразования

### Core
- очищенные данные
- бизнес-правила
- проверка FK

---

## 🔄 ETL процесс

### Staging
- загрузка файлов в staging таблицы
- TRUNCATE перед загрузкой

### Core
- чтение staging
- clean_* функции
- фильтрация FK
- загрузка в core

---

## 📊 ER Diagram (Core Layer)

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

## 🚀 Запуск проекта

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
```python
python main.py
```
📁 Структура проекта
project/
├── data/
├── ddl/
├── dml/
├── src/
├── requirements.txt
├── .gitignore
└── README.md

---
