# 단일 스테이지: Astral uv 베이스 이미지 사용
FROM ghcr.io/astral-sh/uv:latest

# 컨테이너 내 작업 디렉터리
WORKDIR /app

# 1) 의존성 잠금 파일 복사 및 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# 2) 애플리케이션 코드 복사
COPY . .

# 3) .venv/bin 을 PATH 에 추가
ENV PATH="/app/.venv/bin:${PATH}"

# 4) 애플리케이션 포트
EXPOSE 8000

# 5) FastAPI 서버 실행
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
