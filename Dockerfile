FROM python:3.12-slim AS builder
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv \
	&& uv venv /opt/venv \
	&& uv export --locked --no-dev --format requirements-txt > /tmp/requirements.txt \
	&& uv pip install --python /opt/venv/bin/python -r /tmp/requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
COPY --from=builder /opt/venv /opt/venv

CMD ["sh"]