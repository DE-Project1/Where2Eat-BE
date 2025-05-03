# ─── Builder Stage ───────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:debian-slim AS builder
WORKDIR /app

# 종속성 설치(캐시 레이어)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# 애플리케이션 코드 추가
COPY . .

# ─── Runtime Stage ──────────────────────────────────────────────
FROM python:3.11-slim
WORKDIR /app

# 빌더에서 설치된 .venv와 코드만 복사
COPY --from=builder /app /app

# .venv/bin을 PATH에 추가
ENV PATH="/app/.venv/bin:${PATH}"

# FastAPI 서버 실행
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
