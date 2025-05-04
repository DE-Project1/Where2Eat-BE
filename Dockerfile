FROM python:3.11-slim

# 1. uv 설치를 위한 curl 및 ca-certificates 설치
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && curl -sSL https://github.com/astral-sh/uv/releases/download/0.7.2/uv-installer.sh | sh \
 && apt-get purge -y --auto-remove curl \
 && rm -rf /var/lib/apt/lists/*

# uv 바이너리 경로 등록
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# 프로젝트 메타데이터 및 잠금파일 복사
COPY pyproject.toml uv.lock ./

RUN uv sync

# 애플리케이션 소스 및 테스트 복사
COPY .env .
COPY src/ src/

# 애플리케이션 포트 노출 및 실행
EXPOSE 8000
CMD ["uv", "run", "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]