<h1 align="center"> 🤖 Foreign Languages Cards Bot</h1>

Асинхронный Telegram-бот для изучения иностранных языков с двумя режимами обучения и интеллектуальной системой
кэширования.

<h2 align="center">📸 Демонстрация</h2>

### Начало работы
<img width="367" height="627" alt="photo_2026-06-11_21-20-16" src="https://github.com/user-attachments/assets/74924b73-6964-4b57-b061-11a863765d96" />

### Добавление карточки
<img width="382" height="540" alt="photo_2026-06-11_21-19-24" src="https://github.com/user-attachments/assets/ea9c5163-9c67-4dcb-81ee-34672441c64f" />

### Глаголы
<img width="375" height="456" alt="photo_2026-06-11_21-15-44" src="https://github.com/user-attachments/assets/63b59688-e8ea-49e3-91f4-af67397c36d7" />

### Карточки
<img width="363" height="277" alt="photo_2026-06-11_21-20-39" src="https://github.com/user-attachments/assets/4bde86d8-5cb4-4a50-a5ce-2e0f5a036d5d" />
<img width="375" height="325" alt="photo_2026-06-11_21-20-53" src="https://github.com/user-attachments/assets/c3d2f1db-85ab-49de-b465-ce60bd3037e8" />

<h2 align="center"> 🏗 Архитектура системы</h2>

Этот бот является частью микросервисной архитектуры и работает в связке
с [Foreign Languages Cards API](https://github.com/Konstantin-Sorokin/foreign-languages-cards-api).

```text
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────┐
│  Bot (aiogram)  │◄────►│   Redis     │
│                 │      │(кэш/очереди)│
└────────┬────────┘      └─────────────┘
         │
         │ HTTP запросы
         ▼
┌─────────────────┐      ┌─────────────┐
│  FastAPI API    │◄────►│ PostgreSQL  │
│                 │      │   (БД)      │
└─────────────────┘      └─────────────┘
```

### Как это работает:

- Бот — фронтенд для пользователя, управляет состояниями (FSM) и кэширует данные в Redis
- API — бэкенд, хранит данные в PostgreSQL, предоставляет REST endpoints
- Redis — промежуточный слой для быстрого доступа к пакам и управления очередями обучения

<h2 align="center"> 🛠 Стек технологий</h2>

- **Python 3.13+**
- **uv**
- **aiogram 3**
- **Redis 7**
- **Pydantic v2**
- **aiohttp-socks**
- **Docker**

<h2 align="center"> 📦 Основные возможности</h2>

### 🎯 Два режима обучения

#### 1️⃣ Мои карточки

- Пользователь добавляет свои слова с переводами
- Обучение только тех карточек, которые добавил сам
- Интервальное повторение для эффективного запоминания

#### 2️⃣ Неправильные глаголы

- Готовые тематические паки с неправильными глаголами
- Изучение всех трёх форм глагола (V1, V2, V3)
- Контекстные примеры с переводами для каждой формы
- Выбор конкретного пака или случайная выборка из всех паков

### ⚡ Кэширование

- **Lazy Loading**: данные загружаются из API только при первом обращении
- **Redis-очереди**: персональные очереди глаголов для каждого пользователя
- **Автоматическое обновление**: TTL 15 дней для паков, 1 час для сессий обучения

### 🔄 FSM (машина состояний)

- Управление этапами обучения: выбор режима → выбор пака → карточка → ответ
- Хранение текущей карточки в состоянии для быстрого доступа

<h2 align="center"> 🚀 Как запустить локально</h2>

### 1. Клонирование репозитория

```bash
git clone https://github.com/Konstantin-Sorokin/foreign-languages-card-bot
cd foreign-languages-card-bot
```

### 2. Настройка окружения

Создайте файл `.env` на основе `.env.template`

```env
TOKEN=your_telegram_bot_token
PROXY_URL=your_proxy_url (не обязательно)
API_URL=http://api:8000/api
REDIS__HOST=redis
REDIS__PORT=6379
REDIS__DB=0
```

### 3. Запуск через Docker Compose

```bash
docker-compose up -d
```

Бот автоматически подключится к Redis и API через Docker-сеть flc_backend.

### Тестирование

В стадии разработки
