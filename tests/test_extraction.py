import pytest
from unittest.mock import patch, MagicMock
from src.extraction import extract_job_data
from src.models import JobInfo

def test_extract_job_data():
    # Mock text input
    text = "Software Engineer at Google in Mountain View. We build search engines. You will code in Python. Requirements: CS degree."
    
    # Mock LLM response
    mock_job_info = JobInfo(
        job_title="Software Engineer",
        company_name="Google",
        location="Mountain View, CA",
        about_company="Search engine company",
        key_responsibilities="Code in Python",
        qualifications="CS degree",
        requirements="Python knowledge",
        contact_person=None
    )
    
    with patch("src.extraction.ChatGoogleGenerativeAI") as mock_llm_class:
        mock_llm = MagicMock()
        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.return_value = mock_job_info
        mock_llm.with_structured_output.return_value = mock_structured_llm
        mock_llm_class.return_value = mock_llm
        
        # Also need to mock ChatPromptTemplate as it's part of the chain
        with patch("src.extraction.ChatPromptTemplate.from_messages") as mock_prompt_class:
            mock_prompt = MagicMock()
            # The | operator calls __or__
            mock_prompt.__or__.return_value = mock_structured_llm
            mock_prompt_class.return_value = mock_prompt
            
            result = extract_job_data(text)
            
            assert isinstance(result, JobInfo)
            assert result.job_title == "Software Engineer"
        assert result.company_name == "Google"
