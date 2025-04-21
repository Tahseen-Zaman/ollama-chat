from pydantic import BaseModel
from typing import Any, List, Literal
from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]


class SingleTurnRequest(BaseModel):
    model: str
    prompt: list[str]


class ChatResponse(BaseModel):
    response: str

class ChatWithPackagesResponse(BaseModel):
    response: str
    packages: List[Any]

class ChatMessageV2(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class SingleTurnRequestV2(BaseModel):
    model: str
    prompt: List[ChatMessageV2]


Base = declarative_base()

# class Tour(Base):
#     __tablename__ = "tours_tour"  # Use the actual table name from Django

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(1000), index=True)
#     description = Column(Text, nullable=True)
#     starting_price = Column(Float, default=0.0)
#     duration = Column(Integer)  # Store duration as seconds for simplicity
#     is_active = Column(Boolean, default=False)
#     location_id = Column(Integer, ForeignKey("location_cityinformation.id"), nullable=True)
#     vendor_id = Column(Integer, ForeignKey("tours_tourvendor.id"), nullable=True)

#     # Relationships
#     location = relationship("CityInformation", back_populates="tours")
#     vendor = relationship("TourVendor", back_populates="tours")

#     def __repr__(self):
#         return f"<Tour(id={self.id}, name={self.name})>"


# class CityInformation(Base):
#     __tablename__ = "hotels_cityinformation"  # Match the actual table name from your database

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False, index=True)  # Name of the city
#     country_code = Column(String(5), ForeignKey("countries.code"), nullable=False)  # Foreign key to Country
#     latitude = Column(Float, nullable=True)  # Latitude of the city
#     longitude = Column(Float, nullable=True)  # Longitude of the city
#     description = Column(Text, nullable=True)  # Description of the city
#     timezone = Column(String(50), nullable=True)  # Timezone of the city
#     population = Column(Integer, nullable=True)  # Population of the city
#     elevation = Column(Integer, nullable=True)  # Elevation of the city

#     # Relationships
#     country = relationship("Country", back_populates="cities")  # Links to Country
#     tours = relationship("Tour", back_populates="location")  # Links to Tour

#     def __repr__(self):
#         return f"<CityInformation(id={self.id}, name={self.name}, country_code={self.country_code})>"

# from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean, Enum, Table
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class CityInformation(Base):
    __tablename__ = "hotels_cityinformation"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey("hotels_countryinformation.id"))  # <-- fixed table reference

    country = relationship("Country", backref="cities")
    tours = relationship(
        "Tour",
        back_populates="location"
    )  # Links to Tour
    def __repr__(self):
        return f"<CityInformation(id={self.id}, name={self.name}, country_id={self.country_id})>"

class Tour(Base):
    __tablename__ = (
        "tours_management_tour"  # Match the actual table name from your database
    )

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String(1000), nullable=False, index=True)  # Name of the tour
    description = Column(Text, nullable=True)  # Description of the tour
    starting_price = Column(Float, default=0.0)  # Starting price of the tour
    location_id = Column(
        Integer, ForeignKey("hotels_cityinformation.id"), nullable=True
    )  # Foreign key to CityInformation
    is_active = Column(Boolean, default=False)  # Active status of the tour

    # Relationships
    location = relationship(
        "CityInformation", back_populates="tours"
    )  # Links to CityInformation

    def __repr__(self):
        return f"<Tour(id={self.id}, name={self.name}, starting_price={self.starting_price})>"


class Country(Base):
    __tablename__ = "hotels_countryinformation"  # <-- fixed this line

    id = Column(Integer, primary_key=True)
    country_name = Column(String)