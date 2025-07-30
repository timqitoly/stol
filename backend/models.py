from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from database import Base

# SQLAlchemy Models - Using String IDs for compatibility
class ServiceTable(Base):
    __tablename__ = "services"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    detailed_description = Column(Text, nullable=False)
    price = Column(String(100), nullable=False)
    images = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PortfolioTable(Base):
    __tablename__ = "portfolio"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    image = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContactsTable(Base):
    __tablename__ = "contacts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    tagline = Column(String(500), nullable=False)
    phone = Column(String(50), nullable=False)
    whatsapp = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UploadedImagesTable(Base):
    __tablename__ = "uploaded_images"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models for API (Request/Response)
class ServiceBase(BaseModel):
    name: str
    description: str
    detailedDescription: str
    price: str
    images: List[str] = []

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class Service(ServiceBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# Portfolio Models
class PortfolioBase(BaseModel):
    title: str
    image: str
    category: str

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# Contacts Models
class ContactsBase(BaseModel):
    name: str
    tagline: str
    phone: str
    whatsapp: str
    email: str

class ContactsUpdate(ContactsBase):
    pass

class Contacts(ContactsBase):
    id: str
    updatedAt: datetime

    class Config:
        from_attributes = True

# Admin Models
class AdminLogin(BaseModel):
    login: str
    password: str

class AdminResponse(BaseModel):
    success: bool
    message: str

# Upload Models
class UploadedImage(BaseModel):
    id: str
    filename: str
    original_filename: str
    url: str
    size: int
    createdAt: datetime

    class Config:
        from_attributes = True

class ImageUploadResponse(BaseModel):
    success: bool
    message: str
    image: Optional[UploadedImage] = None