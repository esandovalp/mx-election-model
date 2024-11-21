# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    JUPYTER_PATH=/home/jupyter/.local/share/jupyter \
    JUPYTER_CONFIG_DIR=/home/jupyter/.jupyter \
    JUPYTER_DATA_DIR=/home/jupyter/.local/share/jupyter \
    JUPYTER_RUNTIME_DIR=/tmp/jupyter_runtime

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -ms /bin/bash jupyter

# Create necessary directories with correct permissions
RUN mkdir -p /home/jupyter/.local/share/jupyter/kernels \
    && mkdir -p /home/jupyter/.jupyter \
    && mkdir -p /tmp/jupyter_runtime \
    && chown -R jupyter:jupyter /home/jupyter/.local \
    && chown -R jupyter:jupyter /home/jupyter/.jupyter \
    && chown -R jupyter:jupyter /tmp/jupyter_runtime

# Switch to non-root user
USER jupyter

# Create and activate virtual environment
ENV VIRTUAL_ENV=/home/jupyter/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip and install Python packages
COPY --chown=jupyter:jupyter requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set up matplotlib configuration
RUN mkdir -p /home/jupyter/.config/matplotlib && \
    echo "backend: Agg" > /home/jupyter/.config/matplotlib/matplotlibrc

# Expose Jupyter port
EXPOSE 8888

# Set working directory permissions
WORKDIR /app

# Command to keep container running
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]