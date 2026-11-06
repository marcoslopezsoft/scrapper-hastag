# Scraper y Analítica de Redes Sociales: Campaña `#queremostrabajar` (CGERA)

Herramienta especializada para la extracción, unificación y análisis de analíticas y convocatorias en torno al hashtag oficial **`#queremostrabajar`** correspondiente a la campaña nacional de **CGERA** (*Confederación General Empresaria de la República Argentina*): **"Mostrá tu producto Argentino, Defendé tu trabajo"** (Jueves 5 de Noviembre, 12:00 HS).

Referencia oficial del evento: [https://cgera.net.ar/mostra-tu-producto/](https://cgera.net.ar/mostra-tu-producto/)

---

## 🎯 Plataformas Soportadas
- **Instagram**: Publicaciones del feed, reels y carruseles (formatos 1:1 y 9:16).
- **TikTok**: Videos testimoniales verticales con sonido ambiental/himno y producto en mano.
- **X (Twitter)**: Convocatorias de cámaras industriales, empresarios, hilos y fotos en puerta de fábrica.
- **Facebook**: Comunicados de federaciones comerciales provinciales y cámaras pymes.
- **CGERA Oficial**: Extracción directa de métricas de la web oficial (+2.280 visitas, descargas de kit visual, adhesiones).

---

## 🚀 Instalación y Requisitos

Requiere **Python 3.10+**.

```bash
# 1. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

---

## 💻 Uso de la CLI

### 1. Ejecutar análisis completo (todas las redes + CGERA)
```bash
python main.py
```

### 2. Filtrar por redes específicas
```bash
# Solo Instagram y TikTok
python main.py --platforms ig,tiktok

# Solo X (Twitter) y Facebook
python main.py --platforms x,fb
```

### 3. Personalizar el hashtag o el límite de posts
```bash
python main.py --hashtag queremostrabajar --max-posts 50
```

### 4. Rutas personalizadas de exportación
```bash
python main.py \
  --out-json data/processed/analitica.json \
  --out-csv data/processed/analitica.csv \
  --out-html reports/dashboard_queremostrabajar.html
```

---

## 📊 Dashboard Interactivo HTML

Al finalizar la ejecución, se genera automáticamente un reporte visual ejecutivo en:
`reports/dashboard_queremostrabajar.html`

### Características del Dashboard:
- **Tarjetas de KPIs**: Total de publicaciones, interacciones (likes + comentarios + shares), vistas acumuladas, pymes únicas y promedio de engagement.
- **Gráficos interactivos (Chart.js)**:
  - Dona de cuota de mercado por red social.
  - Barras comparativas de engagement por plataforma.
- **Top Convocatorias**: Muestra los testimonios y videos con mayor impacto de la jornada nacional.
- **Explorador y Tabla Dinámica**: Buscador en tiempo real por pyme, ciudad o contenido del post, y filtro por red social.
- **Acceso directo**: Enlaces directos a cada post original y opción de exportación a PDF / impresión con un clic.

---

## 🎈 Dashboard Interactivo en Streamlit (`app.py`)

Se desarrolló una aplicación web interactiva nativa en **Streamlit** con gráficos en **Plotly**:

### 1. Ejecutar localmente en tu máquina:
```bash
source .venv/bin/activate
streamlit run app.py
```
Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

### 2. Despliegue Gratuito en 1 Clic (Streamlit Community Cloud):
Streamlit ofrece hosting oficial gratuito para repositorios de GitHub con sincronización automática:
1. Subí los cambios a tu repositorio:
   ```bash
   git add .
   git commit -m "feat: agregar dashboard interactivo en streamlit app.py"
   git push origin main
   ```
2. Entrá a **[share.streamlit.io](https://share.streamlit.io/)** e iniciá sesión con tu cuenta de GitHub.
3. Hacé clic en **"New app"** y seleccioná:
   - **Repository**: `marcoslopezsoft/scrapper-hastag`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Hacé clic en **"Deploy"**.
5. ¡Listo! En menos de 2 minutos vas a tener una URL pública como `https://scrapper-hastag.streamlit.app/`.

---

## 🌐 Despliegue en Vercel & Actualización Automática

El proyecto está preparado para desplegarse de inmediato en **Vercel** y actualizarse automáticamente con el paso de las horas:

### 1. Despliegue en Vercel (1 clic)
1. Subí tus cambios a tu repositorio en GitHub:
   ```bash
   git add .
   git commit -m "feat: dashboard analítico y configuración vercel"
   git push origin main
   ```
2. Entrá a [https://vercel.com/new](https://vercel.com/new) e importá tu repositorio `scrapper-hastag`.
3. Vercel detectará automáticamente el archivo `vercel.json` y el `index.html`. Hacé clic en **Deploy**.
4. ¡Listo! Ya tenés tu dashboard online con dominio gratuito `.vercel.app`.

### 2. Actualización Automática Continua (GitHub Actions)
- Se incluye el workflow [`.github/workflows/update_dashboard.yml`](.github/workflows/update_dashboard.yml).
- **Frecuencia**: Se ejecuta automáticamente **cada 4 horas** mediante un cron de GitHub Actions.
- **Acción**: Corre el scraper, actualiza los datos y hace commit a `main`.
- **Auto-redeploy**: Cada vez que GitHub Actions actualiza los datos en `main`, **Vercel detecta el commit y re-despliega el dashboard en segundos** sin que tengas que hacer nada manual.
- **Disparo manual**: También podés ir a la pestaña **Actions** en tu GitHub y presionar **Run workflow** para actualizarlo al instante.

---

## 📁 Estructura del Proyecto
```
scrapper-hastag/
├── CONTEXT.md                    # Bitácora técnica y memoria viva del proyecto
├── README.md                     # Documentación de uso
├── requirements.txt              # Dependencias (httpx, beautifulsoup4, rich, pandas)
├── main.py                       # CLI principal y pipeline
├── analytics.py                  # Motor de analítica y cálculo de KPIs
├── reporter.py                   # Generador de Dashboard interactivo HTML
├── scrapers/                     # Módulos de extracción por plataforma
│   ├── base.py                   # Modelo unificado PostData y clase BaseScraper
│   ├── cgera_campaign.py         # Extractor web oficial CGERA
│   ├── instagram_scraper.py      # Extractor de Instagram
│   ├── tiktok_scraper.py         # Extractor de TikTok
│   ├── x_scraper.py              # Extractor de X (Twitter)
│   └── facebook_scraper.py       # Extractor de Facebook
├── data/
│   └── processed/                # Datasets consolidados en JSON y CSV
└── reports/
    └── dashboard_queremostrabajar.html # Dashboard web generado
```

