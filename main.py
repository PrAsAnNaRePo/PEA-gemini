import os
import re
from fastapi import FastAPI
import google.generativeai as genai
from pydantic import BaseModel

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

app = FastAPI()
model = genai.GenerativeModel('gemini-pro')

class EmailRequest(BaseModel):
    email: str
    subject: str
    content: str

@app.post("/")
async def check_email(email: EmailRequest):
    prompt = f"""You are a Email Agent, who have to review the user emails and check if the email is related to job offer or not.
Don't fall for the trap of other institutions and education consultants. Only like if the email was like a job offer or anything like the user've applied before and got result for this.
Don't include the linked in job recommendations or any other job recommendations from any other platform. Only include the job offers from the companies or the job offers from the user applied for.
I the given email fall into the above category, then respond with `YES` or `NO` inside the tag <job>.
For example:
<job>YES<job>

From: {email.email}
Subject: {email.subject}
Content: {email.content}

Make sure your response has the tag <job>YES<job> or <job>NO<job>inside it with correct format.
"""

    response = model.generate_content(prompt).text
    print(response)
    regex = re.compile(r'<job>(.*?)<job>', re.DOTALL)
    match = regex.search(response)
    job_email = match.group(1)
    if job_email == 'YES':
        response = model.generate_content(f"Given a email, you have to write a sweet description regards the mail.\nHere is the email:\n{email.content}").text
        return {"job_email": True, "desc": response}
    return {"job_email": False, "desc": None}
