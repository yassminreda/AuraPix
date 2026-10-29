
"""Load locally fine-tuned CLIP and BLIP models for AuraPix."""

import os
import torch
import streamlit as st
from transformers import (
    CLIPModel,
    CLIPProcessor,
    BlipForConditionalGeneration,
    BlipProcessor,
)

# Paths are relative to this file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

CLIP_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "best_model-20261029T021027Z-1-001",
    "best_model",
)

BLIP_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "best_model-20261029T021035Z-1-001",
    "best_model",
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_setting(name, default=""):
    """Read a setting from Streamlit Secrets or environment variables."""
    try:
        value = st.secrets.get(name, default)
        if value:
            return str(value).strip()
    except Exception:
        pass

    return os.getenv(name, default).strip()


def get_model_source(local_path, repo_setting, model_name):
    """
    Prefer local fine-tuned files when available.
    Otherwise use the configured private Hugging Face repository.
    """
    if os.path.isfile(os.path.join(local_path, "config.json")):
        if not os.path.isfile(
            os.path.join(local_path, "model.safetensors")
        ):
            raise FileNotFoundError(
                f"{model_name} weights were not found at: {local_path}"
            )

        return local_path, None

    repo_id = get_setting(repo_setting)
    token = get_setting("HF_TOKEN")

    if not repo_id:
        raise RuntimeError(
            f"{model_name} model is not available locally and "
            f"{repo_setting} is not configured in Streamlit Secrets."
        )

    if not token:
        raise RuntimeError(
            "HF_TOKEN is missing. Add it to Streamlit Secrets."
        )

    return repo_id, token


@st.cache_resource(show_spinner=False)
def load_clip():
    model_source, token = get_model_source(
        CLIP_MODEL_PATH,
        "CLIP_MODEL_REPO",
        "CLIP",
    )

    load_kwargs = {"use_safetensors": True}

    if token:
        load_kwargs["token"] = token
    else:
        load_kwargs["local_files_only"] = True

    model = CLIPModel.from_pretrained(
        model_source,
        **load_kwargs,
    ).to(DEVICE).eval()

    processor = CLIPProcessor.from_pretrained(
        model_source,
        **(
            {"token": token}
            if token
            else {"local_files_only": True}
        ),
    )

    return model, processor, DEVICE


@st.cache_resource(show_spinner=False)
def load_blip():
    model_source, token = get_model_source(
        BLIP_MODEL_PATH,
        "BLIP_MODEL_REPO",
        "BLIP",
    )

    load_kwargs = {"use_safetensors": True}

    if token:
        load_kwargs["token"] = token
    else:
        load_kwargs["local_files_only"] = True

    model = BlipForConditionalGeneration.from_pretrained(
        model_source,
        **load_kwargs,
    ).to(DEVICE).eval()

    processor = BlipProcessor.from_pretrained(
        model_source,
        **(
            {"token": token}
            if token
            else {"local_files_only": True}
        ),
    )

    return model, processor, DEVICE


def search_images(query, images, top_k=5):
    if not query or not query.strip() or not images:
        return []

    model, processor, device = load_clip()
    scores = []

    with torch.inference_mode():
        text_inputs = processor(
            text=[query.strip()],
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(device)

        text_features = model.get_text_features(**text_inputs)
        text_features = text_features / text_features.norm(
            dim=-1, keepdim=True
        ).clamp(min=1e-12)

        for start in range(0, len(images), 8):
            batch = images[start:start + 8]

            image_inputs = processor(
                images=batch,
                return_tensors="pt",
            ).to(device)

            image_features = model.get_image_features(**image_inputs)
            image_features = image_features / image_features.norm(
                dim=-1, keepdim=True
            ).clamp(min=1e-12)

            batch_scores = (
                image_features @ text_features.T
            ).squeeze(-1)

            scores.extend(batch_scores.cpu().tolist())

    return sorted(
        enumerate(scores),
        key=lambda item: item[1],
        reverse=True,
    )[:max(1, int(top_k))]


def caption_image(image):
    model, processor, device = load_blip()

    with torch.inference_mode():
        inputs = processor(
            images=image,
            return_tensors="pt",
        ).to(device)

        generated_ids = model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=3,
        )

    return processor.decode(
        generated_ids[0],
        skip_special_tokens=True,
    ).strip()

