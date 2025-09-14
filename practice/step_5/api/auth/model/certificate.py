from dataclasses import dataclass


@dataclass
class Certificate:
    id: int
    public_key: str
    encrypt_type: str
    status: str
    
