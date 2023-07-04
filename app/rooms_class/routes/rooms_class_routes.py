from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.rooms_class.models.rooms_class_models import RoomBase, All_Rooms
from app.database.database import get_db
from app.schemas.schemas import Section_Schema, Student_In_Section_Schema, Person_Schema, Student_Schema
from app.middleware import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["Rooms Class"],
    responses={404: {"description": "Not found"}}
)

# define a route to create a new room
@router.post("/", response_description="Create a new room", response_model=All_Rooms,
              status_code=status.HTTP_201_CREATED)
async def create_room(room_class: RoomBase, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admins can create rooms")
    
    # create a new room
    new_room = Section_Schema(**room_class.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


# define a route to get all rooms
@router.get("/", response_description="Get all rooms", response_model=list[All_Rooms],
              status_code=status.HTTP_200_OK)
async def get_all_rooms(db: Session = Depends(get_db), search: Optional[str] = ""):
    rooms = db.query(Section_Schema).filter(Section_Schema.name.ilike(f"%{search}%")).group_by(Section_Schema.id).distinct().all()

    #if no rooms found
    if not rooms:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No rooms found")
    return rooms


# define a route to get a single room
@router.get("/{room_id}", response_description="Get a single room by id",
              status_code=status.HTTP_200_OK)
async def get_single_room(room_id: uuid.UUID, db: Session = Depends(get_db)):
    room = db.query(Student_In_Section_Schema).join(Section_Schema, Section_Schema.id == Student_In_Section_Schema.section_id
                                        ).join(Student_Schema, Student_Schema.id == Student_In_Section_Schema.student_id
                                        ).join(Person_Schema, Person_Schema.id == Student_Schema.person_id
                                        ).filter(Section_Schema.id == room_id).all()
    
    # if no room found
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Room with id: {room_id} not found")
    
    result = []

    for i in room:
        room_data = {
            "student_id": i.student_id,
            "name": f"{i.student.person.firstname} {i.student.person.lastname}",
        }
        result.append(room_data)
    
    return {"id": room_id, "name": room[0].section.name, "students": result}


# define a route to update a room
@router.patch("/{room_id}", response_description="Update a room", response_model=All_Rooms,
              status_code=status.HTTP_200_OK)
async def update_room(room_id: uuid.UUID, room_class: RoomBase, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    if (not current_user.is_admin) | (not current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admins can update rooms")
    
    # get the room
    room = db.query(Section_Schema).filter(Section_Schema.id == room_id).first()
    
    # if no room found
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Room with id: {room_id} not found")

    # update the room
    room.name = room_class.name

    db.commit()
    db.refresh(room)
    return room