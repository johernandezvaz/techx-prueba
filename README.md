Esta es la aplicación frontend desarrollada con Next.js para procesar recibos usando OCR (Reconocimiento Óptico de Caracteres).

## ¿Por qué Next.js?

Elegí Next.js para este proyecto por varias razones fundamentales:

### Recomendaciones de la Comunidad
Después de investigar en varios foros de desarrollo y comunidades como Reddit, Stack Overflow y Discord, Next.js consistentemente aparece como la opción más recomendada para aplicaciones React modernas. La comunidad destaca especialmente su facilidad de uso y excelente documentación.

### Integración Directa con FastAPI
Vercel (los creadores de Next.js) proporcionan plantillas oficiales que facilitan enormemente la conexión entre Next.js y FastAPI. Esta integración nativa me permitió configurar rápidamente la comunicación entre el frontend y el backend sin configuraciones complejas.

### Experiencia de Desarrollo Superior
Recientemente he estado trabajando más con Next.js y he notado las siguientes ventajas que me resultan muy cómodas:

- **Hot Reload instantáneo**: Los cambios se reflejan inmediatamente sin perder el estado
- **Routing automático**: No necesito configurar rutas manualmente
- **Optimización automática**: Next.js optimiza automáticamente las imágenes, fuentes y código
- **TypeScript integrado**: Soporte nativo sin configuración adicional
- **API Routes**: Puedo crear endpoints del lado del servidor si es necesario
- **Deployment sencillo**: Vercel hace el deployment extremadamente simple

### Ventajas Técnicas
- **Server-Side Rendering (SSR)**: Mejor SEO y performance inicial
- **Static Site Generation (SSG)**: Para páginas que no cambian frecuentemente
- **Image Optimization**: Optimización automática de imágenes
- **Bundle Splitting**: Carga solo el código necesario
- **Built-in CSS Support**: Soporte nativo para CSS Modules y Styled Components

## Tecnologías Utilizadas

- **Next.js 13.5.1**: Framework React con App Router
- **TypeScript**: Para tipado estático y mejor experiencia de desarrollo
- **Tailwind CSS**: Framework CSS utility-first para diseño rápido y consistente
- **shadcn/ui**: Biblioteca de componentes UI moderna y accesible
- **Lucide React**: Iconos SVG optimizados y consistentes
- **Sonner**: Sistema de notificaciones toast elegante y funcional

## Estructura del Proyecto

```
src/
├── app/
│   ├── api/
│   │   └── upload-ocr/
│   │       └── route.ts      # API route para comunicación con FastAPI
│   ├── globals.css           # Estilos globales y variables CSS
│   ├── layout.tsx            # Layout principal de la aplicación
│   └── page.tsx              # Página principal con funcionalidad OCR
├── components/
│   └── ui/                   # Componentes UI de shadcn/ui
├── hooks/                    # Custom hooks de React
└── lib/
    └── utils.ts              # Utilidades y helpers
```

## Funcionalidades Principales

### 1. Interfaz de Usuario Moderna
- Diseño minimalista y profesional
- Totalmente responsivo para móviles y desktop
- Animaciones suaves y micro-interacciones
- Tema consistente con variables CSS personalizadas

### 2. Subida de Archivos Intuitiva
- **Drag & Drop**: Arrastra archivos directamente al área de subida
- **Click to Upload**: Selección tradicional de archivos
- **Vista previa**: Muestra la imagen seleccionada antes de procesar
- **Validación**: Solo acepta PNG y JPEG, máximo 10MB

### 3. Procesamiento OCR
- Comunicación directa con la API FastAPI
- Estados de carga con spinner animado
- Manejo robusto de errores
- Feedback visual inmediato

### 4. Gestión de Resultados
- **Textarea de solo lectura**: Muestra el texto extraído
- **Fuente monoespaciada**: Mejor legibilidad del texto
- **Botón de copiado**: Copia el texto al portapapeles con un clic
- **Scroll automático**: Para textos largos

### 5. Sistema de Notificaciones
- Notificaciones toast elegantes con Sonner
- Feedback inmediato para todas las acciones
- Mensajes de éxito y error contextuales

## Rutas y API

### Frontend Routes
- `/` - Página principal con funcionalidad OCR

### API Routes
- `POST /api/upload-ocr` - Proxy hacia FastAPI para procesar imágenes

#### Justificación de la Ruta API
Creé una ruta API en Next.js (`/api/upload-ocr`) que actúa como proxy hacia FastAPI por las siguientes razones:

1. **Manejo de CORS**: Evita problemas de CORS al hacer las peticiones desde el servidor
2. **Seguridad**: Permite ocultar la URL real del backend FastAPI
3. **Validación adicional**: Puedo agregar validaciones del lado de Next.js si es necesario
4. **Logging centralizado**: Mejor control sobre los logs y errores
5. **Flexibilidad**: Facilita cambios futuros en la arquitectura del backend

## Instalación y Desarrollo

### Requisitos Previos
- Node.js 18+ 
- npm o yarn
- Backend FastAPI corriendo en `http://localhost:8000`

### Instalación
```bash
# Clonar el repositorio
git clone [url-del-repo]
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

### Scripts Disponibles
```bash
npm run dev          # Servidor de desarrollo
npm run build        # Build para producción
npm run start        # Servidor de producción
npm run lint         # Linter ESLint
```

## Configuración

### Configuración de Tailwind
El proyecto usa Tailwind CSS con configuración personalizada en `tailwind.config.ts`:
- Variables CSS personalizadas para temas
- Animaciones personalizadas
- Breakpoints responsivos optimizados


## Consideraciones de Diseño

### Principios de UX/UI
- **Simplicidad**: Interfaz limpia sin elementos innecesarios
- **Feedback inmediato**: El usuario siempre sabe qué está pasando
- **Accesibilidad**: Componentes accesibles con shadcn/ui
- **Consistencia**: Uso coherente de colores, espaciado y tipografía

### Responsive Design
- Mobile-first approach
- Breakpoints optimizados para tablets y desktop
- Componentes que se adaptan fluidamente
- Touch-friendly en dispositivos móviles

### Performance
- Lazy loading de componentes
- Optimización automática de imágenes
- Bundle splitting automático
- Prefetch de rutas críticas

## Próximas Posibles Mejoras

- [ ] Historial de procesamiento de recibos
- [ ] Soporte para múltiples idiomas
- [ ] Modo oscuro/claro
- [ ] Procesamiento por lotes
- [ ] Exportación de resultados (PDF, CSV)
- [ ] Integración con servicios de almacenamiento en la nube

## Troubleshooting

### Error de conexión con FastAPI
1. Verifica que el backend esté corriendo en `http://localhost:8000`
2. Revisa la configuración de CORS en FastAPI
3. Confirma que la variable `FASTAPI_URL` esté configurada correctamente

### Problemas de build
1. Limpia el cache: `rm -rf .next`
2. Reinstala dependencias: `rm -rf node_modules && npm install`
3. Verifica la versión de Node.js (requiere 18+)

### Estilos no se aplican
1. Verifica que Tailwind esté configurado correctamente
2. Revisa que los paths en `tailwind.config.ts` incluyan todos los archivos
3. Asegúrate de que `globals.css` esté importado en `layout.tsx`