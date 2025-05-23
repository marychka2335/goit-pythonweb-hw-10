import logging
from typing import Sequence, Optional

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas.contact import ContactCreateSchema, ContactUpdateSchema

logger = logging.getLogger("uvicorn.error")


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self, limit: int = 100, offset: int = 0
    ) -> Sequence[Contact]:
        """Отримати список контактів з пагінацією"""
        stmt = select(Contact).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        """Отримати контакт за його ідентифікатором"""
        stmt = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_contact(self, body: ContactCreateSchema) -> Contact:
        """Створити новий контакт з перевіркою унікальності email/телефону"""
        # Перевірка унікальності лише для тих полів, що мають значення
        if body.email:
            existing_contact = await self.db.execute(
                select(Contact).where(Contact.email == body.email)
            )
            if existing_contact.scalar_one_or_none():
                raise ValueError("Контакт з таким email вже існує")

        if body.phone_number:
            existing_contact = await self.db.execute(
                select(Contact).where(Contact.phone_number == body.phone_number)
            )
            if existing_contact.scalar_one_or_none():
                raise ValueError("Контакт з таким телефоном вже існує")

        contact = Contact(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdateSchema
    ) -> Optional[Contact]:
        """Оновити контакт з перевіркою унікальності email/телефону"""
        contact = await self.get_contact_by_id(contact_id)
        if not contact:
            return None

        update_data = body.model_dump(exclude_unset=True)

        # Якщо оновлюється email або телефон — перевірити на унікальність лише для непустих значень
        new_email = update_data.get("email")
        new_phone = update_data.get("phone_number")

        if new_email:
            stmt = select(Contact).where(
                Contact.email == new_email, Contact.id != contact_id
            )
            existing_contact = await self.db.execute(stmt)
            if existing_contact.scalar_one_or_none():
                raise ValueError("Інший контакт вже використовує цей email")

        if new_phone:
            stmt = select(Contact).where(
                Contact.phone_number == new_phone, Contact.id != contact_id
            )
            existing_contact = await self.db.execute(stmt)
            if existing_contact.scalar_one_or_none():
                raise ValueError("Інший контакт вже використовує цей телефон")

        # Оновлюємо контакт лише для полів, що не є null
        for key, value in update_data.items():
            setattr(contact, key, value)

        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Optional[Contact]:
        """Видалити контакт за ідентифікатором"""
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search_contacts(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Contact]:
        """
        Пошук контактів за іменем, прізвищем чи електронною адресою.
        """
        stmt = select(Contact)
        if first_name:
            stmt = stmt.where(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            stmt = stmt.where(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            stmt = stmt.where(Contact.email.ilike(f"%{email}%"))
        stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contacts_with_upcoming_birthdays(self) -> Sequence[Contact]:
        """
        Отримати контакти із днями народження, що настануть протягом наступних 7 днів.
        """
        stmt = select(Contact).where(
            func.to_char(Contact.birthday, "MM-DD").between(
                func.to_char(func.current_date(), "MM-DD"),
                func.to_char(func.current_date() + text("interval '7 days'"), "MM-DD"),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()