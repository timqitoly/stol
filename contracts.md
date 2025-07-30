# API Contracts - Княжий Терем

## Моковые данные в mock.js

Сейчас используются следующие моковые данные:
1. **services** - массив услуг с полями: id, name, description, detailedDescription, price, images[]
2. **portfolio** - массив работ с полями: id, title, image, category  
3. **company** - контактная информация: name, tagline, phone, whatsapp, email

## API Endpoints для создания

### 1. Services API

**GET /api/services** - получить все услуги
```json
[
  {
    "id": "string",
    "name": "string", 
    "description": "string",
    "detailedDescription": "string",
    "price": "string",
    "images": ["string"],
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
]
```

**POST /api/services** - создать услугу
**PUT /api/services/:id** - обновить услугу  
**DELETE /api/services/:id** - удалить услугу

### 2. Portfolio API

**GET /api/portfolio** - получить все работы
```json
[
  {
    "id": "string",
    "title": "string",
    "image": "string", 
    "category": "string",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
]
```

**POST /api/portfolio** - добавить работу
**PUT /api/portfolio/:id** - обновить работу
**DELETE /api/portfolio/:id** - удалить работу

### 3. Contacts API

**GET /api/contacts** - получить контакты
```json
{
  "name": "string",
  "tagline": "string", 
  "phone": "string",
  "whatsapp": "string",
  "email": "string",
  "updatedAt": "datetime"
}
```

**PUT /api/contacts** - обновить контакты

### 4. Admin Authentication API

**POST /api/admin/login** - вход админа
```json
{
  "login": "string",
  "password": "string"
}
```

## MongoDB Collections

1. **services** - коллекция услуг
2. **portfolio** - коллекция портфолио  
3. **contacts** - коллекция контактов (одна запись)
4. **admin** - коллекция админов (одна запись)

## Frontend Integration Plan

### Замены в компонентах:

1. **HomePage.js**: 
   - Заменить useState(mockData.services) на API вызов useEffect(() => fetchServices())
   - Заменить useState(mockData.portfolio) на API вызов useEffect(() => fetchPortfolio()) 
   - Заменить useState(mockData.company) на API вызов useEffect(() => fetchContacts())

2. **AdminPage.js**:
   - Заменить все mock операции на реальные API вызовы
   - Добавить proper error handling
   - Добавить loading states

3. **Новые API функции**:
   - Создать `/src/services/api.js` с функциями для всех API вызовов
   - Использовать REACT_APP_BACKEND_URL для базового URL

## Error Handling

- Все API вызовы должны иметь try/catch
- Toast уведомления для успешных операций и ошибок
- Loading states для всех асинхронных операций

## Authentication

- Простая проверка логин/пароль через API
- Сохранение состояния авторизации в localStorage
- Проверка авторизации при входе в админ-панель

## Implementation Order

1. Создать MongoDB модели в backend
2. Создать API endpoints с CRUD операциями  
3. Создать API service в frontend
4. Заменить mock данные на API вызовы
5. Добавить error handling и loading states
6. Тестирование всей интеграции