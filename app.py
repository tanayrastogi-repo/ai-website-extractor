import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from src.scraper import fetch_html, extract_clean_text
    from src.extraction import extract_job_data
    from src.formatter import render_markdown, save_markdown
    import os
    import ollama

    # Dynamic Model Discovery for Ollama
    try:
        ollama_models = [m.model for m in ollama.list().models]
    except Exception:
        ollama_models = []
    return (
        extract_clean_text,
        extract_job_data,
        fetch_html,
        mo,
        ollama_models,
        render_markdown,
        save_markdown,
    )


@app.cell
def _(mo):
    mo.md("""
    # 🕵️‍♂️ AI Job Scraper
    """)
    return


@app.cell
def _(mo):
    url_input = mo.ui.text(
        label="Job Description URL",
        placeholder="https://careers.google.com/jobs/results/...",
    )
    extract_button = mo.ui.run_button(label="Extract Information")

    # LLM Provider Selection
    provider_select = mo.ui.dropdown(
        options=["Gemini", "Ollama"], value="Gemini", label="LLM Provider"
    )
    return extract_button, provider_select, url_input


@app.cell
def _(mo, ollama_models, provider_select):
    # Dynamic Model Selection
    gemini_models = ["gemini-2.5-flash", "gemini-2.0-pro-exp"]
    default_ollama = "gemma3:1b"

    # Ensure default_ollama is in the list if available
    available_ollama = ollama_models if ollama_models else ["No local models found"]

    _model_options = (
        gemini_models if provider_select.value == "Gemini" else available_ollama
    )

    _initial_model = (
        "gemini-2.5-flash"
        if provider_select.value == "Gemini"
        else (default_ollama if default_ollama in available_ollama else available_ollama[0])
    )

    model_select = mo.ui.dropdown(
        options=_model_options, value=_initial_model, label="Model Selection"
    )
    return (model_select,)


@app.cell
def _(mo):
    _default_template = """# {{ job_title }} - {{ company_name }}
    ## Overview
    - **Location:** {{ location }}
    - **Contact:** {{ contact_person if contact_person else 'N/A' }}

    ### About the Company
    {{ about_company }}

    ### Role Details
    #### Key Responsibilities
    {{ key_responsibilities }}

    #### Qualifications
    {% for qual in qualifications -%}
    - {{ qual }}
    {% endfor %}

    #### Requirements
    ##### Technical Skills
    {% for tech in technical_skills -%}
    - {{ tech }}
    {% endfor %}

    ##### Soft Skills
    {% for soft in soft_skills -%}
    - {{ soft }}
    {% endfor %}
    """
    template_editor = mo.ui.text_area(
        value=_default_template, label="Markdown Template", full_width=True
    )
    return (template_editor,)


@app.cell
def _(
    extract_button,
    mo,
    model_select,
    provider_select,
    template_editor,
    url_input,
):
    mo.vstack(
        [
            mo.hstack([url_input, extract_button], justify="start"),
            mo.hstack([provider_select, model_select], justify="start"),
            template_editor,
        ]
    )
    return


@app.cell
def _(
    extract_button,
    extract_clean_text,
    extract_job_data,
    fetch_html,
    mo,
    model_select,
    provider_select,
    render_markdown,
    save_markdown,
    template_editor,
    url_input,
):
    mo.stop(not extract_button.value, mo.md("Enter a URL and click 'Extract' to begin."))

    with mo.status.progress_bar(title="Extracting Job Data", subtitle="Fetching HTML...", total=3) as bar:
        try:
            # Step 1: Fetch and Clean
            html = fetch_html(url_input.value)
            clean_text = extract_clean_text(html)
            bar.update(subtitle=f"AI Extraction ({provider_select.value}: {model_select.value})...")

            # Step 2: AI Extraction
            job_info = extract_job_data(clean_text, provider=provider_select.value, model=model_select.value)
            bar.update(subtitle="Formatting Markdown...")

            # Step 3: Render and Save
            markdown_content = render_markdown(job_info, template_editor.value)

            # Save file
            safe_company = job_info.company_name.replace(" ", "_").lower()
            safe_title = job_info.job_title.replace(" ", "_").lower()
            filename = f"extractions/{safe_company}_{safe_title}.md"
            save_markdown(markdown_content, filename)

            bar.update(subtitle="Done!")

            result_view = mo.md(f"### Extraction Complete! \nSaved to `{filename}`\n\n--- \n{markdown_content}")
        except Exception as e:
            result_view = mo.md(f"❌ **Error:** {str(e)}")

    result_view
    return


if __name__ == "__main__":
    app.run()
