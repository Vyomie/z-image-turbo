FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/model-cache

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.11 python3.11-venv python3-pip git \
        libgl1 libglib2.0-0 libxcb1 libsm6 libxext6 libxrender1 && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

WORKDIR /app

# Install Python deps (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download model weights into the image so cold starts are fast
ARG MODEL_ID=stabilityai/sdxl-turbo
RUN python3 -c "\
from diffusers import AutoPipelineForText2Image; \
import torch; \
AutoPipelineForText2Image.from_pretrained('${MODEL_ID}', torch_dtype=torch.float16, variant='fp16')"

# Copy app code
COPY styles.py app.py ./

EXPOSE 8080

CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
