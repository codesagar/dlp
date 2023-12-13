from fastapi import FastAPI, HTTPException
from models import PANPIIRequest, PANPIIResponse
from pan_pii_detector import detect, mask, anonymize

app = FastAPI()


@app.post("/detect/", response_model=PANPIIResponse)
async def detect_info(request: PANPIIRequest):
    
    text, mapping = detect(text=request.text, entities=request.entities)

    return PANPIIResponse(
        text=text,
        entities=request.entities,
        mapping=mapping
    )

@app.post("/mask/", response_model=PANPIIResponse)
async def mask_info(request: PANPIIRequest):

    response_text, mapping = mask(text=request.text, entities=request.entities)

    return PANPIIResponse(
        text=response_text,
        entities=request.entities,
        mapping=mapping
    )

@app.post("/anonymize/", response_model=PANPIIResponse)
async def anonymize_info(request: PANPIIRequest):

    response_text, mapping = anonymize(text=request.text, entities=request.entities)

    return PANPIIResponse(
        text=response_text,
        entities=request.entities,
        mapping=mapping
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)