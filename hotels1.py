from fastapi import Query, Body, APIRouter
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from sqlalchemy import insert, select, func
from src.models.hotels import HotelsOrm
from src.database import engine
from repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels",  tags=["Отели"])


@router.get("")
async def get_hotels(
      pagination: PaginationDep,
      id: int |None = Query( None, descriptions = "Айдишник"),
      title: str | None = Query( None, description = "Название отеля"),     
      location: str| None = Query( None, description = "Название отеля"), 
):
   
      per_page = pagination.per_page or 5
      async with async_session_maker() as session:
         return await HotelsRepository(session).get_all(
            location = location, 
            title = title, 
            limit=per_page,                                                        
            offset=per_page * (pagination.page - 1))    
    
               
      # if pagination.page and pagination.per_page:
      #   return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
     
   
              
@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
      global hotels
      hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
      return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(open_examples={
   
   "1": {
      "summary": "Сочи",
      "value": {
            "title": "Отель Сочи 5 звезд у моря",
             "location": "ул. Моря, 1",
      }
   },
   "2": {
      "summary": "Дубай",
      "value": {
            "title": "Отель Дубай У фонтана",
            "location": "ул. Шейха, 2",
      }
   }   
   
   })  
   ):
   
      async with async_session_maker() as session:
         # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
         # await session.execute(add_hotel_stmt)
         hotel = await HotelsRepository(session).add(hotel_data)
         await session.commit()
   
      return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int,hotel_data: Hotel):
   hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
   hotel["title"] = hotel_data.title,
   hotel["name"] =  hotel_data.name
   return {"status": "OK"}
   


@router.patch("/{hotel_id}",
            summary="Частичное обновление данных об отеле",
            description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",)
def patch_hotel(
   hotel_id: int,
   hotel_data: HotelPATCH 
   ):
   hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
   if hotel_data.title:
      hotel["title"] = hotel_data.title
   if hotel_data.name:
      hotel["name"] = hotel_data.name
   return {"status": "OK"}
