from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, func, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=True, unique=True, index=True
    )
    phone_number: Mapped[str] = mapped_column(
        String(20), nullable=True, unique=True, index=True
    )
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    additional_data: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )

    __table_args__ = (Index("ix_full_name", "first_name", "last_name"),)

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.expression
    def full_name(cls):
        return func.concat(cls.first_name, " ", cls.last_name)

    def __repr__(self):
        return (
            f"Student(id={self.id}, first_name={self.first_name}, "
            f"last_name={self.last_name}, email={self.email}, phone={self.phone_number})"
        )
