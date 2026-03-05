import pytest
from src.scraper import fetch_html, extract_clean_text
from unittest.mock import patch, MagicMock

def test_fetch_html_success():
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Job Content</body></html>"
        mock_get.return_value = mock_response
        
        result = fetch_html("https://example.com/job")
        assert result == "<html><body>Job Content</body></html>"

def test_fetch_html_failure():
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception, match="Failed to fetch URL"):
            fetch_html("https://example.com/job")

def test_extract_clean_text():
    html = """
    <html>
        <head><style>body {color: red;}</style></head>
        <body>
            <h1>Software Engineer</h1>
            <p>We are looking for a developer.</p>
            <script>alert('hello');</script>
        </body>
    </html>
    """
    clean_text = extract_clean_text(html)
    assert "Software Engineer" in clean_text
    assert "We are looking for a developer." in clean_text
    assert "alert('hello')" not in clean_text
    assert "body {color: red;}" not in clean_text

@pytest.mark.parametrize("url", [
    "https://hedvig.teamtailor.com/jobs/7249655-data-scientist",
    "https://us.wd103.myworkdayjobs.com/tobii_dynavox/job/Stockholm/BI-Analyst_JR100923?source=LinkedIn",
    "https://emp.jobylon.com/jobs/341841-postnord-sverige-verksamhetsutvecklare-prognoser-logistik-flera-orter-mojliga/",
    "https://jobs.scania.com/job/S%C3%B6dert%C3%A4lje-Automation-Engineer-151-38/1370133233/",
])
def test_real_world_scraping(url):
    """Integration test to verify scraping and cleaning of real-world job posting URLs."""
    html = fetch_html(url)
    clean_text = extract_clean_text(html)
    
    # Validation logic
    assert clean_text is not None
    assert len(clean_text) > 50, f"Extracted text from {url} is too short ({len(clean_text)} chars). Content: {clean_text[:100]}"
    assert "<script" not in clean_text.lower()
    assert "<style" not in clean_text.lower()
    
    # Optional: Print length for analysis during test run
    print(f"\nURL: {url}")
    print(f"Extracted length: {len(clean_text)}")
    print(f"Snippet: {clean_text[:200]}...")
