from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key="")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


class TextInput(BaseModel):
    context: str

class EditTextInput(BaseModel):
    report: str
    userCondition: str
    
@app.post("/generateReport")
async def summarize_text(data: TextInput):
    print(data.context)
    gemini_response = gemini_model.generate_content(
        f"Generate a brief report on topic : {data.context} and the report should be in good structure and in markdown format with proper headings and point wise for ten pages."
    )
    final = gemini_response.text.replace("\n", "<br>")
    return {"generatedReport": final}

@app.post("/regenerateReport")
async def editReport(data: EditTextInput):
    gemini_response = gemini_model.generate_content(
        f"Regenerate and eloborate report for the given report data : {data.report} and based on the user response :{data.userCondition} the report should be in good structure and in markdown format with proper headings and point wise for ten pages."
    )
    final = gemini_response.text.replace("\n", "<br>")
    return {"generatedReport": final}
    
