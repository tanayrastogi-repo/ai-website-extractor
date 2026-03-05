import pytest
import os
from src.formatter import render_markdown, save_markdown
from src.models import JobInfo

def test_render_markdown():
    job_info = JobInfo(
        job_title="Software Engineer",
        company_name="Google",
        location="Mountain View",
        about_company="Tech giant",
        key_responsibilities="Coding",
        qualifications=["Degree"],
        technical_skills=["Python"],
        soft_skills=["Teamwork"],
        contact_person="HR"
    )
    
    template = "# {{ job_title }} at {{ company_name }}\nQualifications: {{ qualifications[0] }}\nTech Skills: {{ technical_skills[0] }}"
    rendered = render_markdown(job_info, template)
    
    assert "# Software Engineer at Google" in rendered
    assert "Qualifications: Degree" in rendered
    assert "Tech Skills: Python" in rendered

def test_save_markdown(tmp_path):
    content = "# Test Job"
    filename = "test-job.md"
    filepath = tmp_path / filename
    
    save_markdown(content, str(filepath))
    
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        assert f.read() == content
