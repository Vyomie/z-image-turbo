#!/usr/bin/env bash
set -euo pipefail

# ── Configuration (edit these) ──────────────────────────────────────────
PROJECT_ID="${GCP_PROJECT_ID:?Set GCP_PROJECT_ID}"
REGION="${GCP_REGION:-europe-west4}"
SERVICE_NAME="z-image-turbo"
GCS_BUCKET="${GCS_BUCKET:?Set GCS_BUCKET}"
REPO_NAME="z-image-turbo"
IMAGE="europe-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"

echo "==> Creating Artifact Registry repo (if needed)..."
gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location=europe \
    --project="$PROJECT_ID" 2>/dev/null || true

echo "==> Creating GCS bucket (if needed)..."
gcloud storage buckets create "gs://${GCS_BUCKET}" \
    --project="$PROJECT_ID" \
    --location="$REGION" 2>/dev/null || true

echo "==> Building with Cloud Build (GPU-capable image, ~10 min first time)..."
gcloud builds submit . \
    --tag "$IMAGE" \
    --project "$PROJECT_ID" \
    --machine-type=e2-highcpu-32 \
    --timeout=1800

echo "==> Deploying to Cloud Run (GPU)..."
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE" \
    --project "$PROJECT_ID" \
    --region "$REGION" \
    --platform managed \
    --gpu 1 \
    --gpu-type nvidia-l4 \
    --cpu 8 \
    --memory 32Gi \
    --max-instances 3 \
    --min-instances 0 \
    --timeout 300 \
    --cpu-boost \
    --concurrency 1 \
    --port 8080 \
    --set-env-vars "GCS_BUCKET=${GCS_BUCKET}" \
    --allow-unauthenticated \
    --no-cpu-throttling \
    --no-gpu-zonal-redundancy

echo ""
echo "==> Done! Service URL:"
gcloud run services describe "$SERVICE_NAME" \
    --project "$PROJECT_ID" \
    --region "$REGION" \
    --format="value(status.url)"
