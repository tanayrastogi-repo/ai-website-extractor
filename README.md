# AI Website Extractor 🕵️‍♂️

An LLM-powered tool for extracting structured data from websites and formatting it into customizable Markdown templates.

## Overview
This project uses **Google Gemini 2.5 Flash** to analyze raw website content, extract key information (such as job postings), and render it through a flexible templating system. It features an interactive UI built with **Marimo**.

## Features
- **Intelligent Extraction:** Uses Gemini to identify and structure data from messy HTML.
- **Interactive UI:** A real-time web interface for inputting URLs and editing templates.
- **Customizable Formatting:** Support for Jinja2-based Markdown templates to control output structure.
- **Automated Scraping:** Built-in HTML fetching and cleaning pipeline.

## Getting Started

### Prerequisites
- Python 3.12 or higher.
- A Google Gemini API key.

### Installation
1. Clone the repository.
2. Install dependencies using [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```
3. Create a `.env` file in the root directory and add your API key:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

### Usage
Run the interactive application:
```bash
uv run marimo run app.py
```
Open the provided URL in your browser to start extracting data.

## Project Structure
- `app.py`: The main Marimo interactive application.
- `src/`: Core logic including scraping, extraction (LLM), and formatting.
- `extractions/`: Default directory where generated Markdown files are saved.
- `tests/`: Automated test suite.
