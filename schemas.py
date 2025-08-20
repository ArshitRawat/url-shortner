from pydantic import BaseModel, field_validator

class URLCreate(BaseModel):
    longURL: str

    @field_validator("longURL",mode="before")
    def ensure_https(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            return "https://" + value
        return value
