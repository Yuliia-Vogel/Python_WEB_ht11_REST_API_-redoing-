# тут прописуємо функції, які використовуються в роутах у файлі src/routes/contacts.py
from datetime import date, timedelta
from typing import List

from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactBase, ContactResponse, ContactUpdate


async def get_all_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def read_contact(contact_id: int, db: Session) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    new_contact = Contact(first_name=body.first_name, 
                      last_name=body.last_name, 
                      email=body.email,
                      phone=body.phone,
                      birthday=body.birthday,
                      additional_info=body.additional_info)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


# async def update_contact(body: ContactUpdate, contact_id: int, db: Session) -> Contact | None:
#     print("ENTERED FUNCTION ")
#     contact = db.query(Contact).filter(Contact.id == contact_id).first()
#     print("filtering done")
#     if contact:
#         print(f"contact {contact_id} found")
#         contact.first_name = body.first_name
#         contact.last_name = body.last_name
#         contact.email = body.email
#         contact.phone = body.phone
#         contact.birthday = body.birthday
#         contact.additional_info = body.additional_info
#         print("all changed")
#         db.commit()
#         db.refresh(contact)
#         print("changes added to DB")
#     return contact

# Написав мені GPT на моє питання про помилку таке: виглядає так, що ти випадково передаєш цілий об'єкт 
# ContactUpdate як параметр до SQL-запиту, тоді як слід передавати окремі значення полів.
# Проблема в тому, що ти передаєш об'єкт Pydantic як аргумент у SQL-запиті, що викликає помилку 
# "can't adapt type 'ContactUpdate'". Psycopg2 (бібліотека для роботи з PostgreSQL) не розуміє, 
# як перетворити Pydantic модель на SQL-запит.
# Тому нижче - змінена функція редагування контактів, яка у мене нарешті запрацювала.


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if contact:    
        if body.first_name is not None:
            contact.first_name = body.first_name
        if body.last_name is not None:
            contact.last_name = body.last_name
        if body.email is not None:
            contact.email = body.email
        if body.phone is not None:
            contact.phone = body.phone
        if body.birthday is not None:
            contact.birthday = body.birthday
        if body.additional_info is not None:
            contact.additional_info = body.additional_info
        
        db.commit()
        db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_upcoming_birthdays(db: Session):
    today = date.today()
    upcoming = today + timedelta(days=7)
    # порівнюємо лише місяць і день, бо рік народження не має значення для майбутнього ДН
    contacts = db.query(Contact).filter(
        # перевіряємо ДН, коли обидві дати знаходяться в межах одного року
        ((extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day)) |
        ((extract('month', Contact.birthday) == upcoming.month) & (extract('day', Contact.birthday) <= upcoming.day)) |
        # враховуємо перехід  через НР (грудень-січень)
        ((extract('month', Contact.birthday) > today.month) & (extract('month', Contact.birthday) <= upcoming.month))
    ).all()

    return contacts


async def get_contacts(db: Session, first_name: str = None, last_name: str = None, email: str = None): # вивести список всіх контактів чи для пошуку за іменем, прізвищем чи ємейлом
    

    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()