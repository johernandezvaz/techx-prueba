import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from PIL import Image, UnidentifiedImageError
import pytesseract
import io

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# App FastAPI
app = FastAPI(
    title="OCR API",
    description="Procesador OCR para recibos usando Tesseract",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constantes
SUPPORTED_FORMATS = {"image/jpeg", "image/jpg", "image/png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# Funciones utilitarias
def validate_image(file: UploadFile) -> None:
    if file.content_type not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado. Solo se permite: {', '.join(SUPPORTED_FORMATS)}"
        )


def preprocess_image(image: Image.Image) -> Image.Image:
    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.convert('L')  # Escala de grises
        return image
    except Exception as e:
        logger.error(f"[Preprocessing Error] {str(e)}")
        raise HTTPException(status_code=500, detail="Error durante el preprocesamiento de la imagen")


def extract_text(image: Image.Image) -> str:
    try:
        processed_image = preprocess_image(image)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_image, config=custom_config, lang="spa+eng")
        cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(cleaned_lines)
    except pytesseract.TesseractNotFoundError:
        logger.exception("Tesseract no encontrado")
        raise HTTPException(status_code=500, detail="Tesseract no está instalado correctamente")
    except Exception as e:
        logger.exception(f"Error durante el OCR: {str(e)}")
        raise HTTPException(status_code=500, detail="Error extrayendo el texto de la imagen")


# Rutas

@app.get("/")
async def root():
    return {"message": "OCR API operativa"}

@app.get("/health")
async def health():
    try:
        pytesseract.get_tesseract_version()
        return {"status": "ok", "tesseract": "available"}
    except:
        return {"status": "ok", "tesseract": "unavailable"}


@app.post("/upload-ocr")
async def upload_ocr(file: UploadFile = File(...)):
    try:
        validate_image(file)

        # Leer contenido
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="El archivo está vacío")

        try:
            image = Image.open(io.BytesIO(content))
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail="No se pudo abrir la imagen. ¿Está dañada o mal codificada?")
        
        # Realizar OCR
        extracted_text = extract_text(image)

        if not extracted_text.strip():
            return JSONResponse(
                content={"text": "", "error": "No se detectó texto legible. Intenta con otra imagen."},
                status_code=200
            )

        return JSONResponse(content={"text": extracted_text, "error": None}, status_code=200)

    except HTTPException as http_err:
        return JSONResponse(status_code=http_err.status_code, content={"detail": http_err.detail})
    except Exception as e:
        logger.exception(f"Error inesperado: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})
