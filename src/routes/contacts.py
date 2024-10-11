from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"]) # до цього apі-роутера будемо звертатися далі для створення роутів


@router.get("/birthdays", response_model=list[ContactResponse]) # для пошуку днів народж. у найбл. 7 днів. Цю функцію слід ставити перед ф-цією пошуку контакту за {contact_id}, інакше фаст-апі проводить пошук саме за {contact_id}, а не днем народження
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    bd_contacts = await repository_contacts.get_upcoming_birthdays(db)
    if not bd_contacts:
        raise HTTPException(status_code=404, detail="No upcoming birthdays")
    return bd_contacts


@router.get("/", response_model=list[ContactResponse]) # для виведення списку всіх контактів чи для пошуку за ім'ям, прізвищем або електронною поштою (Query)
async def get_contacts(db: Session = Depends(get_db),
    first_name: str | None = Query(None), 
    last_name: str | None = Query(None),
    email: str | None = Query(None)):
    print(f"Searching for contacts: first_name={first_name}, last_name={last_name}, email={email}")
    contacts = await repository_contacts.get_contacts(db, first_name, last_name, email)
    return contacts


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_all_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.read_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact {contact_id} not found")
    return contact


@router.post("/", response_model=ContactBase)
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse) # для редагування контактів, потрібно вносити дані в УСІ поля
async def update_contact(contact_id: int, body: ContactUpdate, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_note(note_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(note_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return contact




