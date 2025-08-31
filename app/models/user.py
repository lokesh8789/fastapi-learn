from sqlalchemy import Column, Integer
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(
        sa_column=Column(
            Integer,
            primary_key=True,
            autoincrement=True,
        )
    )

    name: str = Field(
        nullable=False,
    )
    
    is_active: bool = Field(
        default=True,
        nullable=False,
    )
