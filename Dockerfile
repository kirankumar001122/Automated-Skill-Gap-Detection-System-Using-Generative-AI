# Multi-stage build for the Autonomous Coding Agent

# Stage 1: Backend
FROM python:3.10-slim as backend

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose backend port
EXPOSE 8000

# Backend health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Stage 2: Frontend
FROM node:18-slim as frontend

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci --only=production

# Copy frontend code
COPY frontend/ .

# Build frontend
RUN npm run build

# Stage 3: Final application
FROM nginx:alpine

# Copy frontend build
COPY --from=frontend /app/frontend/out /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose frontend port
EXPOSE 3000

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
