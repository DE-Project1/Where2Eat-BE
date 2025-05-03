from typing import List, Optional
from src.domain.entities import Place, Region, Review

class PlaceRepository:
    def get(self, place_id: int) -> Optional[Place]:
        raise NotImplementedError

class RegionRepository:
    def get(self, adm_dong_code: int) -> Optional[Region]:
        raise NotImplementedError

class ReviewRepository:
    def list(self, place_id: int, limit: int) -> List[Review]:
        raise NotImplementedError