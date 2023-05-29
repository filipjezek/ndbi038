import clip
import torch
from PIL import Image
import numpy as np
from pathlib import Path

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


def get_photo_features(file: str | Path | Image.Image):
    with torch.no_grad():
        image_input = preprocess(
            file if isinstance(file, Image.Image) else Image.open(file)
        ).unsqueeze(0).to(device)
        image_features = model.encode_image(image_input)
        image_features = image_features.cpu().detach().numpy().ravel()
        image_features /= np.linalg.norm(image_features,
                                         axis=-1, keepdims=True)
        return image_features


def get_text_features(query: str):
    text = clip.tokenize([query]).to(device)

    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().detach().numpy().ravel()
