import logging
from typing import List, Optional, Dict, Any
from pymongo.errors import PyMongoError

from src.domain.entities import Place, Region, Review
from src.domain.repositories import PlaceRepository, RegionRepository, ReviewRepository
from src.infrastructure.db import db

logger = logging.getLogger(__name__)

class MongoPlaceRepository(PlaceRepository):
    def get(self, place_id: int) -> Optional[Place]:
        try:
            doc = db["place_info"].find_one(
                {"place_id": place_id},
                {"_id": 0}
            )
            return Place(**doc) if doc else None

        except PyMongoError as e:
            logger.error("MongoPlaceRepository.get failed for place_id=%s: %s", place_id, e, exc_info=True)
            return None

class MongoRegionRepository(RegionRepository):
    def get(self, adm_dong_code: int) -> Optional[Region]:
        try:
            doc = db["region_map"].find_one(
                {"adm_dong_code": adm_dong_code},
                {"_id": 0}
            )
            return Region(**doc) if doc else None

        except PyMongoError as e:
            logger.error("MongoRegionRepository.get failed for adm_dong_code=%s: %s", adm_dong_code, e, exc_info=True)
            return None

class MongoReviewRepository(ReviewRepository):
    def list(self, place_id: int, limit: int) -> List[Review]:
        try:
            cursor = db["reviews"].find(
                {"place_id": place_id},
                {"_id": 0}
            ).limit(limit)
            return [Review(**doc) for doc in cursor]

        except PyMongoError as e:
            logger.error("MongoReviewRepository.list failed for place_id=%s: %s", place_id, e, exc_info=True)
            return []