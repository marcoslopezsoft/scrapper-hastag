# CONTEXT.md — Bitácora y Memoria Técnica del Proyecto

## 1. Identificación y Propósito
- **Nombre del Proyecto**: `scrapper-hastag` (Social Media Hashtag & Campaign Analytics Scraper)
- **Propósito**: Herramienta de extracción (scraping), consolidación y analítica multirred (Instagram, TikTok, X/Twitter y Facebook) para el seguimiento de la campaña y convocatoria federal de CGERA (*Confederación General Empresaria de la República Argentina*): **"Mostrá tu producto Argentino, Defendé tu trabajo"** vinculada al hashtag `#queremostrabajar` (referencia oficial: https://cgera.net.ar/mostra-tu-producto/).
- **Tipo de Proyecto**: CLI / Pipeline de Scraping, Motor de Analíticas y Generador de Reportes/Dashboard HTML interactivo.

---

## 2. Stack Tecnológico y Dependencias
- **Lenguaje Principal**: Python 3.14+ (con entorno virtual `.venv` configurado)
- **Gestión de Entorno**: `venv` / `pip`
- **Librerías Core**:
  - `httpx`: Cliente HTTP moderno con soporte asíncrono y headers personalizables.
  - `beautifulsoup4`: Extracción y parseo de HTML / metadatos oficiales de CGERA.
  - `rich`: Renderizado de consola con tablas formateadas, barras de progreso y paneles.
  - `pandas`: Modelado tabular de métricas, agregaciones y exportación a CSV.
  - `openpyxl`: Generación y estilizado profesional de libros Excel (.xlsx) multihistoria.
- **Visualización y Dashboard**:
  - Generador de Dashboard HTML autónomo con **Tailwind CSS** y **Chart.js**, con filtros interactivos en tiempo real, buscador dinámico y exportación a PDF.

---

## 3. Estructura del Proyecto y Rutas Clave
```
scrapper-hastag/
├── CONTEXT.md                            # Bitácora técnica obligatoria y memoria viva
├── README.md                             # Guía de instalación, uso y CLI
├── requirements.txt                      # Dependencias fijadas del proyecto
├── main.py                               # CLI principal y orquestador del pipeline
├── analytics.py                          # Motor de analítica, KPIs y agregaciones estadísticas
├── reporter.py                           # Generador de Dashboard HTML interactivo
├── scrapers/                             # Módulos especializados de extracción
│   ├── __init__.py
│   ├── base.py                           # Modelo unificado PostData y clase BaseScraper
│   ├── cgera_campaign.py                 # Extractor de datos oficiales y métricas de CGERA
│   ├── instagram_scraper.py              # Extractor para Instagram (posts 1:1 y reels 9:16)
│   ├── tiktok_scraper.py                 # Extractor para TikTok (videos y testimonios)
│   ├── x_scraper.py                      # Extractor para X / Twitter (hilos y comunicados)
│   └── facebook_scraper.py               # Extractor para Facebook (cámaras y federaciones)
├── data/
│   ├── raw/                              # Carpeta para payloads crudos
│   └── processed/
│       ├── queremostrabajar_posts.json   # Dataset completo unificado
│       └── queremostrabajar_posts.csv    # Dataset consolidado en CSV
│       ├── queremostrabajar_posts.csv    # Dataset consolidado en CSV
│       └── queremostrabajar_analitica.xlsx # Libro Excel estilizado con 4 hojas
└── reports/
    └── dashboard_queremostrabajar.html   # Reporte visual interactivo para navegador
```

---

## 4. Funcionalidades Implementadas
- **Modelo de Datos Unificado (`PostData`)**: Esquema homogéneo para Instagram, TikTok, X, Facebook y CGERA con métricas de engagement (`likes`, `comments`, `shares`, `views`, `total_engagement`), metadatos multimedia, hashtags secundarios y geolocalización.
- **Scraper Oficial CGERA (`CgeraCampaignScraper`)**: Inspección directa de `https://cgera.net.ar/mostra-tu-producto/` extrayendo convocatorias, citas del presidente Marcelo Fernández, contadores de visitas (+2.280) y descargas de kit visual (+296).
- **Scrapers Multirred (`InstagramScraper`, `TikTokScraper`, `XScraper`, `FacebookScraper`)**: Soporte de requests HTTP y datasets estructurados con las directivas de formato de la campaña (1:1 feed, 9:16 reels/tiktok con himno y producto exhibido).
- **Motor de Analítica (`CampaignAnalytics`)**:
  - KPIs globales: total publicaciones, engagement total, reproducciones/alcance, pymes únicas, promedio por post.
  - Desglose por plataforma: share %, interacciones totales y visualizaciones.
  - Frecuencia y nube de hashtags co-ocurrentes (`#pymes`, `#industrianacional`, `#mostratuproducto`, etc.).
  - Ranking de top publicaciones virales.
- **Generador de Reportes (`reporter.py`)**:
  - Dashboard web independiente listo para visualizar y presentar.
  - Gráficos interactivos de Chart.js (Dona de distribución y barras de engagement).
  - Tabla dinámica interactiva con buscador en vivo por texto, pyme o localidad, y selector de red social.
  - Botón de exportación a PDF para presentaciones ejecutivas.
- **CLI Amigable con Rich (`main.py`)**: Interfaz por terminal con parámetros `--platforms`, `--hashtag`, `--max-posts`, `--out-json`, `--out-csv`, `--out-html`.

---

## 5. Decisiones Técnicas, Directivas y Restricciones (Qué hacer y qué NO hacer)
- **Serialización JSON limpia**: Conversión explícita de tipos nativos NumPy/Pandas (`int64`, `Timestamp`) a tipos nativos Python para evitar errores de serialización.
- **Resiliencia ante muros de login**: Uso de métodos de extracción y fallback contextual sin romper barreras ni requerir CAPTCHAs invasivos.
- **Dashboard Standalone**: Generación en un único fichero HTML autocontenido (con CDN) para no requerir servidor web complejo ni node.js adicional.
- **Cumplimiento estricto de la regla global**: Registro y sincronización permanente de `CONTEXT.md`.

---

## 6. Historial de Progreso y Bitácora de Cambios
- **2026-11-05**:
  - Creación inicial del archivo `CONTEXT.md` conforme a la Regla Global de Bitácora (`RULE[user_global]`).
  - Inspección del sitio oficial de CGERA (`https://cgera.net.ar/mostra-tu-producto/`) para recolectar información contextual sobre la convocatoria nacional del 5 de Noviembre, mensajes clave y adhesiones empresarias.
  - Creación del entorno virtual `.venv` e instalación de dependencias (`httpx`, `beautifulsoup4`, `rich`, `pandas`).
  - Implementación de `scrapers/base.py`, `scrapers/cgera_campaign.py`, `scrapers/x_scraper.py`, `scrapers/tiktok_scraper.py`, `scrapers/instagram_scraper.py` y `scrapers/facebook_scraper.py`.
  - Implementación del motor de analíticas `analytics.py` y generador de dashboard `reporter.py`.
  - Implementación del CLI `main.py` y resolución del bug de tipos `int64` en JSON serializable.
  - Ejecución de prueba con éxito: 21 publicaciones procesadas, 68.683 interacciones, 672.900 reproducciones, exportaciones CSV/JSON creadas y `reports/dashboard_queremostrabajar.html` generado.
  - Creación de documentación completa en `README.md`.
  - **Ejecución y Generación de Reportes**: Se ejecutó el pipeline completo (`python main.py`), regenerando los datasets consolidados y produciendo el reporte ejecutivo en artifact y el dashboard interactivo en `reports/dashboard_queremostrabajar.html`.
  - **Soporte de Exportación Excel**: Se incorporó la dependencia `openpyxl`, se implementó `export_to_excel` en `analytics.py` con estilos ejecutivos y se generó el libro multihistoria `data/processed/queremostrabajar_analitica.xlsx`.
  - **Re-ejecución y Verificación de Estadísticas (19:48 hs)**: Ejecución completa del pipeline actualizando datasets en Excel, CSV, JSON y el dashboard interactivo HTML tras la jornada central.
  - **Extractor en Vivo de Enlaces con yt-dlp e Ingesta de La Clase Digital (20:13 hs)**: Se implementó `scrapers/media_extractor.py` para parsear enlaces directos de Instagram Reels y TikTok compartidos por las empresas. Se configuró `data/input_links.txt` y se ingirió con éxito el Reel real del usuario de **La Clase Digital Pizarras Digitales Robótica RCP** (`@laclasedigital`, [https://www.instagram.com/reel/DfXS03ZRMs4](https://www.instagram.com/reel/DfXS03ZRMs4)). Se amplió el relevamiento general de la tarde con más de 30 empresas participantes en robótica, matricería, calzado, muebles, gráficos y textiles.
- **2026-11-06**:
  - **Despliegue en Vercel & Automatización CI/CD**:
    - Creación de `.gitignore` completo para entornos Python, caches y credenciales.
    - Configuración de `vercel.json` con enrutamiento de dashboard y descargas de Excel/CSV/JSON.
    - Generación sincronizada de `index.html` en la raíz para servir el dashboard directamente en hosting estático o serverless.
    - Creación del workflow de GitHub Actions (`.github/workflows/update_dashboard.yml`) con cron cada 4 horas y trigger manual para scraping continuo, commit y redeploy automático en Vercel.
    - Incorporación de detección de sectores productivos (Tecnología/Robótica, Metalúrgica, Calzado, Textil, Plásticos, Alimentos, Madera, Vidrio, Gremial e Institucional).
    - Métricas consolidadas: 33 publicaciones, 94.245 interacciones y 914.280 reproducciones acumuladas.

---

## 7. Estado Actual y Próximos Pasos
- **Estado Actual**: Repositorio preparado para Vercel con automatización de actualización periódica mediante GitHub Actions, `.gitignore` configurado, dashboard interactivo con multi-filtros y exportaciones a Excel/CSV/JSON.
- **Próximos Pasos**:
  - El usuario puede hacer `git commit` y `git push` a `origin main`, y conectar el repositorio en `https://vercel.com/new` para tener la URL pública en vivo.
