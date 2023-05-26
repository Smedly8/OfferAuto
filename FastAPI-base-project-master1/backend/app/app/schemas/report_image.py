from app.schemas.base import BaseSchema

# Shared properties


class GettingReportImage(BaseSchema):
    id: int | None = None
    img: str | None = None
    # user: GettingUser | None = None
