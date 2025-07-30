from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime

# Import models
from models import (
    Service, ServiceCreate, ServiceUpdate,
    Portfolio, PortfolioCreate, PortfolioUpdate,
    Contacts, ContactsUpdate,
    AdminLogin, AdminResponse
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize default data
async def initialize_default_data():
    # Check if contacts exist, if not create default
    existing_contacts = await db.contacts.find_one()
    if not existing_contacts:
        default_contacts = {
            "id": "default",
            "name": "Княжий Терем",
            "tagline": "Мастера чистовой отделки деревом",
            "phone": "+7 (999) 123-45-67",
            "whatsapp": "+79991234567",
            "email": "info@knyazhiy-terem.ru",
            "updatedAt": datetime.utcnow()
        }
        await db.contacts.insert_one(default_contacts)

    # Check if services exist, if not create default
    services_count = await db.services.count_documents({})
    if services_count == 0:
        default_services = [
            {
                "id": "1",
                "name": "Баня из бруса",
                "description": "Строительство и отделка бань из качественного бруса. Полный цикл работ от фундамента до финишной отделки.",
                "detailedDescription": "Мы используем только качественный брус из северных регионов России. Каждая баня строится с учетом индивидуальных пожеланий клиента. В стоимость входят все материалы, доставка и монтажные работы. Предоставляем гарантию на все виды работ сроком на 3 года. Дополнительно можем выполнить внутреннюю отделку, установку печи и системы водоснабжения.",
                "price": "от 500 000 ₽",
                "images": [
                    "https://images.unsplash.com/photo-1571502973714-8c2b0cc0b7ee?w=400&h=300&fit=crop",
                    "https://images.unsplash.com/photo-1542078753-9b3ec0a9b6d5?w=400&h=300&fit=crop"
                ],
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "2",
                "name": "Беседка из дерева",
                "description": "Изготовление и установка деревянных беседок. Различные размеры и дизайн под ваши потребности.",
                "detailedDescription": "Создаем уютные беседки для отдыха на природе. Работаем с различными породами дерева: сосна, лиственница, дуб. Предлагаем готовые проекты или разрабатываем индивидуальный дизайн. В комплект может входить мебель, освещение, декоративные элементы. Все конструкции обрабатываются защитными составами от влаги и насекомых.",
                "price": "от 150 000 ₽",
                "images": [
                    "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=400&h=300&fit=crop",
                    "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=400&h=300&fit=crop"
                ],
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "3",
                "name": "Отделка дома деревом",
                "description": "Внутренняя и внешняя отделка домов натуральным деревом. Работаем с различными породами дерева.",
                "detailedDescription": "Выполняем комплексную отделку деревом любых помещений. Используем вагонку, имитацию бруса, блок-хаус, массивную доску. Предварительно составляем проект с расчетом материалов. Все работы выполняются аккуратно с соблюдением технологий. Дополнительно устанавливаем плинтуса, наличники, декоративные элементы.",
                "price": "от 2000 ₽/м²",
                "images": [
                    "https://images.unsplash.com/photo-1513594736757-3c44df5db6a9?w=400&h=300&fit=crop",
                    "https://images.unsplash.com/photo-1600563438938-a9e2e2a35470?w=400&h=300&fit=crop"
                ],
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "4",
                "name": "Деревянная мебель",
                "description": "Изготовление мебели из дерева на заказ. Столы, стулья, шкафы, кровати и другая мебель.",
                "detailedDescription": "Создаем эксклюзивную мебель из массива дерева по индивидуальным проектам. Работаем с дубом, ясенем, березой, сосной. Каждое изделие проходит многоступенчатую обработку и покрывается экологически чистыми материалами. Предоставляем эскизы и 3D-визуализацию перед началом работ. Доставка и сборка на объекте включены в стоимость.",
                "price": "от 30 000 ₽",
                "images": [
                    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop",
                    "https://images.unsplash.com/photo-1542744173-05336fcc7ad4?w=400&h=300&fit=crop"
                ],
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        ]
        await db.services.insert_many(default_services)

    # Check if portfolio exists, if not create default
    portfolio_count = await db.portfolio.count_documents({})
    if portfolio_count == 0:
        default_portfolio = [
            {
                "id": "1",
                "title": "Русская баня",
                "image": "https://images.unsplash.com/photo-1571502973714-8c2b0cc0b7ee?w=600&h=400&fit=crop",
                "category": "Бани",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "2",
                "title": "Садовая беседка",
                "image": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=600&h=400&fit=crop",
                "category": "Беседки",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "3",
                "title": "Деревянная отделка",
                "image": "https://images.unsplash.com/photo-1513594736757-3c44df5db6a9?w=600&h=400&fit=crop",
                "category": "Отделка",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "4",
                "title": "Кухонный гарнитур",
                "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop",
                "category": "Мебель",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "5",
                "title": "Терраса",
                "image": "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=600&h=400&fit=crop",
                "category": "Террасы",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "id": "6",
                "title": "Деревянный стол",
                "image": "https://images.unsplash.com/photo-1542744173-05336fcc7ad4?w=600&h=400&fit=crop",
                "category": "Мебель",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        ]
        await db.portfolio.insert_many(default_portfolio)

# Services Endpoints
@api_router.get("/services", response_model=List[Service])
async def get_services():
    services = await db.services.find().to_list(1000)
    return [Service(**service) for service in services]

@api_router.post("/services", response_model=Service)
async def create_service(service: ServiceCreate):
    service_dict = service.dict()
    service_obj = Service(**service_dict)
    await db.services.insert_one(service_obj.dict())
    return service_obj

@api_router.put("/services/{service_id}", response_model=Service)
async def update_service(service_id: str, service: ServiceUpdate):
    service_dict = service.dict()
    service_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.services.update_one(
        {"id": service_id}, 
        {"$set": service_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    
    updated_service = await db.services.find_one({"id": service_id})
    return Service(**updated_service)

@api_router.delete("/services/{service_id}")
async def delete_service(service_id: str):
    result = await db.services.delete_one({"id": service_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

# Portfolio Endpoints
@api_router.get("/portfolio", response_model=List[Portfolio])
async def get_portfolio():
    portfolio = await db.portfolio.find().to_list(1000)
    return [Portfolio(**item) for item in portfolio]

@api_router.post("/portfolio", response_model=Portfolio)
async def create_portfolio(portfolio_item: PortfolioCreate):
    portfolio_dict = portfolio_item.dict()
    portfolio_obj = Portfolio(**portfolio_dict)
    await db.portfolio.insert_one(portfolio_obj.dict())
    return portfolio_obj

@api_router.put("/portfolio/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(portfolio_id: str, portfolio_item: PortfolioUpdate):
    portfolio_dict = portfolio_item.dict()
    portfolio_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.portfolio.update_one(
        {"id": portfolio_id}, 
        {"$set": portfolio_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    updated_portfolio = await db.portfolio.find_one({"id": portfolio_id})
    return Portfolio(**updated_portfolio)

@api_router.delete("/portfolio/{portfolio_id}")
async def delete_portfolio(portfolio_id: str):
    result = await db.portfolio.delete_one({"id": portfolio_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return {"message": "Portfolio item deleted successfully"}

# Contacts Endpoints
@api_router.get("/contacts", response_model=Contacts)
async def get_contacts():
    contacts = await db.contacts.find_one()
    if not contacts:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return Contacts(**contacts)

@api_router.put("/contacts", response_model=Contacts)
async def update_contacts(contacts: ContactsUpdate):
    contacts_dict = contacts.dict()
    contacts_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.contacts.update_one(
        {"id": "default"}, 
        {"$set": contacts_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contacts not found")
    
    updated_contacts = await db.contacts.find_one({"id": "default"})
    return Contacts(**updated_contacts)

# Admin Endpoints
@api_router.post("/admin/login", response_model=AdminResponse)
async def admin_login(admin: AdminLogin):
    # Simple hardcoded admin check
    if admin.login == "admin" and admin.password == "admin123":
        return AdminResponse(success=True, message="Login successful")
    else:
        return AdminResponse(success=False, message="Invalid credentials")

# Basic endpoints
@api_router.get("/")
async def root():
    return {"message": "Княжий Терем API"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await initialize_default_data()
    logger.info("Default data initialized")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()