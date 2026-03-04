import numpy as np
from .db import get_conn


def get_random_article():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, url FROM articles ORDER BY random() LIMIT 1"
    )
    article = cur.fetchone()
    cur.close()
    conn.close()
    return article


def get_top_k_similar_articles(base_id: int, k: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT embedding FROM articles WHERE id = %s", (base_id,)
    )
    base_row = cur.fetchone()
    if not base_row or not base_row["embedding"]:
        cur.close()
        conn.close()
        return []

    base_emb = np.array(base_row["embedding"], dtype=np.float32)

    cur.execute(
        "SELECT id, title, url, embedding FROM articles WHERE id <> %s",
        (base_id,),
    )
    candidates = cur.fetchall()

    sims = []
    for cand in candidates:
        if not cand["embedding"]:
            continue
        emb = np.array(cand["embedding"], dtype=np.float32)
        sim = np.dot(base_emb, emb)
        sims.append((sim, cand))

    top = sorted(sims, key=lambda x: x[0], reverse=True)[:k]

    cur.close()
    conn.close()
    return [c for _, c in top]