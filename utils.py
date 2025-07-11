import os
import re
import uuid
from pathlib import Path
import PyPDF2
from fastapi import HTTPException, UploadFile
import openai
from dotenv import load_dotenv

dotenv_path=Path("../.env")

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

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

def extract_document_with_llm(content: str, document_type: str, image_url: str) -> str:
    """Extract license/SSN number using LLM (OpenAI)"""

    if document_type == "text":
        try:
            client = openai.OpenAI(api_key=openai_api_key)

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
            client = openai.OpenAI(api_key=openai_api_key)
            
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

        # Fallback regex patterns
        # if document_type == DocumentType.DRIVING_LICENSE:
        #     # Common DL patterns (varies by state)
        #     patterns = [
        #         r'[A-Z]\d{7,8}',  # Format: A1234567
        #         r'[A-Z]{2}\d{6,7}',  # Format: AB123456
        #         r'\d{8,9}',  # Format: 12345678
        #         r'[A-Z]\d{2}-\d{3}-\d{3}',  # Format: A12-345-678
        #     ]
        # else:  # SSN
        #     patterns = [
        #         r'\d{3}-\d{2}-\d{4}',  # Format: 123-45-6789
        #         r'\d{9}',  # Format: 123456789
        #     ]
        
        # for pattern in patterns:
        #     match = re.search(pattern, content)
        #     if match:
        #         return match.group(0)
        
        # raise HTTPException(status_code=400, detail=f"Could not extract {document_type} number from document")
        
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