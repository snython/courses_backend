from pydantic import BaseModel
from typing import Optional
from .address import AddressDTO

class AddressDTO(BaseModel):
    name: Optional[str] = None
    location: Optional[AddressDTO] = None