import pytest
from unittest.mock import patch, MagicMock
from src.extraction import extract_job_data
from src.models import JobInfo

def test_extract_job_data_gemini():
    # Mock text input
    text = "Software Engineer at Google in Mountain View."
    
    # Mock LLM response
    mock_job_info = JobInfo(
        job_title="Software Engineer",
        company_name="Google",
        location="Mountain View, CA",
        about_company="Search engine company",
        key_responsibilities="Code in Python",
        qualifications=["CS degree"],
        technical_skills=["Python"],
        soft_skills=["Teamwork"],
        contact_person=None
    )
    
    with patch("src.extraction.get_structured_llm") as mock_get_llm:
        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.return_value = mock_job_info
        mock_get_llm.return_value = mock_structured_llm
        
        with patch("src.extraction.ChatPromptTemplate.from_messages") as mock_prompt_class:
            mock_prompt = MagicMock()
            mock_prompt.__or__.return_value = mock_structured_llm
            mock_prompt_class.return_value = mock_prompt
            
            result = extract_job_data(text, provider="gemini", model="gemini-2.5-flash")
            
            assert isinstance(result, JobInfo)
            assert result.job_title == "Software Engineer"
            mock_get_llm.assert_called_once_with("gemini", "gemini-2.5-flash")

def test_extract_job_data_ollama():
    # Mock text input
    text = "Data Scientist at Startup."
    
    mock_job_info = JobInfo(
        job_title="Data Scientist",
        company_name="Startup",
        location="Remote",
        about_company="AI Startup",
        key_responsibilities="Build models",
        qualifications=["PhD"],
        technical_skills=["Python"],
        soft_skills=["Communication"],
        contact_person=None
    )
    
    with patch("src.extraction.get_structured_llm") as mock_get_llm:
        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.return_value = mock_job_info
        mock_get_llm.return_value = mock_structured_llm
        
        with patch("src.extraction.ChatPromptTemplate.from_messages") as mock_prompt_class:
            mock_prompt = MagicMock()
            mock_prompt.__or__.return_value = mock_structured_llm
            mock_prompt_class.return_value = mock_prompt
            
            result = extract_job_data(text, provider="ollama", model="llama3.3")
            
            assert isinstance(result, JobInfo)
            assert result.job_title == "Data Scientist"
            mock_get_llm.assert_called_once_with("ollama", "llama3.3")
