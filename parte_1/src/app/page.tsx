/* eslint-disable @next/next/no-img-element */
'use client';

import { useState, useCallback } from 'react';
import { Upload, FileText, Copy, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';


interface OCRResponse {
  text: string;
  error: string | null;
}

export default function OCRApp() {
  const [ selectedFile, setSelectedFile ] = useState<File | null>(null);
  const [ previewUrl, setPreviewUrl ] = useState<File | null>(null);
  const [extractedText, setExtractedText] = useState<string>('');
  const [ isLoading, setIsLoading ] = useState(false);  
  const [ isDragOver, setIsDragOver] = useState(false);

  const validateFile = (file: File): boolean => {
    const validTypes = [ 'image/png', 'image/jpeg', 'image/jpg' ];
    const maxSize = 10 * 1024 * 1024; 

    if (!validTypes.includes(file.type)){
      toast.error('Archivo invalido. Solo se permiten imagenes PNG o JPEG');
      return false;
    }

    if(file.size > maxSize){
      toast.error('El archivo es demasiado grande. Maximo 10MB.');
      return false;
    }

    return true;

  };

  const handleFileSelect = useCallback((file: File) => {
    if (!validateFile(file)) return;

    setSelectedFile(file);

    const reader = new FileReader();

    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);

    setExtractedText("");

  }, []);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    const files = e.dataTransfer.files;

    if (files.length > 0){
      handleFileSelect(files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelect(files[0]);
    }
  };


  const processImage = async () => {
    if (!selectedFile) {
      toast.error('Por favor selecciona una imagen primero');
      return;
    }

    setIsLoading(true);

    try{
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('/api/upload-ocr', {
        method: 'POST',
        body: formData
      });

      if(!response.ok){
        throw new Error(`Error del servidor: ${response.status}`);
      }

      const data: OCRResponse = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setExtractedText(data.text);
      toast.success('Texto extraido correctamente');
    } catch (error) {
      console.error('Error procesando la imagen: ', error);
      toast.error('No se pudo extraer texto de la imagen');
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async  () => {
    if (!extractedText) return;

    try{
      await navigator.clipboard.writeText(extractedText);
      toast.success('Texto copiado al portapapeles')
    } catch (error){
      console.error('Error copying text: ', error);
      toast.error('No se pudo copiar el texto');
    }
  };

  const clearAll = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setExtractedText('');
  };

  return (
    <div className='min-h-screen bg-[#f9fafb] py-8 px-4'>
      <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className='text-center mb-8'>
            <h1 className='text-3xl font-bold text-gray-900 mb-2'>
                Procesador de Recibos
            </h1>
            <p className='text-gray-600'>
              Extrae el texto de tus recibos
            </p>
          </div>
          {/* Subir Archivos */}
          <Card className='mb-6 shadow-md hover:shadow-lg transition-all duration-300'>
            <CardContent className='p-6'>
              <div className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 ${
              isDragOver
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragOver={ handleDragOver} 
            onDragLeave={ handleDragLeave}
            onDrop={ handleDrop} 
            >
              <input 
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              onChange={ handleFileInputChange}
              className="hidden"
              id="file-upload" 
              />

              { previewUrl ? (
                <div className='space-y-4'>
                  <div className='relative inline-block'>
                    <img 
                    src={previewUrl} 
                    alt="Preview"
                    className='max-w-full max-h-64 rounded-lg shadow-md' 
                    />
                    <Button
                    variant="destructive"
                    size="sm"
                    className='absolute top-2 right-2'
                    onClick={ clearAll}
                    >
                      ×
                    </Button>
                  </div>
                  <p className='text-sm text-gray-600'>
                      {selectedFile?.name} ({(selectedFile?.size || 0 / 1024).toFixed(2)} MB)
                  </p>
                </div>
              ) : (
                <div className='space-y-4'>
                  < Upload className='w-12 h-12 mx-auto text-gray-400' />
                  <div>
                    <label 
                    htmlFor="file-upload"
                    className='cursor-pointer text-blue-600 hover:text-blue-700 font-medium'
                    >
                      Selecciona una imagen
                    </label>
                    <span className='text-gray-500'> o arrastra y suelta aqui</span>
                  </div>
                  <p className='text-sm text-gray-500'>
                    Selecciona o arrastra una imagen de un recibo para procesarla
                  </p>
                  <p className='text-xs text-gray-400'>
                    Solo archivos PNG o JPEF (maximo 10MB)
                  </p>
                </div>
              )}
              </div>
            </CardContent>
          </Card>
          {/* Boton de procesar */}
          <div className='mb-6'>
            <Button
            onClick={processImage}
            disabled = {!selectedFile || isLoading}
            className = "w-full bg-[#2563eb] hover:bg-[#1d4ed8] text-white font-medium py-3 px-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed" 
            >
              { isLoading ? (
                <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Procesando imagen...
                </>
              ) : (
                <>
                <FileText className = "w-5 h-5 mr-2" />
                </>
              )}
            </Button>
          </div>

          { /* Resultados */}
          { extractedText && (
            <Card className='shadow-md hover:shadow-lg transition-all duration-300'>
              <CardContent className='p-6'>
                <div className='flex justify-between items-center mb-4'>
                  <h2 className="text-xl font-semibold text-gray-900">
                    Texto Extraido
                  </h2>
                  <Button
                  variant="outline"
                  size="sm"
                  onClick={copyToClipboard}
                  className='hover:bg-gray-50'
                  >
                    <Copy className='w-4 h-4 mr-2' />
                  </Button>
                </div>

                <textarea 
                value={extractedText} 
                readOnly
                className='w-full h-64 p-4 bg-white border border-gray-200 rounded-lg font-mono text-sm text-gray-900 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                placeholder='El texto extraido aparecera aqui...'
                />
                <div className='mt-4 flex items-center text-sm text-gray-500'>
                  <CheckCircle className='w-4 h-4 mr-2 text-green-500'/>
                  Texto extraido correctamente. Puedes copiarlo usando el boton de arriba
                </div>
              </CardContent>
            </Card>
          )}

          { /* Info de la API */}
          <div className='mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200'>
            <div className='flex items-start'>
              <AlertCircle className='w-5 h-5 text-blue-600 mr-2 mt-0.5' />
              <div className='text-sm text-blue-800'>
                <p className='font-medium mb-1'>Informacion de la API</p>
                <p>
                  Esta aplicacion esta configurada con FastAPI en { ' ' }
                  <code className='bg-blue-100 px-1 py-0.5 rounded text-xs'>
                    POST /api/upload-ocr
                  </code>
                </p>
              </div>
            </div>
          </div>
      </div>
    </div>
  );
}

