from typing import List, Dict, Any
from src.infrastructure.db import db
import math

# 공통 유틸: NaN 처리
def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj

def with_clean_nan(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return clean_nan(result)
    return wrapper

# 클러스터 조회: 구/동 → 클러스터 목록(cluster_id, cluster_name, places_count)
def get_clusters_by_region():
    @with_clean_nan
    def uc(district: str, neighborhood: str) -> List[Dict[str, Any]]:
        # 행정동 코드 조회
        region = db["region_map"].find_one(
            {"district": district, "neighborhood": neighborhood},
            {"adm_dong_code": 1, "_id": 0},
        )
        if not region:
            return []

        adm_dong = region["adm_dong_code"]

        # reviews → place_info join + 필터 + 그룹핑 최적화
        pipeline = [
            {
                "$lookup": {
                    "from": "place_info",
                    "let": {"place_id": "$place_id"},
                    "pipeline": [
                        {"$match": {
                            "$expr": {"$eq": ["$place_id", "$$place_id"]},
                            "adm_dong_code": adm_dong
                        }},
                        {"$project": {"place_id": 1}}
                    ],
                    "as": "place_info"
                }
            },
            {"$match": {"place_info": {"$ne": []}}},
            {
                "$group": {
                    "_id": {
                        "cluster_id": "$situation_cluster",
                        "cluster_name": "$cluster_name",
                    },
                    "place_ids": {"$addToSet": "$place_id"},
                }
            },
            {
                "$project": {
                    "cluster_id": "$_id.cluster_id",
                    "cluster_name": "$_id.cluster_name",
                    "places_count": {"$size": "$place_ids"},
                    "_id": 0,
                }
            },
        ]

        result = list(db["reviews"].aggregate(pipeline))
        return result

    return uc

# 특정 클러스터의 장소 리스트: 구/동 + 클러스터 ID → 장소 리스트
def get_places_by_region_and_cluster():
    @with_clean_nan
    def uc(district: str, neighborhood: str, cluster_id: int) -> List[Dict[str, Any]]:
        # 행정동 코드 조회
        region = db["region_map"].find_one(
            {"district": district, "neighborhood": neighborhood},
            {"adm_dong_code": 1, "_id": 0},
        )
        if not region:
            return []

        adm_dong = region["adm_dong_code"]

        # 해당 adm_dong place_id 목록
        place_ids = db["place_info"].distinct("place_id", {"adm_dong_code": adm_dong})
        if not place_ids:
            return []

        # reviews에서 해당 cluster_id와 일치하는 place_id만 추출
        matched_place_ids = db["reviews"].distinct(
            "place_id",
            {
                "place_id": {"$in": place_ids},
                "situation_cluster": cluster_id
            }
        )
        if not matched_place_ids:
            return []

        # place_info에서 최종 데이터 조회
        places = list(db["place_info"].find(
            {"place_id": {"$in": matched_place_ids}},
            {"_id": 0}
        ))

        return places

    return uc

# 장소 ID로 situation_definition 페이징 조회
def get_situation_definitions_by_place_id():
    @with_clean_nan
    def uc(place_id: int, page: int = 1) -> List[Dict[str, Any]]:
        skip = (page - 1) * 10

        pipeline = [
            {"$match": {"place_id": place_id}},
            {"$project": {"situation_definition": 1, "_id": 0}},
            {"$skip": skip},
            {"$limit": 10},
        ]
        result = list(db["reviews"].aggregate(pipeline))
        return result

    return uc
