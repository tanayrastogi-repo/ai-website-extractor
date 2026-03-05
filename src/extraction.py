import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.models import JobInfo
from dotenv import load_dotenv

load_dotenv()

def extract_job_data(text: str) -> JobInfo:
    """Uses Gemini 2.5 Flash to extract structured job information from text."""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    structured_llm = llm.with_structured_output(JobInfo)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at extracting structured information from job postings."),
        ("human", "Extract the job information from the following text: {text}")
    ])
    
    chain = prompt | structured_llm
    
    return chain.invoke({"text": text})
