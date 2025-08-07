# Copyright 2024 Firefly OSS
# Licensed under the Apache License, Version 2.0

FROM python:3.10-slim

LABEL org.opencontainers.image.title="Firefly SBOM Tool"
LABEL org.opencontainers.image.description="Comprehensive SBOM generation tool for Firefly Open Banking Platform"
LABEL org.opencontainers.image.vendor="Firefly OSS"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/firefly-oss/sbom-tool"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    maven \
    golang \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Flutter
RUN git clone https://github.com/flutter/flutter.git /usr/local/flutter --depth 1 --branch stable
ENV PATH="/usr/local/flutter/bin:${PATH}"

WORKDIR /app

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

# Create non-root user
RUN useradd -m -u 1000 sbom && chown -R sbom:sbom /app
USER sbom

ENTRYPOINT ["firefly-sbom"]
CMD ["--help"]
