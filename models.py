"""
This file contains data models for the digital menu system.
Since we're using JSON-based storage, these are primarily for documentation
and future database migration purposes.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Dish:
    """Represents a dish in a menu section"""
    id: str
    name: str
    description: str
    price: str
    image: Optional[str] = None

@dataclass
class MenuSection:
    """Represents a section in a restaurant menu"""
    id: str
    name: str
    dishes: List[Dish]

@dataclass
class Menu:
    """Represents a complete restaurant menu"""
    sections: List[MenuSection]

@dataclass
class Restaurant:
    """Represents a restaurant with its details and menu"""
    id: str
    name: str
    description: str
    logo: Optional[str]
    address: str
    phone: str
    email: str
    instagram: str
    facebook: str
    website: str
    created_at: str
    visits: int
    menu: Menu
    updated_at: Optional[str] = None

# JSON Schema for validation (future use)
RESTAURANT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "logo": {"type": ["string", "null"]},
        "address": {"type": "string"},
        "phone": {"type": "string"},
        "email": {"type": "string"},
        "instagram": {"type": "string"},
        "facebook": {"type": "string"},
        "website": {"type": "string"},
        "created_at": {"type": "string"},
        "visits": {"type": "integer"},
        "menu": {
            "type": "object",
            "properties": {
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "dishes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "price": {"type": "string"},
                                        "image": {"type": ["string", "null"]}
                                    },
                                    "required": ["id", "name", "description", "price"]
                                }
                            }
                        },
                        "required": ["id", "name", "dishes"]
                    }
                }
            },
            "required": ["sections"]
        }
    },
    "required": ["id", "name", "description", "created_at", "visits", "menu"]
}
