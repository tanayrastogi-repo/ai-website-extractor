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
