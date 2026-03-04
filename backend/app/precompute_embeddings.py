# backend/app/similarity.py
import os
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from .db import get_conn


MODEL_NAME = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()                     
device = torch.device("cpu")    
model.to(device)


def embed_text(text: str) -> np.ndarray:
    inputs = tokenizer(
        text,
        truncation=True,
        max_length=512,
        return_tensors="pt",
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    hidden = outputs.last_hidden_state.squeeze(0)      

    pooled = hidden.mean(dim=0)                            

    vec = pooled.cpu().numpy().astype(np.float32)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


def store_embeddings() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, abstract FROM articles WHERE embedding IS NULL"
    )
    rows = cur.fetchall()

    for row in rows:
        emb = embed_text(row["abstract"]).tolist() 
        cur.execute(
            "UPDATE articles SET embedding = %s WHERE id = %s",
            (emb, row["id"]),
        )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    store_embeddings()