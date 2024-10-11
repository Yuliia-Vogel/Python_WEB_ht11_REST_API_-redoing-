from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class ContactBase(BaseModel): # визначає поля класу Contacts
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None


class ContactResponse(ContactBase): # модель відповіді при поверненні даних Contacts клієнту
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # цей атрибут використовується для увімкнення режиму ORM для цієї моделі


class ContactUpdate(ContactBase): # для оновлення контакту.
    first_name: Optional[str] # всі поля optional - щоб можна було оновити вибіркові поля
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]
    
    class Config:
        from_attributes = True