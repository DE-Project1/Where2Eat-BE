from pydantic import BaseModel, Field
from typing import List, Optional


class Place(BaseModel):
    place_id: int = Field(..., description="장소 고유 ID")
    adm_dong_code: int = Field(..., description="행정동 코드")
    name: str = Field(..., description="장소명")
    category: str = Field(..., description="카테고리")
    address: str = Field(..., description="주소")
    opening_hours: Optional[str] = None
    naver_rating: Optional[float] = None


class Region(BaseModel):
    adm_dong_code: int = Field(..., description="행정동 코드")
    district: str = Field(..., description="시군구명")
    neighborhood: str = Field(..., description="읍면동명")

class Review(BaseModel):
    place_id: int = Field(..., description="장소 고유 ID")
    visit_count: Optional[float] = None
    content_nouns: Optional[List[str]] = None
    situation_definition: Optional[str] = None
    situation_cluster: Optional[int] = None
    cluster_name: Optional[str] = None
