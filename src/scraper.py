import httpx
from bs4 import BeautifulSoup

def fetch_html(url: str) -> str:
    """Fetches raw HTML from a URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = httpx.get(url, headers=headers, follow_redirects=True)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url} (Status: {response.status_code})")
    return response.text

def extract_clean_text(html: str) -> str:
    """Extracts clean text from HTML by removing scripts and styles."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    # Get text and clean up whitespace
    text = soup.get_text(separator=" ")
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    clean_text = "\n".join(chunk for chunk in chunks if chunk)
    
    return clean_text
