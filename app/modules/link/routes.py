from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.modules.link.crud import crud_create_short_link, crud_get_long_url
from app.modules.link.schema import LinkBase, LinkCreate

router = APIRouter()


@router.get(
    "/{short_code}",
    status_code=status.HTTP_302_FOUND,
    name="Redirect to the original URL",
)
async def redirect_link(
    short_code: str, db: AsyncSession = Depends(get_db)
) -> RedirectResponse:
    response = await crud_get_long_url(db, short_code)
    # For locust only uncomment that :
    # return {"response": f"{response}"}
    return RedirectResponse(url=f"{response}", status_code=status.HTTP_302_FOUND)


@router.post(
    "/links",
    status_code=status.HTTP_201_CREATED,
    response_model=LinkCreate,
    name="Create a short URL",
)
async def create_short_link(
    link: LinkBase, request: Request, db: AsyncSession = Depends(get_db)
) -> LinkCreate:
    return await crud_create_short_link(db, request, link.long_url)
