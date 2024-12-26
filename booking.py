from fastapi import APIRouter, Body
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.api.dependencies import DBDep, UserIdDep 

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/bookings")

async def create_bookings( user_id: UserIdDep, db: DBDep, bookings_data: BookingsAddRequest = Body()):
      _bookings_data = BookingsAdd(user_id=user_id, **bookings_data.model_dump())
      # async with async_session_maker() as session:
      #       room = await RoomsRepository(session).add(_room_data)            
      #       await session.commit()        
      bookings = await db.bookings.add(_bookings_data)
      await db.commit()                   
      return {"status": "OK", "data": bookings}   
