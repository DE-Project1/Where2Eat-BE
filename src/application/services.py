from typing import List, Dict, Any
from src.infrastructure.db import db
import math

def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj

# 구/동을 받아 해당 지역의 클러스터(cluster_id, cluster_name, places_count) 조회
def get_clusters_by_region():
    def uc(district: str, neighborhood: str) -> List[Dict[str, Any]]:
        # 1) 행정동 코드 조회
        region = db["region_map"].find_one(
            {"district": district, "neighborhood": neighborhood},
            {"adm_dong_code": 1, "_id": 0},
        )
        if not region:
            return []

        adm_dong = region["adm_dong_code"]

        # 2) 해당 동의 모든 place_id 리스트 (인덱스가 있다면 매우 빠름)
        place_ids = [
            doc["place_id"]
            for doc in db["place_info"].find(
                {"adm_dong_code": adm_dong},
                {"place_id": 1, "_id": 0},
            )
        ]
        if not place_ids:
            return []

        # 3) reviews 컬렉션만으로 그룹화 → 고유 place_id 세트로 묶은 뒤 count
        pipeline = [
            {"$match": {"place_id": {"$in": place_ids}}},
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
        return clean_nan(result)

    return uc

# 구/동과 클러스터 ID를 받아 해당 클러스터의 장소 리스트를 빠르게 조회
def get_places_by_region_and_cluster():
    def uc(district: str, neighborhood: str, cluster_id: int) -> List[Dict[str, Any]]:
        # 1) 행정동 코드 조회
        region = db["region_map"].find_one(
            {"district": district, "neighborhood": neighborhood},
            {"adm_dong_code": 1, "_id": 0},
        )
        if not region:
            return []

        adm_dong = region["adm_dong_code"]

        # 2) 해당 동의 place_id 목록 조회 (adm_dong_code 인덱스 활용)
        place_ids = db["place_info"].distinct(
            "place_id",
            {"adm_dong_code": adm_dong}
        )
        if not place_ids:
            return []

        # 3) reviews에서 해당 cluster_id와 place_id 필터 후 고유 place_id만 추출 (복합 인덱스 활용)
        matched_place_ids = db["reviews"].distinct(
            "place_id",
            {
                "place_id": {"$in": place_ids},
                "situation_cluster": cluster_id
            }
        )
        if not matched_place_ids:
            return []

        # 4) 최종 place_info 문서 조회하여 반환 (_id 제외)
        places = list(db["place_info"].find(
            {"place_id": {"$in": matched_place_ids}},
            {"_id": 0}
        ))
        return clean_nan(places)

    return uc

# 장소 ID로 리뷰의 situation_definition을 10개씩 페이징 조회
def get_situation_definitions_by_place_id():
    def uc(place_id: int, page: int = 1) -> List[Dict[str, Any]]:
        # 페이지 계산
        skip = (page - 1) * 10

        # situation_definition만 추출하여 skip/limit 적용
        pipeline = [
            {"$match": {"place_id": place_id}},
            {"$project": {"situation_definition": 1, "_id": 0}},
            {"$skip": skip},
            {"$limit": 10},
        ]
        result = list(db["reviews"].aggregate(pipeline))
        return clean_nan(result)

    return uc
