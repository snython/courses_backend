from pydantic import BaseModel
from typing import Optional

class AddressDTO(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None