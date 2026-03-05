



if __name__ == "__main__":

    #---- DEBUGGING FOR SCRAPER MODULE ----#
    from src.scraper import fetch_html, extract_clean_text

    ## Test with a real job posting URL
    # url = "https://hedvig.teamtailor.com/jobs/7249655-data-scientist"
    url = "https://us.wd103.myworkdayjobs.com/tobii_dynavox/job/Stockholm/BI-Analyst_JR100923?source=LinkedIn"
    # url = "https://emp.jobylon.com/jobs/341841-postnord-sverige-verksamhetsutvecklare-prognoser-logistik-flera-orter-mojliga/"
    # url = "https://jobs.scania.com/job/S%C3%B6dert%C3%A4lje-Automation-Engineer-151-38/1370133233/"
    html = fetch_html(url)
    # print(html)  # Print the first 500 characters of the HTML

    ## Test to extract clean text from the HTML
    clean_text = extract_clean_text(html)
    print(clean_text)  # Print the first 1000 characters of the






    print("\n#---- DEBUGGING FOR AI FORMATTER ----#")
    ## Use the following Job Model for testing the formatter
    from pydantic import BaseModel, Field
    from typing import Optional

    class JobInfo(BaseModel):
        """Structured information about a job posting."""
        job_title: str = Field(description="The official title of the job position.")
        company_name: str = Field(description="The name of the company offering the job.")
        location: str = Field(description="The geographic location of the job (e.g., 'Remote', 'New York, NY').")
        about_company: str = Field(description="A brief description of what the company does.")
        key_responsibilities: str = Field(description="Main duties and tasks the employee will perform.")
        qualifications: list[str] = Field(description="Educational background, certifications, or years of experience required, as a list of bullet points.")
        technical_skills: list[str] = Field(description="List of specific technical skills, tools, or knowledge needed for the role.")
        soft_skills: list[str] = Field(description="List of soft skills, such as communication, leadership, or teamwork, needed for the role.")
        contact_person: Optional[str] = Field(description="Name or role of the person to contact, if available.")

    ## The LLM Model for testing the formatter
    import os 
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from dotenv import load_dotenv
    load_dotenv()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    structured_llm = llm.with_structured_output(JobInfo)
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert at extracting structured information from job postings. Break down qualifications and requirements into clear, concise bullet points. Specifically, categorize requirements into 'technical_skills' (tools, languages, domain knowledge) and 'soft_skills' (communication, teamwork, interpersonal)."),
    ("human", "Extract the job information from the following text: {text}")])
    
    chain = prompt | structured_llm
    output = chain.invoke({"text": clean_text})
    print(output)




    print("\n#---- DEBUGGING FOR MARKDOWN FORMATTER ----#")
    from src.formatter import render_markdown
    ## Test the Markdown rendering with the extracted job information
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


    markdown_content = render_markdown(output, default_template)
    print(markdown_content)  # Print the rendered Markdown content 