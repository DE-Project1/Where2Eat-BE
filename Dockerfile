# syntax=docker/dockerfile:1

# 1) Python 3.11 및 uv 환경 이미지
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# 2) 의존성 메타파일만 복사 & lock된 의존성만 먼저 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project --locked --no-cache

# 3) 애플리케이션 코드 전체 복사
COPY . .

# 4) 프로젝트 자체도 설치 (최종 검증)
RUN uv sync --locked --no-cache

# 5) .venv/bin 을 PATH 에 추가
ENV PATH="/app/.venv/bin:${PATH}"

# 6) 8000 포트 노출
EXPOSE 8000

# 7) FastAPI 앱 실행
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
