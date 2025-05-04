import os, sys
import pytest

# 프로젝트 루트를 모듈 경로에 추가
sys.path.insert(0, os.getcwd())

# 테스트용 기본 환경 변수 설정
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")
os.environ.setdefault("MONGO_DB", "testdb")

@pytest.fixture(autouse=True)
def override_env_vars(monkeypatch):
    monkeypatch.setenv("MONGO_URI", os.environ["MONGO_URI"])
    monkeypatch.setenv("MONGO_DB", os.environ["MONGO_DB"])
    yield
