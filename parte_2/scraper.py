import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BookScraper:
    def __init__(self):
        self.base_url = "http://books.toscrape.com/catalogue/"
        self.session = requests.Session()
        # Agregar headers para evitar ser bloqueado
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_books(self) -> List[Dict]:
        """
        Hacer scraping de libros desde books.toscrape.com
        
        Retorna:
            List[Dict]: Lista de diccionarios de libros con título, precio, categoría y calificación
        """
        url = "http://books.toscrape.com/catalogue/page-1.html"
        books = []
        page_count = 0
        max_pages = 50  # Límite para prevenir bucles infinitos
        
        logger.info("Iniciando proceso de scraping de libros...")
        
        while url and page_count < max_pages:
            try:
                logger.info(f"Haciendo scraping de página {page_count + 1}: {url}")
                
                # Agregar delay aleatorio para ser respetuoso con el servidor
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(url, timeout=10)
                
                if response.status_code != 200:
                    logger.warning(f"La página retornó estado {response.status_code}: {url}")
                    break
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Verificar si la página tiene productos
                articles = soup.select(".product_pod")
                if not articles:
                    logger.warning(f"No se encontraron productos en la página: {url}")
                    break
                
                # Extraer datos de libros de cada artículo
                for article in articles:
                    try:
                        book_data = self._extract_book_data(article)
                        if book_data:
                            books.append(book_data)
                    except Exception as e:
                        logger.error(f"Error extrayendo datos del libro: {str(e)}")
                        continue
                
                logger.info(f"Extraídos {len(articles)} libros de la página {page_count + 1}")
                
                # Buscar siguiente página
                next_btn = soup.select_one(".next a")
                if next_btn and next_btn.get("href"):
                    next_page = next_btn["href"]
                    url = self.base_url + next_page
                    page_count += 1
                else:
                    logger.info("No se encontraron más páginas, scraping completo")
                    break
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error de petición para {url}: {str(e)}")
                break
            except Exception as e:
                logger.error(f"Error inesperado haciendo scraping de {url}: {str(e)}")
                break
        
        logger.info(f"Scraping completado. Total de libros encontrados: {len(books)}")
        return books
    
    def _extract_book_data(self, article) -> Dict:
        """
        Extraer datos del libro de un elemento artículo individual
        
        Argumentos:
            article: Elemento BeautifulSoup que contiene datos del libro
            
        Retorna:
            Dict: Diccionario de datos del libro
        """
        try:
            # Extraer título
            title_element = article.select_one("h3 a")
            if not title_element:
                return None
            title = title_element.get("title", "").strip()
            
            # Extraer precio
            price_element = article.select_one(".price_color")
            if not price_element:
                return None
            price_text = price_element.text.strip()
            # Remover símbolo de moneda y convertir a float
            price = float(price_text.replace("£", "").replace("$", ""))
            
            # Extraer calificación
            rating_element = article.select_one("p[class*='star-rating']")
            rating = 0
            if rating_element:
                rating_class = rating_element.get("class", [])
                rating_words = ["Zero", "One", "Two", "Three", "Four", "Five"]
                for class_name in rating_class:
                    if class_name in rating_words:
                        rating = rating_words.index(class_name)
                        break
            
            # La categoría es general para este sitio
            category = "Books"
            
            return {
                "title": title,
                "price": price,
                "category": category,
                "rating": rating
            }
            
        except Exception as e:
            logger.error(f"Error extrayendo datos del libro: {str(e)}")
            return None

# Crear instancia del scraper
scraper = BookScraper()

def scrape_books() -> List[Dict]:
    """
    Función principal para hacer scraping de libros
    
    Retorna:
        List[Dict]: Lista de diccionarios de libros
    """
    return scraper.scrape_books()