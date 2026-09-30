from pydantic import BaseModel,Field,ConfigDict
from typing import Literal
Hazard=Literal['auto','rain','heat','cyclone']
class Lead(BaseModel):
    day:int;fci:int;p_bust:float;hazard:str;band:str
    conformal_interval:list[float];error_unit:str;error_p90_class:str
class Region(BaseModel):
    id:str;name:str;name_hi:str;states:list[str];trust_horizon_day:int|None;leads:list[Lead]
class Confidence(BaseModel):
    init:str;hazard:str;regions:list[Region];data_mode:str;regime:str;init_times:list[str];model:str
class FeedbackInput(BaseModel):
    region:str;lead:int=Field(ge=1,le=10);verdict:Literal['Bust confirmed','False alarm'];init:str;hazard:str
class Feedback(FeedbackInput):
    id:str;created_at:str
class Explanation(BaseModel):
    model_config=ConfigDict(extra='allow')
    region:str;day:int;fci:int;p_bust:float;drivers:list[dict];counterfactual:dict;narrative:dict;analogs:list[dict];data_mode:str