# ============================================================
# Stage 1: Use Python 3.12 on a lightweight Linux (Debian slim)
# ============================================================
# "FROM" = start with this base image (pre-built OS + Python)
# python:3.12-slim = Python 3.12 on a minimal Debian Linux (~150MB)
# vs python:3.12 which is ~900MB (includes compilers, docs, etc.)
FROM python:3.12-slim

# ============================================================
# Stage 2: Set the working directory inside the container
# ============================================================
# All following commands (COPY, RUN, CMD) happen inside /app
# Think of it like: cd /app
WORKDIR /app

# ============================================================
# Stage 3: Install dependencies FIRST (for caching)
# ============================================================
# WHY copy requirements.txt separately before copying all code?
# Docker caches each layer. If your code changes but requirements.txt
# doesn't, Docker reuses the cached pip install layer — saves minutes.
#
# If we copied everything first, ANY code change would re-trigger
# pip install even though dependencies didn't change.
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir  = don't store pip's download cache (saves ~50MB)
# --no-compile    = skip generating .pyc files (saves space)
RUN pip install --no-cache-dir --no-compile -r requirements.txt

# ============================================================
# Stage 4: Copy the rest of your application code
# ============================================================
# "." = copy everything from your project folder into /app
# .dockerignore controls what gets excluded (like .gitignore)
COPY . .

# ============================================================
# Stage 5: Create the media directory
# ============================================================
# Your app uses /media for uploaded files — ensure it exists
RUN mkdir -p media/profile_pics

# ============================================================
# Stage 6: Tell Docker which port the app uses
# ============================================================
# EXPOSE doesn't actually publish the port — it's documentation
# for other developers and tools like Railway to know which port
# your app listens on
EXPOSE 8000

# ============================================================
# Stage 7: Define the startup command
# ============================================================
# CMD = the command that runs when the container starts
# This is the same as your Procfile, but for Docker
#
# "0.0.0.0" = listen on all interfaces (required in containers)
# "${PORT:-8000}" = use $PORT env var if set, otherwise default to 8000
#   - Railway/Heroku set $PORT automatically
#   - Running locally defaults to 8000
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
