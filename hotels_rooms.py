from fastapi import Query, Body, APIRouter
from sqlalchemy import insert, select, func
from typing import Annotated
from src.schemas.hotels import Hotel, HotelPatch
from src.schemas.rooms import Room, RoomPatch
#from src.api.dependencies import PaginationParams
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])

router_room = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Все номера в отеле"])

@router.get("")
async def get_hotels( 
      pagination: PaginationDep,            
      #id: int | None = Query(None, description="Айдишник"),
      title: str | None = Query(None, description="Название отеля"),
      location: str |None =  Query(None, description="Локация"),
      
    
):
         per_page = pagination.per_page or 5
         async with async_session_maker()  as session:
               return await HotelsRepository(session).get_all(
                  location = location, 
                  title = title, 
                  limit=per_page,
                  offset=per_page * (pagination.page - 1)                 
                  
                  )
   

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
   async with async_session_maker()  as session:
      return await HotelsRepository(session).get_one_or_none(id=hotel_id)



@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
      async with async_session_maker() as session:
         await HotelsRepository(session).delete(id=hotel_id)
         await session.commit()   
      return{"status": "Ok"}


@router.post("")
async def create_hotel( hotel_data: Hotel = Body(openapi_examples={
   "1": {
         "summary": "Сочи", 
         "value": {
               "title": "Отель Сочи 5 звезд у моря",
               "location": "ул. Моря, 1"      
         }
   },
   "2": {
         "summary": "Дубай", 
         "value": {
                  "title": "Отель Дубай у фонтана",
                  "location": "ул. Шейха, 2"      
      }
}
})):

      async with async_session_maker() as session:
         
            #print(hotel_data.model_dump())
            hotel = await HotelsRepository(session).add(hotel_data)
            #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            #add_hotel_stmt = insert(HotelsOrm).values(hotel_data.model_dump()).returning(HotelsOrm)    
            #result = await session.execute(add_hotel_stmt)
            await session.commit() 
                           
            return {"status": "OK", "data": hotel}   


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
   async with async_session_maker() as session:
      await HotelsRepository(session).edit(hotel_data, id=hotel_id)
      await session.commit()   
   return{"status": "Ok"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def edit_hotel(
   hotel_id: int,
   hotel_data: HotelPatch
   
):
   async with async_session_maker() as session:
      await HotelsRepository(session).edit(hotel_data, partially_updated=True, id=hotel_id)
      await session.commit()   
   return{"status": "Ok"}
 
 
@router_room.get("", summary="Получение всех номеров выбранного отеля")
async def get_all_rooms(hotel_id: int):
      async with async_session_maker()  as session:
         return await RoomsRepository(session).get_rooms_all(hotels_id=hotel_id)


@router_room.get("/{room_id}", summary="Получение одного номера выбранного отеля")
async def get_one_room(hotel_id: int, room_id: int):
      async with async_session_maker()  as session:
         return await RoomsRepository(session).get_room_one(hotels_id=hotel_id, id=room_id)  
      
      
@router_room.post("")
async def create_room(      
      room_data: Room                 
                     ):    
   async with async_session_maker() as session:         
        
            room = await RoomsRepository(session).add(room_data)            
            await session.commit() 
                           
            return {"status": "OK", "data": room} 
         
         
@router_room.put("/{room_id}",  summary="Редактированиме комнаты одного номера выбранного отеля")
async def edit_hotel(hotel_id: int, room_id: int, room_data: Room):
   async with async_session_maker() as session:
      await RoomsRepository(session).edit(room_data, hotels_id=hotel_id, id = room_id)
      await session.commit()   
   return{"status": "Ok"} 


@router.patch("/{room_id}", summary="Частичное обновление данных о номере в отеле")
async def edit_room(
   hotel_id: int,
   room_id: int,
   room_data: RoomPatch
   
):
   async with async_session_maker() as session:
      await RoomsRepository(session).edit(room_data, partially_updated=True, id=hotel_id)
      await session.commit()   
   return{"status": "Ok"}


@router_room.delete("/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
      async with async_session_maker() as session:
         await RoomsRepository(session).delete(hotels_id = hotel_id, id = room_id)
         await session.commit()   
      return{"status": "Ok"}
