from typing import Annotated
from dotenv import load_dotenv
import httpx
from ddgs import DDGS
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import InjectedToolArg
from markdownify import markdownify
from tavily import TavilyClient

load_dotenv()

def fetch_webpage_content(url: str, timeout: float = 10.0) -> str:
    """Fetch and convert webpage content to markdown.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Webpage content as markdown
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = httpx.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return markdownify(response.text)
    except Exception as e:
        # return f"Error fetching content from {url}: {str(e)}"
        return ""


def fetch_webpage_using_webloader(url: str):
    loader = WebBaseLoader(url)
    # loader.requests_kwargs = {'verify': False}
    loader.requests_kwargs = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    }
    try:
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"Error fetching {url} with WebBaseLoader: {e}")
        return []


def duckduckgo_web_search(search_queries: list[str]):
    results = []
    with DDGS() as ddgs:
        for query in search_queries:
            for result in ddgs.text(query, max_results=2):
                url = result.get("href")
                content = fetch_webpage_content(url)
                if content != "":
                    results.append({
                        "search_query": query,
                        "title": result.get("title"),
                        "url": result.get("href"),
                        "snippet": content,
                        "source": "duckduckgo"
                    })

    return results


def duckduckgo_web_search_1(search_queries: list[str]):
    results = []
    with DDGS() as ddgs:
        for query in search_queries:
            for result in ddgs.text(query, max_results=2):
                url = result.get("href")
                document = fetch_webpage_using_webloader(url)
                results.append({
                    "search_query": query,
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "snippet": document[0].page_content,
                    "source": "duckduckgo"
                })
    return results


tavily_client = TavilyClient()


def tavily_search(search_queries: list[str]):
    results = []
    excluded = ["youtube.com", "facebook.com", "instagram.com"]
    for query in search_queries:
        search_results = tavily_client.search(query, max_results=3, exclude_domains=excluded)
        for result in search_results.get("results", []):
            url = result["url"]
            title = result["title"]
            if url.lower().endswith(".pdf"):
                continue
            # Fetch webpage content
            document = fetch_webpage_using_webloader(url)
            if document and len(document) > 0:
                results.append({
                    "search_query": query,
                    "title": title,
                    "url": url,
                    "snippet": document[0].page_content,
                    "source": "tavily"
                })
    return results

