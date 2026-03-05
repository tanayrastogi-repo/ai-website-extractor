# 🕵️‍♂️ AI Job Scraper
   
An AI-powered tool that transforms messy job posting URLs into clean, structured Markdown files. It uses LLMs to intelligently parse responsibilities, qualifications, and skills from any careers page.

### Features
* **Multi-Model Support:** Choose between Google **Gemini** (Fast/Pro) or local **Ollama** models .

* **Custom Templates:** Use Jinja2-style templates to define exactly how your Markdown should be formatted.

* **Interactive UI:** Built with [Marimo](https://marimo.io/) for a reactive, notebook-like experience.


### 🛠️ Tech Stack
- **Interactive UI & Reactive Runner:** marimo
- **LLM Orchestration & Structured Output:** langchain
- **Google Gemini Model Integration:** langchain-google-genai
- **Local Ollama Model Integration:** langchain-ollama
- **Structured Data Modeling & Validation:** pydantic
- **HTML Scraping & HTTP Requests:** httpx
- **HTML Parsing & Text Cleaning:** beautifulsoup4
- **Markdown Templating Engine:** jinja2
- **Environment Variable Management:** python-dotenv
- **Automated Testing Framework:** pytest
- **Local Model Discovery:** ollama


## Getting Started

### 1. Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended)
- (Optional) [Ollama](https://ollama.com/) for local extraction.

### 2. Installation
git clone https://github.com/your-repo/ai-website-extractor.git
cd ai-website-extractor
uv sync

### 3. Configuration
Create a `.env` file in the root directory:
GOOGLE_API_KEY=your_gemini_api_key_here

### 4. Run the App
uv run marimo edit app.py

