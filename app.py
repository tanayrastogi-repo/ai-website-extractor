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

    return (
        extract_clean_text,
        extract_job_data,
        fetch_html,
        mo,
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
    url_input = mo.ui.text(label="Job Description URL", placeholder="https://careers.google.com/jobs/results/...")
    extract_button = mo.ui.run_button(label="Extract Information")

    default_template = """# {{ job_title }} - {{ company_name }}
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
    template_editor = mo.ui.text_area(value=default_template, label="Markdown Template", full_width=True)

    mo.hstack([url_input, extract_button], justify="start")
    return extract_button, template_editor, url_input


@app.cell
def _(
    extract_button,
    extract_clean_text,
    extract_job_data,
    fetch_html,
    mo,
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
            bar.update(subtitle="AI Extraction (Gemini)...")

            # Step 2: AI Extraction
            job_info = extract_job_data(clean_text)
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
