from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# Service Model
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
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Portfolio Model
class PortfolioBase(BaseModel):
    title: str
    image: str
    category: str

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Contacts Model
class ContactsBase(BaseModel):
    name: str
    tagline: str
    phone: str
    whatsapp: str
    email: str

class ContactsUpdate(ContactsBase):
    pass

class Contacts(ContactsBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Admin Model
class AdminLogin(BaseModel):
    login: str
    password: str

class AdminResponse(BaseModel):
    success: bool
    message: str

# Upload Models
class UploadedImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    original_filename: str
    url: str
    size: int
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

class ImageUploadResponse(BaseModel):
    success: bool
    message: str
    image: Optional[UploadedImage] = None