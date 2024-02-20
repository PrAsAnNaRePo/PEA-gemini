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
Don't fall for the trap of other institutions and education consultants. Only like if the email was like a job offer or anything like the user've applied bedore and got result for tha.
I the given email fall into the above category, then respond with `YES` or `NO` inside the tag <job>.
For example:
<job>YES<job>

From: {email.email}
Subject: {email.subject}
Content: {email.content}
"""

    response = model.generate_content(prompt).text
    regex = re.compile(r'<job>(.*?)<job>', re.DOTALL)
    match = regex.search(response)
    return {"job": match.group(1)}
