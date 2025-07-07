import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Optional
import logging

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError("Las variables de entorno SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY son requeridas")

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

class ProductDatabase:
    def __init__(self):
        self.supabase = supabase
    
    def insert_product(self, product_data: Dict) -> bool:
        """Insertar un solo producto en la base de datos"""
        try:
            # Verificar si el producto ya existe
            existing = self.supabase.table("products").select("id").eq("title", product_data["title"]).execute()
            
            if existing.data:
                logger.info(f"El producto '{product_data['title']}' ya existe, omitiendo...")
                return False
            
            # Insertar nuevo producto
            result = self.supabase.table("products").insert(product_data).execute()
            
            if result.data:
                logger.info(f"Producto insertado exitosamente: {product_data['title']}")
                return True
            else:
                logger.error(f"Error al insertar producto: {product_data['title']}")
                return False
                
        except Exception as e:
            logger.error(f"Error insertando producto {product_data['title']}: {str(e)}")
            return False
    
    def insert_products_batch(self, products: List[Dict]) -> int:
        """Insertar múltiples productos en lote"""
        inserted_count = 0
        
        for product in products:
            if self.insert_product(product):
                inserted_count += 1
        
        return inserted_count
    
    def get_products(self, 
                    title: Optional[str] = None,
                    category: Optional[str] = None,
                    min_price: Optional[float] = None,
                    max_price: Optional[float] = None) -> List[Dict]:
        """Obtener productos con filtros opcionales"""
        try:
            query = self.supabase.table("products").select("*")
            
            # Aplicar filtros
            if title:
                query = query.ilike("title", f"%{title}%")
            if category:
                query = query.ilike("category", f"%{category}%")
            if min_price is not None:
                query = query.gte("price", min_price)
            if max_price is not None:
                query = query.lte("price", max_price)
            
            # Ejecutar consulta
            result = query.execute()
            
            if result.data:
                return result.data
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error obteniendo productos: {str(e)}")
            return []
    
    def get_categories(self) -> List[str]:
        """Obtener todas las categorías únicas"""
        try:
            result = self.supabase.table("products").select("category").execute()
            
            if result.data:
                categories = list(set([item["category"] for item in result.data]))
                return sorted(categories)
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error obteniendo categorías: {str(e)}")
            return []

# Inicializar instancia de base de datos
db = ProductDatabase()