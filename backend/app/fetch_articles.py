import os
import httpx
import xml.etree.ElementTree as ET
from .db import get_conn

ARXIV_QUERY = "cat:cs.LG"          
MAX_RESULTS = 500                  

BASE_URL = "https://export.arxiv.org/api/query"


def fetch_arXiv() -> str:
    params = {
        "search_query": ARXIV_QUERY,
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    resp = httpx.get(
        BASE_URL,
        params=params,
        timeout=30.0,
        follow_redirects=True,
    )
    resp.raise_for_status()
    return resp.text


def parse_and_store(xml_data: str) -> None:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_data)

    conn = get_conn()
    cur = conn.cursor()

    for entry in root.findall("atom:entry", ns):
        arXiv_id = entry.find("atom:id", ns).text.split("/")[-1]

        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")

        url = entry.find("atom:id", ns).text.strip()

        abstract = entry.find("atom:summary", ns).text.strip().replace("\n", " ")

        cur.execute(
            """
            INSERT INTO articles (arXiv_id, title, url, abstract)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (arXiv_id) DO NOTHING
            """,
            (arXiv_id, title, url, abstract),
        )

    conn.commit()
    cur.close()
    conn.close()


def fetch() -> None:
    xml = fetch_arXiv()
    parse_and_store(xml)


if __name__ == "__main__":
    fetch()