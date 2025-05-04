import os
import sys
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# 현재 test 폴더의 한 단계 위(프로젝트 루트)를 PYTHONPATH에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.application.services import (
    get_clusters_by_region,
    get_places_by_region_and_cluster,
    get_situation_definitions_by_place_id,
)

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_dependencies():
    # clusters용 더미 의존성: 항상 1개짜리 리스트 반환
    def fake_get_clusters():
        return lambda district, neighborhood: [
            {"cluster_id": 1, "cluster_name": "테스트 클러스터", "places_count": 3}
        ]

    # places용 더미 의존성: 항상 1개짜리 리스트 반환
    def fake_get_places():
        return lambda district, neighborhood, cluster_id: [
            {
                "place_id": 10,
                "adm_dong_code": 1111051500,
                "name": "테스트 식당",
                "category": "한식",
                "address": "테스트 주소",
                "opening_hours": "10:00-22:00",
                "naver_rating": 4.2,
            }
        ]

    # situation_definitions용 더미 의존성: 항상 1개짜리 리스트 반환
    def fake_get_defs():
        return lambda place_id, page=1: [
            {"situation_definition": "테스트 상황 설명"}
        ]

    # 의존성 오버라이드
    app.dependency_overrides[get_clusters_by_region] = fake_get_clusters
    app.dependency_overrides[get_places_by_region_and_cluster] = fake_get_places
    app.dependency_overrides[get_situation_definitions_by_place_id] = fake_get_defs

    yield

    # 테스트 후 정리
    app.dependency_overrides.clear()


def test_get_clusters_success():
    r = client.get("/regions/clusters?district=종로구&neighborhood=청운효자동")
    assert r.status_code == 200
    assert r.json() == [
        {"cluster_id": 1, "cluster_name": "테스트 클러스터", "places_count": 3}
    ]


def test_get_clusters_not_found():
    # 빈 리스트 반환하도록 의존성만 교체
    app.dependency_overrides[get_clusters_by_region] = lambda: (lambda d, n: [])
    r = client.get("/regions/clusters?district=없음구&neighborhood=없음동")
    assert r.status_code == 404


def test_get_places_success():
    r = client.get("/regions/places?district=종로구&neighborhood=청운효자동&cluster_id=1")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and data[0]["place_id"] == 10


def test_get_places_not_found():
    app.dependency_overrides[get_places_by_region_and_cluster] = lambda: (lambda d, n, s: [])
    r = client.get("/regions/places?district=종로구&neighborhood=청운효자동&cluster_id=999")
    assert r.status_code == 404


def test_get_situation_definitions_success():
    r = client.get("/regions/places/10?page=1")
    assert r.status_code == 200
    assert r.json() == [{"situation_definition": "테스트 상황 설명"}]


def test_get_situation_definitions_empty():
    # 정의가 없을 땐 빈 리스트(200) 반환
    app.dependency_overrides[get_situation_definitions_by_place_id] = lambda: (lambda p, pg=1: [])
    r = client.get("/regions/places/10?page=2")
    assert r.status_code == 200
    assert r.json() == []
