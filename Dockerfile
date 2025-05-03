# syntax=docker/dockerfile:1

# 1. uv(Python 3.11) 베이스 이미지
FROM ghcr.io/astral-sh/uv:0.4.17-python3.11-bookworm-slim :contentReference[oaicite:0]{index=0}

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 의존성 메타파일 복사 & lock된 의존성만 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project --locked --no-cache

# 4. 애플리케이션 코드 복사
COPY . .

# 5. 프로젝트 자체도 설치(최종 검증)
RUN uv sync --locked --no-cache

# 6. .venv/bin을 PATH에 추가
ENV PATH="/app/.venv/bin:${PATH}"

# 7. 서비스 포트
EXPOSE 8000

# 8. uvicorn으로 FastAPI 앱 실행
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
