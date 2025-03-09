from fastapi import APIRouter, Request, HTTPException, status
from ..models.user import User, UserCreate, UserUpdate
from ..crud import users as user_crud


user_not_found_response = {
    404: {
        "description": "User with the given id not found",
        "content": {
            "application/json": {
                "example": {
                    "message": "User with id 67ccb6d6825b86fb6abcae70 not found"
                }
            }
        }
    }
}

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("", summary="Get all users", description="Fetch a list of all users", response_model=list[User])
async def getUsers(request: Request):
    users = await user_crud.fetch_all_users(request.app.database)
    return users


@router.get("/{id}", summary="Get user", description="Fetch a user by id", response_model=User, responses=user_not_found_response)
async def getUser(id: str, request: Request):
    user = await user_crud.fetch_user(request.app.database, id)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")


@router.post("", summary="Create a user", description="Manually create a user", response_model=User, status_code=status.HTTP_201_CREATED)
async def createUser(user: UserCreate, request: Request):
    new_user = await user_crud.create_user(request.app.database, user.model_dump())
    return new_user


@router.put("/{id}", summary="Update user", description="Update a user by ID", response_model=User, responses=user_not_found_response)
async def updateUser(id: str, user_data: UserUpdate, request: Request):
    updated_user = await user_crud.update_user(request.app.database, id, user_data.model_dump(exclude_unset=True))
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.delete("/{id}", summary="Delete user", description="Delete a user by ID", status_code=status.HTTP_204_NO_CONTENT, responses=user_not_found_response)
async def deleteUser(id: str, request: Request):
    result = await user_crud.remove_user(request.app.database, id)
    if result:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")