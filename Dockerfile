FROM python:3.11-slim

RUN pip install --no-cache-dir uv

WORKDIR /validation

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY scripts/ ./scripts/
COPY shacl/ ./shacl/

ENTRYPOINT ["uv", "run", "scripts/validate.py"]
CMD ["--help"]
