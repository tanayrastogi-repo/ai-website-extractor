import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.models import JobInfo
from dotenv import load_dotenv

load_dotenv()

def get_structured_llm(provider: str, model: str):
    """Returns a structured LLM based on the provider and model."""
    if provider.lower() == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        return llm.with_structured_output(JobInfo)
    elif provider.lower() == "ollama":
        llm = ChatOllama(
            model=model,
            temperature=0,
            format="json",
        )
        # 2026 Best Practice: use json_schema for Ollama logit masking
        return llm.with_structured_output(JobInfo, method="json_schema")
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def extract_job_data(text: str, provider: str = "gemini", model: str = "gemini-2.5-flash") -> JobInfo:
    """Extracts structured job information from text using the selected provider and model."""
    
    structured_llm = get_structured_llm(provider, model)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at extracting structured information from job postings. Return ONLY valid JSON that matches the requested schema. Do not include any preamble, conversational filler, or Markdown code blocks (like ```json). Break down qualifications and requirements into clear, concise bullet points. Specifically, categorize requirements into 'technical_skills' (tools, languages, domain knowledge) and 'soft_skills' (communication, teamwork, interpersonal)."),
        ("human", "Extract the job information from the following text: {text}\n\nStrictly output valid JSON only.")
    ])
    
    chain = prompt | structured_llm
    
    return chain.invoke({"text": text})
