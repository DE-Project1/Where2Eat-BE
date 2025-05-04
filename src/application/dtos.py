# src/application/dtos.py

from pydantic import BaseModel, Field
from typing import Optional

class ClusterDTO(BaseModel):
    cluster_id: int = Field(..., description="클러스터 ID")
    cluster_name: str = Field(..., description="클러스터 이름")
    places_count: int = Field(..., description="클러스터별 장소 수")


class PlaceDTO(BaseModel):
    place_id: int = Field(..., description="장소 고유 ID")
    adm_dong_code: float = Field(..., description="행정동코드")
    name: str = Field(..., description="장소명")
    category: Optional[str] = Field(None, description="카테고리")
    address: Optional[str] = Field(None, description="주소")
    opening_hours: Optional[str] = Field(None, description="영업 시간")
    naver_rating: float | None = None

class SituationDefinitionDTO(BaseModel):
    situation_definition: Optional[str] = Field(None, description="리뷰 상황 설명")
