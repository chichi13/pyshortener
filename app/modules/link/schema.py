from pydantic import AnyHttpUrl, BaseModel


class OrmTrue(BaseModel):
    class Config:
        orm_mode = True


class LinkBase(BaseModel):
    long_url: AnyHttpUrl | None = None


class LinkCreate(OrmTrue):
    short_code: str
