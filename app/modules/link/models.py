from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, String, Text, text

from app.db.base import Base
from app.db.mixins import BaseFeaturesMixin


class Link(Base, BaseFeaturesMixin):
    __tablename__ = "lnk_url"

    long_url = Column(Text, nullable=False)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    expired_on = Column(
        TIMESTAMP(timezone=False),
        server_default=text("now()"),
        default=datetime.utcnow,
        nullable=False,
    )
    last_accessed_at = Column(TIMESTAMP(timezone=False))
    ip_address = Column(String(16))


class BlacklistedDomain(Base, BaseFeaturesMixin):
    __tablename__ = "lnk_blacklisted_domain"

    domain_name = Column(String(100), unique=True, index=True, nullable=False)
