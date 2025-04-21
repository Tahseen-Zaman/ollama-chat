from database import AsyncSessionLocal
from models import CityInformation, Tour
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

async def get_all_tours():
     async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Tour)
            .options(
                selectinload(Tour.location).selectinload(CityInformation.country)
            )
            .where(Tour.is_active == True)
        )
        tours = result.scalars().all()

        formatted = []
        for tour in tours:
            if tour.location is None:
                continue
            location_name = tour.location.name if tour.location else "Unknown"
            country_name = (
                tour.location.country.country_name if tour.location and tour.location.country else "Unknown Country"
            )
            location_country = f"{location_name}, {country_name}"
            # Format the price
            price = f"${tour.starting_price:.2f}" if tour.starting_price else "Price not available"
            # Append formatted tour details
            formatted.append({
                "id": tour.id,
                "name": tour.name,
                "description": tour.description or "Explore this amazing destination!",
                "price": price,
                "locations": [location_name, location_country, country_name],
                "url": f"https://gozayaan.com/tour/details?id={tour.id}",
            })

        return formatted