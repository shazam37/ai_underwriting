import os
import re
import uuid
from pathlib import Path
import PyPDF2
from fastapi import HTTPException, UploadFile
import openai
from dotenv import load_dotenv

openai_api_key = os.environ.get('OPENAI_API_KEY')

client = openai.OpenAI(api_key=openai_api_key)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
    
def extract_text_from_pdf_stream(file_stream) -> str:
    """Extract text directly from in-memory uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def extract_document_with_llm(content: str, document_type: str, image_url: str) -> str:
    """Extract license/SSN number using LLM (OpenAI)"""

    if document_type == "text":
        try:
            # OpenAI API call (uncomment and configure when ready)
            prompt = f'''You are an expert character recognition system. You will receive a Driving License/ Social Security Number as text.
                        Your job is to only extract the License or Social Secrity number from it. You will only return the number as output. There should be no spaces, dashes, or commas in the output.

                        Here is the PDF content: {content}
                        
                        '''

            response = client.responses.create(
                model="gpt-4.1",
                input=prompt
            )
            
            return response.output_text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting number: {str(e)}")
        
    elif document_type == 'image':
        try:            
            # OpenAI API call (uncomment and configure when ready)
            prompt = f'''You are an expert OCR system. You will receive a Driving License/ Social Security Number details as an image.
                        Your job is to only extract the License or Social Secrity number from it. You will only return the number as output. There should be no spaces, dashes, or commas in the output.

                        Here is the image:'''
            
            response = client.responses.create(
                model="gpt-4.1",
                input=[{
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": image_url,
                        },
                    ],
                }],
            )
            return response.output_text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting number: {str(e)}")
        
def save_file(file: UploadFile) -> str:
    """Save uploaded file locally"""
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
    
    try:
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        print(f'original_filepath: {file.filename}')
        print(f'file uploaded at {file_path}')
        return str(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
def verify_document(document_type, type, content, image_url):
    
    if type == 'image':
        try:      
            # OpenAI API call (uncomment and configure when ready)
            prompt = f'''  
                        You are an expert OCR system in identifying the document type: {document_type}. You will receive a document as an image.
                        Your job is to verify whether the uploaded document is of the document type or is related to the document type:: {document_type}. 
                        Be very thorough, strict and specific with the analysis.
                        If it is, return only the Boolean 'True' as output
                        If it is not, return only the Boolean 'False' as output 
                        
                        Here is the image:'''
            
            response = client.responses.create(
                model="gpt-4.1",
                input=[{
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": image_url,
                        },
                    ],
                }],
            )
            return response.output_text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting number: {str(e)}")
        
    elif type == "text":
        try:
            # OpenAI API call (uncomment and configure when ready)
            prompt = f'''You are an expert OCR system in identifying the document type: {document_type}. You will receive a document.
                        Your job is to verify whether the uploaded document is of the document type: {document_type}. 
                        Only appliction belonging to the {document_type} must be accepted.
                        Be very thorough, strict and specific with the analysis. Check for important stuff that are supposed to be present in the given document to qualify as {document_type}.
                        Strictly do not confuse between the bank application and bank statement. Always read the title of the document to decide.
                        If it is, return only the Boolean 'True' as output
                        If it is not, return only the Boolean 'False' as output 

                        Here is the PDF content: {content}
                        
                        '''

            response = client.responses.create(
                model="gpt-4.1",
                input=prompt
            )
            print(f'The Decision: {response.output_text}')
            return response.output_text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting number: {str(e)}")