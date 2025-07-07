# OCR Receipt Processor - FastAPI Backend

Este es el backend de la aplicación OCR para procesar recibos, desarrollado con FastAPI y Tesseract.

## ¿Por qué FastAPI?

Elegí FastAPI para este proyecto por varias razones que se alinean perfectamente con los requisitos de la prueba técnica y mis preferencias de desarrollo:

### Requisito de la Prueba Técnica
La prueba técnica específicamente menciona el uso de FastAPI, lo cual fue determinante en la elección. Sin embargo, más allá del requisito, FastAPI resultó ser una excelente opción por las siguientes razones.

### Primera Experiencia Positiva
Aunque no había trabajado previamente con FastAPI, me sorprendió gratamente lo rápido que pude crear un backend funcional como prototipo. La curva de aprendizaje fue muy suave comparada con otros frameworks que he usado.

### Ventajas que Descubrí

#### Desarrollo Rápido de Prototipos
- **Documentación automática**: FastAPI genera automáticamente documentación interactiva en `/docs`
- **Validación automática**: Los tipos de Python se convierten automáticamente en validaciones
- **Serialización JSON nativa**: Manejo automático de conversiones de datos
- **Hot reload**: Cambios instantáneos durante el desarrollo

#### Integración Perfecta con Tesseract
- **Manejo de archivos multipart**: Soporte nativo para subida de archivos
- **Procesamiento asíncrono**: Ideal para operaciones de OCR que pueden tomar tiempo
- **Manejo de errores robusto**: Sistema de excepciones bien estructurado

#### Experiencia de Desarrollo Superior
- **Type hints**: Aprovecha completamente el sistema de tipos de Python
- **Async/await nativo**: Rendimiento superior para operaciones I/O
- **Middleware flexible**: Fácil configuración de CORS y otros middlewares
- **Testing integrado**: Herramientas de testing incluidas

## ¿Por qué Tesseract OCR?

### Experiencia Previa
He usado Tesseract en proyectos anteriores y, aunque reconozco que la documentación ya no está tan actualizada como me gustaría, mi experiencia pasada me ha demostrado que es una herramienta muy cómoda y confiable para implementar OCR.

### Ventajas Prácticas
- **Gratuito y open source**: Sin costos de licenciamiento
- **Soporte multiidioma**: Perfecto para recibos en español e inglés
- **Integración sencilla**: La biblioteca `pytesseract` hace la integración muy directa
- **Configuración flexible**: Permite ajustar parámetros para diferentes tipos de documentos
- **Comunidad activa**: A pesar de la documentación desactualizada, hay mucho soporte comunitario

### Configuración Optimizada para Recibos
He configurado Tesseract específicamente para el reconocimiento de recibos:
- **PSM 6**: Optimizado para bloques uniformes de texto
- **Whitelist de caracteres**: Limitado a caracteres comunes en recibos
- **Preprocesamiento**: Conversión a escala de grises para mejor reconocimiento

## Tecnologías Utilizadas

- **FastAPI 0.104.1**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Tesseract OCR**: Motor de reconocimiento óptico de caracteres
- **Pillow (PIL)**: Procesamiento de imágenes en Python
- **pytesseract**: Wrapper de Python para Tesseract
- **python-multipart**: Manejo de formularios multipart

## Arquitectura del Sistema

### Flujo de Procesamiento
1. **Recepción**: El endpoint recibe la imagen via multipart/form-data
2. **Validación**: Verifica formato, tamaño y integridad del archivo
3. **Preprocesamiento**: Convierte la imagen para optimizar el OCR
4. **OCR**: Extrae el texto usando Tesseract con configuración personalizada
5. **Postprocesamiento**: Limpia y formatea el texto extraído
6. **Respuesta**: Devuelve el resultado en formato JSON

### Manejo de Errores
- **Validación de entrada**: Formatos soportados y límites de tamaño
- **Errores de Tesseract**: Manejo específico para problemas de OCR
- **Errores de imagen**: Validación de integridad de archivos
- **Logging detallado**: Para debugging y monitoreo

## Estructura del Proyecto

```
backend/
├── main.py              # Aplicación principal FastAPI
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Documentación (este archivo)
```

### Justificación de la Estructura Simple
Mantuve una estructura simple por las siguientes razones:
- **Prototipo rápido**: Para esta prueba técnica, una estructura simple es más eficiente
- **Fácil comprensión**: Cualquier desarrollador puede entender el código rápidamente
- **Escalabilidad futura**: La estructura puede expandirse fácilmente cuando sea necesario

## Endpoints Implementados

### `GET /`
**Propósito**: Health check básico para verificar que la API está funcionando
**Respuesta**: Estado básico del servicio

### `GET /health`
**Propósito**: Health check detallado con información del sistema
**Justificación**: Esencial para monitoreo en producción, incluye estado de Tesseract

### `POST /upload-ocr`
**Propósito**: Endpoint principal para procesamiento OCR
**Justificación**: 
- Nombre descriptivo que indica claramente su función
- Método POST apropiado para subida de archivos
- Respuesta estructurada para fácil integración con frontend

## Configuración de CORS

Configuré CORS específicamente para permitir comunicación con el frontend Next.js:
```python
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### Justificación
- **Desarrollo local**: Permite testing desde el frontend en desarrollo
- **Seguridad**: Restringe acceso solo a orígenes conocidos
- **Flexibilidad**: Fácil de expandir para producción

## Optimizaciones Implementadas

### Configuración de Tesseract
```python
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:-$€£¥₹ '
```

**Justificación de cada parámetro**:
- `--oem 3`: Usa el motor OCR más estable
- `--psm 6`: Optimizado para bloques de texto como recibos
- `tessedit_char_whitelist`: Limita a caracteres comunes en recibos, mejora precisión

### Preprocesamiento de Imágenes
- **Conversión a escala de grises**: Mejora el contraste para OCR
- **Validación de formato**: Asegura compatibilidad con Tesseract
- **Manejo de diferentes modos de color**: Convierte automáticamente a RGB

## Instalación y Configuración

### Requisitos del Sistema
- **Python 3.8+**: Compatibilidad con FastAPI y type hints modernos
- **Tesseract OCR**: Motor de OCR instalado en el sistema
- **Paquetes de idioma**: Español e inglés para reconocimiento multiidioma

### Instalación Paso a Paso

#### 1. Tesseract OCR
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-spa

# macOS
brew install tesseract tesseract-lang

# Windows
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
```

### Ejecución
```bash
# Desarrollo
python main.py

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Testing y Debugging

### Endpoints de Verificación
- **`/health`**: Verifica estado de Tesseract y configuración
- **Logs detallados**: Información completa sobre procesamiento y errores
- **Documentación automática**: Disponible en `/docs` para testing interactivo

### Debugging Common Issues
1. **"Tesseract not found"**: Verificar instalación y PATH
2. **Errores de CORS**: Confirmar configuración de orígenes permitidos
3. **Calidad de OCR baja**: Ajustar parámetros de preprocesamiento

## Consideraciones de Producción

### Seguridad
- **Validación de archivos**: Límites de tamaño y formato
- **Rate limiting**: Considerar implementar para evitar abuso
- **Autenticación**: Agregar si es necesario para uso en producción

### Performance
- **Procesamiento asíncrono**: FastAPI maneja múltiples requests concurrentemente
- **Optimización de memoria**: Limpieza automática de imágenes procesadas
- **Caching**: Considerar cache para imágenes procesadas frecuentemente

### Escalabilidad
- **Workers múltiples**: Usar Gunicorn con workers Uvicorn
- **Load balancing**: Distribuir carga entre múltiples instancias
- **Monitoreo**: Implementar métricas y alertas

## Próximas Mejoras

### Funcionalidades
- [ ] Soporte para más formatos de imagen (TIFF, BMP)
- [ ] Procesamiento por lotes
- [ ] API de configuración dinámica de Tesseract
- [ ] Historial de procesamiento
- [ ] Métricas de precisión de OCR

### Técnicas
- [ ] Preprocesamiento avanzado de imágenes
- [ ] Integración con servicios de ML en la nube
- [ ] Cache distribuido con Redis
- [ ] Base de datos para persistencia
- [ ] Autenticación JWT

## Lecciones Aprendidas

### FastAPI
- La documentación automática es increíblemente útil para desarrollo y testing
- El sistema de validación automática ahorra mucho tiempo de desarrollo
- La integración con Python type hints hace el código más mantenible

### Tesseract
- La configuración correcta es crucial para buenos resultados
- El preprocesamiento de imágenes puede mejorar significativamente la precisión
- Los parámetros PSM deben ajustarse según el tipo de documento

### Desarrollo de APIs
- El manejo robusto de errores es esencial para una buena experiencia de usuario
- Los logs detallados facilitan enormemente el debugging
- La validación temprana de entrada previene muchos problemas downstream

Esta experiencia me ha convencido de que FastAPI es una excelente opción para APIs modernas, especialmente cuando se necesita desarrollo rápido sin sacrificar robustez y performance.