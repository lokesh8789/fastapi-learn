from typing import Annotated
from fastapi import Depends, Request

from app.models.user import User


def get_current_user(request: Request):
    return request.state.user

CurrentUserDep = Annotated[User, Depends(get_current_user)]