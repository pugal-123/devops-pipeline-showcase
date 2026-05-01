# ── Stage 1: Builder ────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .

# Install dependencies into a local folder (no system install)
RUN pip install --user --no-cache-dir -r requirements.txt


# ── Stage 2: Production ─────────────────────────────────────────
FROM python:3.11-alpine

# Security: create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy app source
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
ENV FLASK_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:5000/health || exit 1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
