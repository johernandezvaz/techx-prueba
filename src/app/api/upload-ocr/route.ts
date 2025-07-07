import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No se encontró archivo en la petición' },
        { status: 400 }
      );
    }

    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      return NextResponse.json(
        { error: 'Tipo de archivo inválido. Solo se permiten PNG o JPEG.' },
        { status: 400 }
      );
    }


    const fastApiFormData = new FormData();
    fastApiFormData.append('file', file);


    const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000';
    
    const response = await fetch(`${FASTAPI_URL}/upload-ocr`, {
      method: 'POST',
      body: fastApiFormData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('FastAPI Error:', errorText);
      return NextResponse.json(
        { error: 'Error del servidor de procesamiento OCR' },
        { status: 500 }
      );
    }

    const data = await response.json();
    
    return NextResponse.json({
      text: data.text || '',
      error: data.error || null,
    });
  } catch (error) {
    console.error('OCR Processing Error:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor' },
      { status: 500 }
    );
  }
}