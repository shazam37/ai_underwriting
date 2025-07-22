import os
import json
import uuid
from pathlib import Path
from typing import List
from datetime import datetime

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from dotenv import load_dotenv
import requests
import asyncio

from database import *
from schemas import *
from utils import *
from dummy_data import init_dummy_data

# dotenv_path=Path("../.env")

# # Load environment variables
# load_dotenv()

xai_api_key=os.environ.get('XAI_API_KEY')
uw_key=os.environ.get('UW_API_KEY')
image_extraction_file=os.environ.get('IMAGE_HOST_URL')
langflow_url=os.environ.get('LANGLFLOW_URL')

# Initialize FastAPI
app = FastAPI(title="Document Processing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

#old::
# API Endpoints
@app.post("/upload_personal_documents")
async def upload_personal_documents(
    file: UploadFile = File(...),
    document_type: ApplicationDocumentType = Query(..., description="Type of personal document: driving_license or ssn"),
    db: Session = Depends(get_db)
):
    """Upload and process a document (image or PDF) to extract license/SSN number"""
    
    # Validate file type
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_extension} not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save file locally
    file_path = save_file(file)
    
    try:
        # Extract content based on file type
        if file_extension == '.pdf':
            image_url = ''
            content = extract_text_from_pdf(file_path)
            verified = verify_document(document_type, 'text', content, image_url)
            if verified == str('True'):
                extracted_number = extract_document_with_llm(content, 'text', image_url)
            elif verified == str('False'):
                print('Failed verification')
                return DocumentUploadMessage(
                        success=False,
                        message=f"Couldn't Upload the document: {document_type}",
                        document_type=document_type,
                        extracted_number="",
                        file_path=file_path
                    )
        elif file_extension in ['.jpg', '.png', '.jpeg']:
            content = ''
            image_url = f"{image_extraction_file}/{file.filename}" 
            verified = verify_document(document_type, 'image', content, image_url)
            if verified == str('True'):
                extracted_number = extract_document_with_llm(content, 'image', image_url)
            elif verified == str('False'):
                print('Failed verification')
                return DocumentUploadMessage(
                        success=False,
                        message=f"Couldn't Upload the document: {document_type}",
                        document_type=document_type,
                        extracted_number="",
                        file_path=file_path
                    )

        print(f'The number extracted: {extracted_number}')
        
        new_license_number = DocumentUploadSave(id = str(uuid.uuid4()),
                                                document_type = document_type, 
                                                extracted_number = extracted_number, 
                                                created_at = datetime.now())

        db.add(new_license_number)
        db.commit()

        print('Document Saved Successfully')

        return DocumentUploadMessage(
            success=True,
            message=f"Successfully extracted {document_type} number",
            document_type=document_type,
            extracted_number=extracted_number,
            file_path=file_path
        )
        
    except Exception as e:
        # Clean up file on error
        try:
            os.remove(file_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload_bank_documents")
async def upload_bank_documents(file: UploadFile = File(...), 
                                application_type: StatementDocumentType  = Query(..., description="Type of bank document: bank_application or bank_statement"),
                                db: Session = Depends(get_db)):

    # Validate file type
    allowed_extensions = {'.pdf'}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_extension} not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save file locally
    file_path = save_file(file)

    try:

        content = extract_text_from_pdf(file_path)

        image_url = ''

        verified = verify_document(application_type, 'text', content, image_url)

        if verified == str('True'):
            try:
                new_bank_document = ApplicationUploadSave(id = str(uuid.uuid4()),
                                                            content = content,
                                                            application_type=application_type,
                                                            created_at = datetime.now())

                db.add(new_bank_document)
                db.commit()

                print('Document Saved Successfully')

                return ApplicationUploadMessage(
                    success=True,
                    message=f"Successfully extracted {application_type}",
                    application_type=application_type,
                    content=content,
                    file_path=file_path
                )

            except Exception as e:
                raise f'Couldnt upload file due to: {e}'
            
        elif verified == str('False'):
            return ApplicationUploadMessage(
                    success=False,
                    message=f"Couldn't Upload the document: {application_type}",
                    application_type=application_type,
                    content="",
                    file_path=file_path
                )
    except Exception as e:
        # Clean up file on error
        try:
            os.remove(file_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-driving-license/{extracted_number}")
async def save_driving_license(extracted_number: str, db: Session = Depends(get_db)):

    try:
        new_license_number = DocumentUploadSave(id = str(uuid.uuid4()),
                                                    document_type = "driving_license", 
                                                    extracted_number = extracted_number, 
                                                    created_at = datetime.now())

        db.add(new_license_number)
        db.commit()

        print('Document Saved Successfully')

        return "DL number uploaded"

    except Exception as e:
        return {f"Couldn't upload DL due to: {e}"}

@app.get("/driving-license/{license_number}", response_model=DrivingLicenseResponse)
async def get_driving_license(license_number: str, db: Session = Depends(get_db)):
    """Get driving license details by license number"""
    
    license_record = db.query(DrivingLicense).filter(
        DrivingLicense.license_number == license_number
    ).first()
    
    if not license_record:
        raise HTTPException(status_code=404, detail="Driving license not found")
    
    return license_record

@app.post("/save-ssn/{extracted_number}")
async def save_ssn(extracted_number: str, db: Session = Depends(get_db)):

    try:
        new_license_number = DocumentUploadSave(id = str(uuid.uuid4()),
                                                    document_type = "ssn", 
                                                    extracted_number = extracted_number, 
                                                    created_at = datetime.now())

        db.add(new_license_number)
        db.commit()

        print('Document Saved Successfully')

        return "SSN uploaded"

    except Exception as e:
        return {f"Coulndn't upload SSN due to: {e}"}

@app.get("/ssn/{ssn}", response_model=SSNResponse)
async def get_ssn_record(ssn: str, db: Session = Depends(get_db)):
    """Get SSN record details by SSN"""
    
    ssn_record = db.query(SSNRecord).filter(SSNRecord.ssn == ssn).first()
    
    if not ssn_record:
        raise HTTPException(status_code=404, detail="SSN record not found")
    
    return ssn_record

@app.post("/save-bank-application")
async def save_bank_application(request: BankApplicationSchema, db: Session = Depends(get_db)):
    
    try:
        new_license_number = ApplicationUploadSave(id = str(uuid.uuid4()),
                                                    content = str(request.content),
                                                    application_type="application",
                                                    created_at = datetime.now())

        db.add(new_license_number)
        db.commit()

        print('Application Saved Successfully')

        return "Bank application uploaded"

    except Exception as e:
        raise f'Couldnt upload application due to: {e}'
    
@app.post("/save-bank-statement")
async def save_bank_statement(request: BankApplicationSchema, db: Session = Depends(get_db)):
    
    try:
        new_license_number = ApplicationUploadSave(id = str(uuid.uuid4()),
                                                    content = str(request.content),
                                                    application_type="statement",
                                                    created_at = datetime.now())

        db.add(new_license_number)
        db.commit()

        print('Statement Saved Successfully')

        return "Bank application uploaded"

    except Exception as e:
        raise f'Couldnt upload statement due to: {e}'

@app.get("/bureau-record/{ssn}", response_model=BureauResponse)
async def get_bureau_record(ssn: str, db: Session = Depends(get_db)):
    """Get Bureau record details by SSN"""
    
    bureau__record = db.query(Bureau).filter(Bureau.ssn == ssn).first()
    
    if not bureau__record:
        raise HTTPException(status_code=404, detail="Bureau record not found")
    
    return bureau__record

@app.get("/kyc-record/{ssn}", response_model=KYCResponse)
async def get_kyc_record(ssn: str, db: Session = Depends(get_db)):
    """Get KYC record details by SSN"""
    
    kyc_record = db.query(KYC).filter(KYC.ssn == ssn).first()
    
    if not kyc_record:
        raise HTTPException(status_code=404, detail="KYC record not found")
    
    return kyc_record

@app.get("/latest_dl_number")
async def get_latest_document_by_type(db: Session = Depends(get_db)):
    """Get the latest extracted_number for the given document_type"""

    latest_doc = db.query(DocumentUploadSave).filter(
        DocumentUploadSave.document_type == "driving_license"
    ).order_by(DocumentUploadSave.created_at.desc()).first()

    if not latest_doc:
        raise HTTPException(status_code=404, detail="No documents found for this type")

    return latest_doc.extracted_number

@app.get("/latest_ssn_number")
async def get_latest_document_by_type(db: Session = Depends(get_db)):
    """Get the latest extracted_number for the given document_type"""

    latest_doc = db.query(DocumentUploadSave).filter(
        DocumentUploadSave.document_type == "ssn"
    ).order_by(DocumentUploadSave.created_at.desc()).first()

    if not latest_doc:
        raise HTTPException(status_code=404, detail="No documents found for this type")

    return latest_doc.extracted_number

@app.get("/latest_bank_application")
async def get_latest_application(db: Session = Depends(get_db)):
    "Get the latest parsed bank application"

    latest_app = db.query(ApplicationUploadSave).filter(
        ApplicationUploadSave.application_type == "bank_application"
    ).order_by(ApplicationUploadSave.created_at.desc()).first()

    if not latest_app:
        raise HTTPException(status_code=404, detail="No latest bank application found")
    
    return latest_app.content

@app.get("/latest_bank_statement")
async def get_latest_statement(db: Session = Depends(get_db)):
    "Get the latest parsed bank application"

    latest_app = db.query(ApplicationUploadSave).filter(
        ApplicationUploadSave.application_type == "bank_statement"
    ).order_by(ApplicationUploadSave.created_at.desc()).first()

    if not latest_app:
        raise HTTPException(status_code=404, detail="No latest bank application found")
    
    return latest_app.content

@app.get("/driving-licenses", response_model=List[DrivingLicenseResponse])
async def get_all_driving_licenses(db: Session = Depends(get_db)):
    """Get all driving license records"""
    licenses = db.query(DrivingLicense).all()
    return licenses

@app.get("/ssn-records", response_model=List[SSNResponse])
async def get_all_ssn_records(db: Session = Depends(get_db)):
    """Get all SSN records"""
    ssn_records = db.query(SSNRecord).all()
    return ssn_records

@app.get("/bureau-records", response_model=List[BureauResponse])
async def get_all_bureau_records(db: Session = Depends(get_db)):
    """Get all Bureau records"""
    bureau_records = db.query(Bureau).all()
    return bureau_records

@app.get("/kyc-records", response_model=List[KYCResponse])
async def get_all_kyc_records(db: Session = Depends(get_db)):
    "Get all KYC records"
    kyc_records = db.query(KYC).all()
    return kyc_records

@app.get("/fetch_all_stored_license", response_model=List[DocumentUploadResponse])
async def get_all_documents(db: Session = Depends(get_db)):
    """Get all uploaded document records"""
    try:
        documents = db.query(DocumentUploadSave).all()
        return documents
    except Exception as e:
        return f"No values found: {e}"

@app.get("/fetch_all_stored_applications", response_model=List[ApplicationUploadResponse])
async def get_all_applications(db: Session = Depends(get_db)):
    """Get all bank applications"""
    try:
        applications = db.query(ApplicationUploadSave).all()
        return applications
    except Exception as e:
        return f"No values found: {e}" 

@app.post("/Delete_all-records")
async def delete_all_records(db: Session = Depends(get_db)):
    """Delete all records from both driving licenses and SSN tables"""
    
    dl_count = db.query(DrivingLicense).count()
    ssn_count = db.query(SSNRecord).count()
    bureau_count = db.query(Bureau).count()
    kyc_count = db.query(KYC).count()
    total_count = dl_count + ssn_count + bureau_count + kyc_count
    
    if total_count == 0:
        raise HTTPException(status_code=404, detail="No records found in database")
    
    db.query(DrivingLicense).delete()
    db.query(SSNRecord).delete()
    db.query(Bureau).delete()
    db.query(KYC).delete()
    db.commit()
    
    return {
        "success": True,
        "message": f"All records deleted successfully",
        "deleted_counts": {
            "driving_licenses": dl_count,
            "ssn_records": ssn_count,
            "bureau_records": bureau_count,
            "kyc_records": kyc_count,
            "total": total_count
        }
    }

# Throws problem while calling the UW API:
# @app.post("/post_on_uw_model")
# async def post_on_uw_model(request: Request):

#     body = await request.body()
    
#     data = body.decode("utf-8").strip()

#     # cleaned_data = re.sub(r"^```json\s*|\s*```$", "", data.strip(), flags=re.DOTALL)

#     match = re.search(r'"id":\s*"([^"]*)"', data)
    
#     id = match.group(1)

#     json_data = json.loads(data)

#     url =  'https://apiv2.aryaxai.com/v2/project/case-register'

#     headers = {
#     "Content-Type": "application/json",
#     "x-api-token": uw_key
#     }

#     payload = {
#     "client_id": "amey_balekundri_arya",
#     "project_name": "lending_club_3DEWX2KF8X",
#     "unique_identifier": id,
#     "tag": "377",
#     "data": [json_data]
#     }

#     try:
#         resp = requests.post(url, headers=headers, json=payload)
#         resp.raise_for_status()
#         return resp.text
#     except requests.RequestException as e:
#         # network error or non‑200 status
#         raise HTTPException(status_code=502, detail=f"Upstream request failed: {e}")    

@app.get("/get_uw_result/{tag}/{ID}")
async def get_uw_results(tag: str, ID: str):
    
    await asyncio.sleep(60)

    url =  'https://apiv2.aryaxai.com/v2/project/get-case-profile'
    headers = {
    "Content-Type": "application/json",
    "x-api-token": uw_key
    }
    payload = {
    "client_id": "amey_balekundri_arya",
    "project_name": "lending_club_3DEWX2KF8X",
    "unique_identifier": ID,
    "tag": tag,
    "refresh": "true"
    }
    # resp_2 = requests.post(url, headers=headers, json=payload)
    # return resp_2.json()

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=400)
        resp.raise_for_status()
    except requests.RequestException as e:
        # network error or non‑200 status
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {e}")

    try:
        data = resp.json()
    except ValueError:
        # invalid JSON
        return JSONResponse(
            status_code=200,
            content={
                "warning": "Upstream returned non‑JSON payload",
                "raw_text": resp.text,
            },
        )

    return data
    # except Exception as e:
    #     raise f'An exception occuered: {e}'

@app.post("/post_underwriting_result")
async def post_underwriting_result(request: UnderwritingInput, db: Session = Depends(get_db)):
    try:
        result_id = str(uuid.uuid4())
        new_result = UnderstatementResult(
            id=result_id,
            content=str(request.payload_content),
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        return {"message": "Underwriting result saved successfully", "id": result_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save: {str(e)}")
    finally:
        db.close()
    
@app.get("/latest_underwriting_result")
def get_latest_underwriting_result(db: Session = Depends(get_db)):
    try:
        latest_result = (
            db.query(UnderstatementResult)
            .order_by(UnderstatementResult.created_at.desc())
            .first()
        )

        if not latest_result:
            raise HTTPException(status_code=404, detail="No underwriting result found.")

        return {
            "underwriting_analysis": latest_result.content,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving latest result: {str(e)}")
    finally:
        db.close()

@app.get("/get_all_underwriting_results", response_model=List[UnderstatementResponse])
async def get_all_underwriting_results(db: Session = Depends(get_db)):
    """Get all driving license records"""
    understatement = db.query(UnderstatementResult).all()
    return understatement

@app.get("/run_underwriting_flow")
async def run_underwriting_flow():
    
    url = langflow_url

    # Request payload configuration
    payload = {
        # "input_value": "hello world!",  # The input value to be processed by the flow
        "output_type": "chat",  # Specifies the expected output format
        # "input_type": "text",  # Specifies the input format 
        # "session_id": "07edd3d0-c1e7-4f42-a547-7a86cd59ab7a"  # Unique UUID session_id 
    }

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": xai_api_key  # Authentication key from environment variable    
    }

    try:
        # Send API request
        response = requests.request("POST", url, json=payload, headers=headers, timeout=900)
        response.raise_for_status()  # Raise exception for bad status codes

        # Print response
        print(response.text)

        json_response = json.loads(response.text)

        json_response = json_response['outputs'][0]['outputs'][0]['results']['message']['data']['text']

        return json_response

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except ValueError as e:
        print(f"Error parsing response: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Initialize dummy data on startup
@app.on_event("startup")
async def startup_event():
    init_dummy_data()

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


