import io
import os
import uuid
from datetime import timedelta

import torch
from diffusers import AutoPipelineForText2Image
from fastapi import FastAPI, HTTPException
from google.cloud import storage
from pydantic import BaseModel, Field

from styles import STYLES, build_prompt

# ── Config ──────────────────────────────────────────────────────────────
GCS_BUCKET = os.environ["GCS_BUCKET"]
MODEL_ID = os.getenv("MODEL_ID", "stabilityai/sdxl-turbo")
SIGNED_URL_EXPIRY_MINUTES = int(os.getenv("SIGNED_URL_EXPIRY_MINUTES", "60"))

# ── Load pipeline once at startup ───────────────────────────────────────
pipe = AutoPipelineForText2Image.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    variant="fp16",
)
pipe.to("cuda")

# ── GCS client ──────────────────────────────────────────────────────────
gcs = storage.Client()
bucket = gcs.bucket(GCS_BUCKET)

# ── FastAPI ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="Z Image Turbo",
    version="1.0.0",
    description="Scientific illustration generator for AI tutoring. "
    "Produces cartoonish yet scientifically accurate diagrams across disciplines.",
)


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    style: str = Field(default="biology")
    width: int = Field(default=512, ge=256, le=1024)
    height: int = Field(default=512, ge=256, le=1024)


class GenerateResponse(BaseModel):
    image_url: str
    style: str
    prompt_used: str


@app.get("/styles")
def list_styles():
    """Return available style presets."""
    return {
        name: {"prefix": s["prefix"], "suffix": s["suffix"]}
        for name, s in STYLES.items()
    }


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_ID, "gpu": torch.cuda.is_available()}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    try:
        styled = build_prompt(req.prompt, req.style)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    image = pipe(
        prompt=styled["prompt"],
        negative_prompt=styled["negative_prompt"],
        guidance_scale=styled["guidance_scale"],
        num_inference_steps=styled["num_inference_steps"],
        width=req.width,
        height=req.height,
    ).images[0]

    # Upload to GCS (in-memory only, never touches disk)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    blob_name = f"generations/{uuid.uuid4().hex}.png"
    blob = bucket.blob(blob_name)
    blob.upload_from_file(buf, content_type="image/png")

    signed_url = blob.generate_signed_url(
        expiration=timedelta(minutes=SIGNED_URL_EXPIRY_MINUTES),
        method="GET",
    )

    return GenerateResponse(
        image_url=signed_url,
        style=req.style,
        prompt_used=styled["prompt"],
    )
