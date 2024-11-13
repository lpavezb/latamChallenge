from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator
from typing import List

OPERAS=["Aerolineas Argentinas", "Aeromexico", "Air Canada", "Air France", "Alitalia", "American Airlines", "Austral", "Avianca", "British Airways", "Copa Air", "Delta Air", "Gol Trans", "Grupo LATAM", "Iberia", "JetSmart SPA", "K.L.M.", "Lacsa", "Latin American Wings", "Oceanair Linhas Aereas", "Plus Ultra Lineas Aereas", "Qantas Airways", "Sky Airline", "United Airlines"]
TIPOS_VUELO=["I", "N"]

val_dict = {"OPERA": OPERAS, "TIPOVUELO": TIPOS_VUELO}

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int
    
    @field_validator("OPERA", "TIPOVUELO")
    @classmethod
    def str_fields_must_be_valid(cls, field: str, info: ValidationInfo) -> str:
        if not (field in val_dict[info.field_name]):
            raise ValueError(f"invalid {info.field_name}: {field}")
        return field
    
    @field_validator("MES")
    @classmethod
    def mes_must_be_valid(cls, mes: int) -> str:
        if mes < 1 or mes > 12:
            raise ValueError(f"invalid MES: {mes}")
        return mes

class Flights(BaseModel):
    flights: List[Flight]

if __name__ == "__main__":
    test_data = {        
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "O", 
                    "MES": 13
                }
            ]
        }
    try:
        Flights(**test_data)  
    except ValidationError as e:
        print("error")
        print(e.errors())