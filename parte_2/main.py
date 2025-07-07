from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import db
from scraper import scrape_books
from typing import List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Web Scraper",
    description="API para scraping de productos con filtros avanzados",
    version="1.0.0"
)

# Agregar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "API de Web Scraper",
        "version": "1.0.0",
        "endpoints": {
            "/scrape": "Ejecutar el web scraper",
            "/products": "Obtener productos con filtros",
            "/categories": "Obtener todas las categorías disponibles"
        }
    }

@app.post("/scrape")
def run_scraper():
    """
    Ejecutar el web scraper y guardar productos en la base de datos
    
    Retorna:
        dict: Mensaje con número de productos guardados
    """
    try:
        logger.info("Iniciando proceso de web scraping...")
        books = scrape_books()
        
        if not books:
            return {"message": "No se encontraron productos durante el scraping", "count": 0}
        
        # Insertar productos en la base de datos
        inserted_count = db.insert_products_batch(books)
        
        logger.info(f"Scraping completado. {inserted_count} productos nuevos guardados.")
        
        return {
            "message": f"Scraping completado exitosamente",
            "total_scrapeado": len(books),
            "productos_nuevos_guardados": inserted_count,
            "duplicados_omitidos": len(books) - inserted_count
        }
        
    except Exception as e:
        logger.error(f"Error durante el scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping falló: {str(e)}")

@app.get("/products")
def get_products(
    title: Optional[str] = Query(None, description="Filtrar por título del producto (coincidencia parcial)"),
    category: Optional[str] = Query(None, description="Filtrar por categoría (coincidencia parcial)"),
    min_price: Optional[float] = Query(None, ge=0, description="Filtro de precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Filtro de precio máximo"),
    limit: Optional[int] = Query(100, ge=1, le=1000, description="Número máximo de resultados")
):
    """
    Obtener productos con filtros opcionales
    
    Argumentos:
        title: Filtrar por título del producto (coincidencia parcial sin distinción de mayúsculas)
        category: Filtrar por categoría (coincidencia parcial sin distinción de mayúsculas)
        min_price: Precio mínimo (inclusivo)
        max_price: Precio máximo (inclusivo)
        limit: Número máximo de resultados a retornar
    
    Retorna:
        List[dict]: Lista de productos que coinciden con los filtros
    """
    try:
        # Validar rango de precios
        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(
                status_code=400, 
                detail="min_price no puede ser mayor que max_price"
            )
        
        products = db.get_products(
            title=title,
            category=category,
            min_price=min_price,
            max_price=max_price
        )
        
        # Aplicar límite
        if limit and len(products) > limit:
            products = products[:limit]
        
        return {
            "productos": products,
            "cantidad": len(products),
            "filtros_aplicados": {
                "title": title,
                "category": category,
                "min_price": min_price,
                "max_price": max_price,
                "limit": limit
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo productos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")

@app.get("/categories")
def get_categories():
    """
    Obtener todas las categorías de productos disponibles
    
    Retorna:
        dict: Lista de categorías únicas
    """
    try:
        categories = db.get_categories()
        return {
            "categorias": categories,
            "cantidad": len(categories)
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo categorías: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")

@app.get("/health")
def health_check():
    """Endpoint de verificación de salud"""
    return {"estado": "saludable", "servicio": "API de Web Scraper"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)