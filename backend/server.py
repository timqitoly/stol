from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime
import shutil
import uuid
from PIL import Image

# Import database and models
from database import engine, Base, get_db_session
from models import (
    # SQLAlchemy models
    ServiceTable, PortfolioTable, ContactsTable, UploadedImagesTable,
    # Pydantic models
    Service, ServiceCreate, ServiceUpdate,
    Portfolio, PortfolioCreate, PortfolioUpdate,
    Contacts, ContactsUpdate,
    AdminLogin, AdminResponse,
    UploadedImage, ImageUploadResponse
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create uploads directory
UPLOADS_DIR = ROOT_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Create the main app without a prefix
app = FastAPI()

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Helper function to convert SQLAlchemy model to Pydantic model
def convert_service_to_pydantic(service_row) -> Service:
    return Service(
        id=str(service_row.id),
        name=service_row.name,
        description=service_row.description,
        detailedDescription=service_row.detailed_description,
        price=service_row.price,
        images=service_row.images or [],
        createdAt=service_row.created_at,
        updatedAt=service_row.updated_at
    )

def convert_portfolio_to_pydantic(portfolio_row) -> Portfolio:
    return Portfolio(
        id=str(portfolio_row.id),
        title=portfolio_row.title,
        image=portfolio_row.image,
        category=portfolio_row.category,
        createdAt=portfolio_row.created_at,
        updatedAt=portfolio_row.updated_at
    )

def convert_contacts_to_pydantic(contacts_row) -> Contacts:
    return Contacts(
        id=str(contacts_row.id),
        name=contacts_row.name,
        tagline=contacts_row.tagline,
        phone=contacts_row.phone,
        whatsapp=contacts_row.whatsapp,
        email=contacts_row.email,
        updatedAt=contacts_row.updated_at
    )

def convert_uploaded_image_to_pydantic(image_row) -> UploadedImage:
    return UploadedImage(
        id=str(image_row.id),
        filename=image_row.filename,
        original_filename=image_row.original_filename,
        url=image_row.url,
        size=image_row.size,
        createdAt=image_row.created_at
    )

# Helper function to resize and optimize images
async def process_image(file_path: Path, max_width: int = 1200, max_height: int = 800, quality: int = 85):
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new dimensions while maintaining aspect ratio
            ratio = min(max_width / img.width, max_height / img.height)
            if ratio < 1:
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(file_path, "JPEG", quality=quality, optimize=True)
    except Exception as e:
        logging.error(f"Error processing image {file_path}: {e}")

# Initialize default data
async def initialize_default_data():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    # Add default data
    async with get_db_session().__anext__() as session:
        # Check if contacts exist, if not create default
        result = await session.execute(select(ContactsTable))
        existing_contacts = result.scalar_one_or_none()
        
        if not existing_contacts:
            default_contacts = ContactsTable(
                name="Княжий Терем",
                tagline="Мастера чистовой отделки деревом",
                phone="+7 (999) 123-45-67",
                whatsapp="+79991234567",
                email="info@knyazhiy-terem.ru"
            )
            session.add(default_contacts)
            await session.commit()

        # Check if services exist, if not create default
        result = await session.execute(select(ServiceTable))
        existing_services = result.scalars().all()
        
        if not existing_services:
            default_services = [
                ServiceTable(
                    name="Баня из бруса",
                    description="Строительство и отделка бань из качественного бруса. Полный цикл работ от фундамента до финишной отделки.",
                    detailed_description="Мы используем только качественный брус из северных регионов России. Каждая баня строится с учетом индивидуальных пожеланий клиента. В стоимость входят все материалы, доставка и монтажные работы. Предоставляем гарантию на все виды работ сроком на 3 года. Дополнительно можем выполнить внутреннюю отделку, установку печи и системы водоснабжения.",
                    price="от 500 000 ₽",
                    images=[
                        "https://images.unsplash.com/photo-1571502973714-8c2b0cc0b7ee?w=400&h=300&fit=crop",
                        "https://images.unsplash.com/photo-1542078753-9b3ec0a9b6d5?w=400&h=300&fit=crop"
                    ]
                ),
                ServiceTable(
                    name="Беседка из дерева",
                    description="Изготовление и установка деревянных беседок. Различные размеры и дизайн под ваши потребности.",
                    detailed_description="Создаем уютные беседки для отдыха на природе. Работаем с различными породами дерева: сосна, лиственница, дуб. Предлагаем готовые проекты или разрабатываем индивидуальный дизайн. В комплект может входить мебель, освещение, декоративные элементы. Все конструкции обрабатываются защитными составами от влаги и насекомых.",
                    price="от 150 000 ₽",
                    images=[
                        "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=400&h=300&fit=crop",
                        "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=400&h=300&fit=crop"
                    ]
                ),
                ServiceTable(
                    name="Отделка дома деревом",
                    description="Внутренняя и внешняя отделка домов натуральным деревом. Работаем с различными породами дерева.",
                    detailed_description="Выполняем комплексную отделку деревом любых помещений. Используем вагонку, имитацию бруса, блок-хаус, массивную доску. Предварительно составляем проект с расчетом материалов. Все работы выполняются аккуратно с соблюдением технологий. Дополнительно устанавливаем плинтуса, наличники, декоративные элементы.",
                    price="от 2000 ₽/м²",
                    images=[
                        "https://images.unsplash.com/photo-1513594736757-3c44df5db6a9?w=400&h=300&fit=crop",
                        "https://images.unsplash.com/photo-1600563438938-a9e2e2a35470?w=400&h=300&fit=crop"
                    ]
                ),
                ServiceTable(
                    name="Деревянная мебель",
                    description="Изготовление мебели из дерева на заказ. Столы, стулья, шкафы, кровати и другая мебель.",
                    detailed_description="Создаем эксклюзивную мебель из массива дерева по индивидуальным проектам. Работаем с дубом, ясенем, березой, сосной. Каждое изделие проходит многоступенчатую обработку и покрывается экологически чистыми материалами. Предоставляем эскизы и 3D-визуализацию перед началом работ. Доставка и сборка на объекте включены в стоимость.",
                    price="от 30 000 ₽",
                    images=[
                        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop",
                        "https://images.unsplash.com/photo-1542744173-05336fcc7ad4?w=400&h=300&fit=crop"
                    ]
                )
            ]
            session.add_all(default_services)
            await session.commit()

        # Check if portfolio exists, if not create default
        result = await session.execute(select(PortfolioTable))
        existing_portfolio = result.scalars().all()
        
        if not existing_portfolio:
            default_portfolio = [
                PortfolioTable(
                    title="Русская баня",
                    image="https://images.unsplash.com/photo-1571502973714-8c2b0cc0b7ee?w=600&h=400&fit=crop",
                    category="Бани"
                ),
                PortfolioTable(
                    title="Садовая беседка",
                    image="https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=600&h=400&fit=crop",
                    category="Беседки"
                ),
                PortfolioTable(
                    title="Деревянная отделка",
                    image="https://images.unsplash.com/photo-1513594736757-3c44df5db6a9?w=600&h=400&fit=crop",
                    category="Отделка"
                ),
                PortfolioTable(
                    title="Кухонный гарнитур",
                    image="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop",
                    category="Мебель"
                ),
                PortfolioTable(
                    title="Терраса",
                    image="https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=600&h=400&fit=crop",
                    category="Террасы"
                ),
                PortfolioTable(
                    title="Деревянный стол",
                    image="https://images.unsplash.com/photo-1542744173-05336fcc7ad4?w=600&h=400&fit=crop",
                    category="Мебель"
                )
            ]
            session.add_all(default_portfolio)
            await session.commit()

# Image Upload Endpoints
@api_router.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...), session: AsyncSession = Depends(get_db_session)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        return ImageUploadResponse(
            success=False,
            message="Файл должен быть изображением"
        )
    
    # Validate file size (5MB max)
    if file.size > 5 * 1024 * 1024:
        return ImageUploadResponse(
            success=False,
            message="Размер файла не должен превышать 5MB"
        )
    
    try:
        # Generate unique filename
        file_extension = file.filename.split(".")[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process image (resize and optimize)
        await process_image(file_path)
        
        # Get file size after processing
        file_size = file_path.stat().st_size
        
        # Create image record
        base_url = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
        image_url = f"{base_url}/uploads/{unique_filename}"
        
        image_record = UploadedImagesTable(
            filename=unique_filename,
            original_filename=file.filename,
            url=image_url,
            size=file_size
        )
        
        # Save to database
        session.add(image_record)
        await session.commit()
        
        return ImageUploadResponse(
            success=True,
            message="Изображение успешно загружено",
            image=convert_uploaded_image_to_pydantic(image_record)
        )
        
    except Exception as e:
        logging.error(f"Error uploading image: {e}")
        return ImageUploadResponse(
            success=False,
            message=f"Ошибка загрузки: {str(e)}"
        )

@api_router.get("/uploaded-images", response_model=List[UploadedImage])
async def get_uploaded_images(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(
        select(UploadedImagesTable).order_by(UploadedImagesTable.created_at.desc())
    )
    images = result.scalars().all()
    return [convert_uploaded_image_to_pydantic(image) for image in images]

@api_router.delete("/uploaded-images/{image_id}")
async def delete_uploaded_image(image_id: str, session: AsyncSession = Depends(get_db_session)):
    try:
        # Find image record
        result = await session.execute(
            select(UploadedImagesTable).where(UploadedImagesTable.id == uuid.UUID(image_id))
        )
        image_record = result.scalar_one_or_none()
        
        if not image_record:
            raise HTTPException(status_code=404, detail="Изображение не найдено")
        
        # Delete file from filesystem
        file_path = UPLOADS_DIR / image_record.filename
        if file_path.exists():
            file_path.unlink()
        
        # Delete from database
        await session.execute(
            delete(UploadedImagesTable).where(UploadedImagesTable.id == uuid.UUID(image_id))
        )
        await session.commit()
        
        return {"message": "Изображение удалено успешно"}
        
    except Exception as e:
        logging.error(f"Error deleting image: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка удаления: {str(e)}")

# Services Endpoints
@api_router.get("/services", response_model=List[Service])
async def get_services(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(ServiceTable))
    services = result.scalars().all()
    return [convert_service_to_pydantic(service) for service in services]

@api_router.post("/services", response_model=Service)
async def create_service(service: ServiceCreate, session: AsyncSession = Depends(get_db_session)):
    service_record = ServiceTable(
        name=service.name,
        description=service.description,
        detailed_description=service.detailedDescription,
        price=service.price,
        images=service.images
    )
    session.add(service_record)
    await session.commit()
    await session.refresh(service_record)
    return convert_service_to_pydantic(service_record)

@api_router.put("/services/{service_id}", response_model=Service)
async def update_service(service_id: str, service: ServiceUpdate, session: AsyncSession = Depends(get_db_session)):
    # Update service
    stmt = (
        update(ServiceTable)
        .where(ServiceTable.id == uuid.UUID(service_id))
        .values(
            name=service.name,
            description=service.description,
            detailed_description=service.detailedDescription,
            price=service.price,
            images=service.images,
            updated_at=datetime.utcnow()
        )
    )
    result = await session.execute(stmt)
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    
    await session.commit()
    
    # Fetch updated service
    result = await session.execute(
        select(ServiceTable).where(ServiceTable.id == uuid.UUID(service_id))
    )
    updated_service = result.scalar_one()
    return convert_service_to_pydantic(updated_service)

@api_router.delete("/services/{service_id}")
async def delete_service(service_id: str, session: AsyncSession = Depends(get_db_session)):
    stmt = delete(ServiceTable).where(ServiceTable.id == uuid.UUID(service_id))
    result = await session.execute(stmt)
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    
    await session.commit()
    return {"message": "Service deleted successfully"}

# Portfolio Endpoints
@api_router.get("/portfolio", response_model=List[Portfolio])
async def get_portfolio(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(PortfolioTable))
    portfolio = result.scalars().all()
    return [convert_portfolio_to_pydantic(item) for item in portfolio]

@api_router.post("/portfolio", response_model=Portfolio)
async def create_portfolio(portfolio_item: PortfolioCreate, session: AsyncSession = Depends(get_db_session)):
    portfolio_record = PortfolioTable(
        title=portfolio_item.title,
        image=portfolio_item.image,
        category=portfolio_item.category
    )
    session.add(portfolio_record)
    await session.commit()
    await session.refresh(portfolio_record)
    return convert_portfolio_to_pydantic(portfolio_record)

@api_router.put("/portfolio/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(portfolio_id: str, portfolio_item: PortfolioUpdate, session: AsyncSession = Depends(get_db_session)):
    # Update portfolio
    stmt = (
        update(PortfolioTable)
        .where(PortfolioTable.id == uuid.UUID(portfolio_id))
        .values(
            title=portfolio_item.title,
            image=portfolio_item.image,
            category=portfolio_item.category,
            updated_at=datetime.utcnow()
        )
    )
    result = await session.execute(stmt)
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    await session.commit()
    
    # Fetch updated portfolio
    result = await session.execute(
        select(PortfolioTable).where(PortfolioTable.id == uuid.UUID(portfolio_id))
    )
    updated_portfolio = result.scalar_one()
    return convert_portfolio_to_pydantic(updated_portfolio)

@api_router.delete("/portfolio/{portfolio_id}")
async def delete_portfolio(portfolio_id: str, session: AsyncSession = Depends(get_db_session)):
    stmt = delete(PortfolioTable).where(PortfolioTable.id == uuid.UUID(portfolio_id))
    result = await session.execute(stmt)
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    
    await session.commit()
    return {"message": "Portfolio item deleted successfully"}

# Contacts Endpoints
@api_router.get("/contacts", response_model=Contacts)
async def get_contacts(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(ContactsTable))
    contacts = result.scalar_one_or_none()
    
    if not contacts:
        raise HTTPException(status_code=404, detail="Contacts not found")
    
    return convert_contacts_to_pydantic(contacts)

@api_router.put("/contacts", response_model=Contacts)
async def update_contacts(contacts: ContactsUpdate, session: AsyncSession = Depends(get_db_session)):
    # Update contacts (assuming there's only one record)
    stmt = (
        update(ContactsTable)
        .values(
            name=contacts.name,
            tagline=contacts.tagline,
            phone=contacts.phone,
            whatsapp=contacts.whatsapp,
            email=contacts.email,
            updated_at=datetime.utcnow()
        )
    )
    result = await session.execute(stmt)
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Contacts not found")
    
    await session.commit()
    
    # Fetch updated contacts
    result = await session.execute(select(ContactsTable))
    updated_contacts = result.scalar_one()
    return convert_contacts_to_pydantic(updated_contacts)

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
    return {"message": "Княжий Терем API (PostgreSQL)"}

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
    logger.info("Database initialized and default data created")

@app.on_event("shutdown")
async def shutdown_db_client():
    await engine.dispose()