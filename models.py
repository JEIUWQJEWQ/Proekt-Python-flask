from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base,engine


class Anketa(Base):
    __tablename__ = "anketa"

    id = Column(Integer, primary_key=True)
    prasanje = Column(Text, nullable=False)
    rok = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    opcii = relationship(
        "Opcii",
        back_populates="anketa",
        cascade="all, delete-orphan"
    )


class Opcii(Base):
    __tablename__ = "opcii"

    id = Column(Integer, primary_key=True)
    tekst = Column(String(200), nullable=False)
    anketa_id = Column(Integer, ForeignKey("anketa.id"), nullable=False)

    anketa = relationship(
        "Anketa",
        back_populates="opcii"
    )

    glasovi = relationship(
        "Glasovi",
        back_populates="opcija",
        cascade="all, delete-orphan"
    )


class Glasovi(Base):
    __tablename__ = "glasovi"

    id = Column(Integer, primary_key=True)
    opcija_id = Column(Integer, ForeignKey("opcii.id"), nullable=False)

    opcija = relationship(
        "Opcii",
        back_populates="glasovi"
    )



Base.metadata.create_all(bind=engine)
