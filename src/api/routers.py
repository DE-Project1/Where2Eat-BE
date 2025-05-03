from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from src.application.dtos import ClusterDTO, PlaceDTO, SituationDefinitionDTO
from src.application.services import (
    get_clusters_by_region,
    get_places_by_region_and_cluster,
    get_situation_definitions_by_place_id,
)

router = APIRouter(prefix="/regions", tags=["regions"])

@router.get(
    "/clusters",
    response_model=List[ClusterDTO],
    summary="행정구역별 상황 클러스터 리스트 조회",
    description="district(시군구명)와 neighborhood(읍면동명)을 받아, 해당 지역에 속한 상황 클러스터 목록을 반환합니다."
)
def select_region_for_clusters(
    district: str = Query(..., description="시군구명"),
    neighborhood: str = Query(..., description="읍면동명"),
    get_clusters=Depends(get_clusters_by_region),
):
    clusters = get_clusters(district, neighborhood)
    if not clusters:
        raise HTTPException(status_code=404, detail="No clusters found")
    return clusters


@router.get(
    "/places",
    response_model=List[PlaceDTO],
    summary="클러스터별 장소 리스트 조회",
    description="district, neighborhood, cluster_id를 받아, 해당 클러스터에 속한 장소 목록을 반환합니다."
)
def select_region_and_cluster_for_places(
    district: str = Query(..., description="시군구명"),
    neighborhood: str = Query(..., description="읍면동명"),
    cluster_id: int = Query(..., description="상황 클러스터 ID"),
    get_places=Depends(get_places_by_region_and_cluster),
):
    places = get_places(district, neighborhood, cluster_id)
    if not places:
        raise HTTPException(status_code=404, detail="No places found")
    return places


@router.get(
    "/places/{place_id}",
    response_model=List[SituationDefinitionDTO],
    summary="장소별 리뷰 상황 설명 조회 (페이지네이션)",
    description="place_id와 page를 받아, 해당 장소의 리뷰 상황 설명을 최대 10개씩 페이징해서 반환합니다."
)
def get_situation_definitions_of_place(
    place_id: int,
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    get_situation_definitions=Depends(get_situation_definitions_by_place_id),
):
    results = get_situation_definitions(place_id, page)
    # 페이지에 결과가 없더라도 빈 리스트 반환
    return results