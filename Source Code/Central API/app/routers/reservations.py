from fastapi import APIRouter, HTTPException, Depends, status, Response
from ..models.reservation import ReservationBase, Reservation, ReservationCollection
from ..crud import reservations as reservations_crud
from ..utils.filtering import parse_reservations_filter


res_not_found_response = {
    404: {
        "description": "Reservation with the given id not found",
        "content": {
            "application/json": {
                "example": {
                    "message": "Reservation with id 67ccb6d6825b86fb6abcae70 not found"
                }
            }
        }
    }
}


router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.get(
    path="",
    summary="Get all reservations",
    description="Fetch a list of all reservations",
    response_model=ReservationCollection
)
async def getReservations(filters: dict = Depends(parse_reservations_filter)) -> ReservationCollection:
    reservations = await reservations_crud.fetch_all_reservations(filters)
    return ReservationCollection(reservations=reservations)


@router.get(
    path="/{id}",
    summary="Get reservation",
    description="Fetch a reservation by its Mongo id",
    response_model=Reservation,
    responses=res_not_found_response
)
async def getReservation(id: str) -> Reservation:
    reservation = await reservations_crud.fetch_reservation(id)
    if reservation:
        return reservation
    raise HTTPException(status_code=404, detail=f"Reservation with id {id} not found")


@router.post(
    path="",
    summary="Create reservation",
    description="Create a reservation record in the database",
    response_model=Reservation,
    responses={404: {"detail": "Conflict with existing reservation"}}
)
async def createReservation(reservation: ReservationBase) -> Reservation:
    created_reservation = await reservations_crud.create_reservation(reservation.model_dump(by_alias=True, exclude=["id"]))
    return created_reservation


@router.delete(
    path="/{id}",
    summary="Delete reservation",
    description="Delete a reservation by its mongo id",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=res_not_found_response
)
async def deleteReservation(id: str):
    result = await reservations_crud.remove_reservation(id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Reservation with id {id} not found")