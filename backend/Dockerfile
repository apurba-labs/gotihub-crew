# ==========================================
# STAGE 1: Dependency Compiler & Python Base
# ==========================================
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr for transparent logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install critical system dependencies needed for compilation or SQLite stability
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy package requirement definitions first to maximize layer caching benefits
COPY requirements.txt .

# Install dependencies directly into the system layer configuration space
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ==========================================
# STAGE 2: Secure Production Container Runtime
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Create a secure non-root system user profile to execute application processes safely
RUN useradd -u 1001 -m appuser

# Bring over installed dependencies from the compiler stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy the rest of the backend source files into the runtime container working room
COPY . .

# Create and lock permissions for SQLite data directory AFTER copying code
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data /app

# Switch runtime contexts execution over to the non-root profile
USER appuser

# Expose the internal API interface port matching your compose layout map
EXPOSE 8000

# Automated health check to ensure Uvicorn is successfully serving routes 
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Fire up the Uvicorn engine to serve your FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
