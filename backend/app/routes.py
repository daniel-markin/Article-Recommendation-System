# backend/app/routes.py
from fastapi import APIRouter, HTTPException
from .get_articles import (
    get_random_article,
    get_top_k_similar_articles,
)


router = APIRouter()


@router.get("/random")
def process_random_article():
    article = get_random_article()
    if not article:
        raise HTTPException(status_code=404, detail="Статьи не найдены")
    return {"id": article["id"], "title": article["title"], "url": article["url"]}


@router.get("/similar/{article_id}")
def process_similar_articles(article_id: int):
    similar = get_top_k_similar_articles(article_id, k=5)
    return [
        {"title": a["title"], "url": a["url"]} for a in similar
    ]