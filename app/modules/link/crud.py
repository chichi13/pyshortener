from datetime import datetime, timedelta
from urllib.parse import urlparse

from fastapi import HTTPException, Request, status
from pydantic import AnyHttpUrl
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.modules.link.models import BlacklistedDomain, Link
from app.services import strings
from app.tools.base58 import human_readable_string
from app.tools.expiry_method import storage


async def _update_accessed_at(db: AsyncSession, short_code):
    stmt = (
        update(Link)
        .where(Link.short_code == short_code)
        .values(last_accessed_at=datetime.utcnow())
    )
    await db.execute(stmt)
    await db.commit()


async def _check_blacklisted_domain(db: AsyncSession, long_url) -> None:
    domain_name: str = urlparse(long_url).netloc

    query = await db.execute(
        select(BlacklistedDomain).where(BlacklistedDomain.domain_name == domain_name)
    )
    if query.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.BLACKLISTED_DOMAIN
        )


async def crud_get_long_url(db: AsyncSession, short_code: str):
    long_url = storage.get_long_url(short_code)

    if long_url is None:
        query = await db.execute(select(Link).where(Link.short_code == short_code))
        result = query.scalars().first()

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        long_url = result.long_url

    storage.set_key(
        short_code,
        timedelta(days=settings.CACHE_EXPIRATION_DELAY),
        long_url,
    )

    await _update_accessed_at(db, short_code)

    return long_url


async def crud_create_short_link(
    db: AsyncSession, request: Request, long_url: AnyHttpUrl
):
    short_code: str = human_readable_string()
    expiration_date: datetime = datetime.utcnow() + timedelta(
        days=settings.LINK_EXPIRATION_DELAY
    )

    await _check_blacklisted_domain(db, long_url)

    db_link = Link(
        long_url=long_url,
        short_code=short_code,
        expired_on=expiration_date,
        ip_address=request.client.host,
    )

    stmt = select(Link).where(Link.short_code == short_code)
    result = await db.execute(stmt)

    # TODO: Find another way to do that
    if result.scalars().first():
        try:
            await crud_create_short_link(db, request, long_url)
        except RecursionError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=strings.NO_SHORTCODE
            )

    db.add(db_link)
    await db.commit()
    await db.flush()

    return db_link
