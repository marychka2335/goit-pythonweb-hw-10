from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contact import ContactCreateSchema, ContactUpdateSchema


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactCreateSchema):
        return await self.contact_repository.create_contact(body)

    async def get_contacts(self, limit: int, offset: int):
        return await self.contact_repository.get_contacts(limit, offset)

    async def get_contact_by_id(self, contact_id: int):
        return await self.contact_repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactUpdateSchema):
        return await self.contact_repository.update_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        return await self.contact_repository.remove_contact(contact_id)

    async def search_contacts(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ):
        return await self.contact_repository.search_contacts(
            first_name, last_name, email, limit, offset
        )

    async def get_contacts_with_upcoming_birthdays(self):
        return await self.contact_repository.get_contacts_with_upcoming_birthdays()
