from pydantic import BaseModel

class MachineData(BaseModel):
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float
    lifecycle: float  
    operational_time: float  
