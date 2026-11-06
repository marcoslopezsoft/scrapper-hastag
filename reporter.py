"""
HTML Dashboard and Report Generator for #queremostrabajar Social Media Analytics.
Produces an executive, standalone, interactive dashboard using Tailwind CSS and Chart.js.
"""
import json
from typing import Dict, Any
from pathlib import Path


def generate_html_dashboard(report_data: Dict[str, Any], output_path: str = "reports/dashboard_queremostrabajar.html") -> str:
    kpis = report_data["kpis"]
    platforms = report_data["platforms"]
    sectors = report_data.get("sectors", [])
    top_hashtags = report_data["top_hashtags"]
    top_posts = report_data["top_posts"]
    posts = report_data["posts"]

    # Prepare data for Chart.js
    platform_names = [p["platform"].upper() for p in platforms]
    platform_posts = [p["posts_count"] for p in platforms]
    platform_eng = [p["total_engagement"] for p in platforms]
    platform_views = [p["views"] for p in platforms]

    sector_names = [s["sector"] for s in sectors[:8]]
    sector_eng = [s["total_engagement"] for s in sectors[:8]]
    sector_posts = [s["posts_count"] for s in sectors[:8]]

    tag_labels = [t["tag"] for t in top_hashtags[:8]]
    tag_counts = [t["count"] for t in top_hashtags[:8]]

    posts_json = json.dumps(posts, ensure_ascii=False)

    # Unique sectors for filter dropdown
    unique_sectors = sorted(list(set(p.get("sector", "Industria Nacional") for p in posts)))
    sector_options_html = "".join([f'<option value="{s}">{s}</option>' for s in unique_sectors])

    html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-950 text-slate-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campaña #queremostrabajar | Dashboard Analítico Federal CGERA & CSIRA</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
        .badge-x {{ background-color: #0f172a; border: 1px solid #334155; color: #f8fafc; }}
        .badge-tiktok {{ background-color: #000000; border: 1px solid #ff0050; color: #00f2fe; }}
        .badge-instagram {{ background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; }}
        .badge-facebook {{ background-color: #1877f2; color: white; }}
        .badge-cgera {{ background-color: #0284c7; color: white; }}
        .badge-sector {{ background-color: #1e293b; border: 1px solid #334155; color: #94a3b8; }}
        @media print {{
            header, .no-print {{ display: none !important; }}
            body {{ background: white !important; color: black !important; }}
        }}
    </style>
</head>
<body class="min-h-full flex flex-col antialiased selection:bg-cyan-500 selection:text-white">

    <!-- Top Navigation Header -->
    <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div class="flex items-center space-x-3">
                <span class="inline-flex items-center justify-center p-2.5 bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 rounded-xl shadow-lg shadow-cyan-500/20 text-white font-black text-xl">
                    🇦🇷
                </span>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-xl font-bold tracking-tight text-white">#queremostrabajar</h1>
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-medium">
                            Jornada Federal 5N
                        </span>
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-950 text-indigo-400 border border-indigo-800 font-medium hidden sm:inline">
                            CGERA + CSIRA
                        </span>
                    </div>
                    <p class="text-xs text-slate-400">
                        Campaña Nacional: "Mostrá tu producto Argentino, Defendé tu trabajo" &bull; 
                        <a href="https://cgera.net.ar/mostra-tu-producto/" target="_blank" class="text-cyan-400 hover:underline">cgera.net.ar/mostra-tu-producto</a>
                    </p>
                </div>
            </div>

            <!-- Export Buttons -->
            <div class="flex flex-wrap items-center gap-2 no-print">
                <a href="../data/processed/queremostrabajar_analitica.xlsx" download
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-800 rounded-lg text-xs font-semibold shadow-sm transition">
                    📗 Descargar Excel (.xlsx)
                </a>
                <a href="../data/processed/queremostrabajar_posts.csv" download
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold transition">
                    📄 CSV
                </a>
                <a href="../data/processed/queremostrabajar_posts.json" download
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold transition">
                    📦 JSON
                </a>
                <button onclick="window.print()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 transition">
                    🖨️ PDF
                </button>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        <!-- Executive Highlights Alert -->
        <div class="bg-gradient-to-r from-blue-950/70 via-slate-900 to-indigo-950/60 border border-blue-800/60 rounded-2xl p-6 shadow-xl relative overflow-hidden">
            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                <div class="space-y-1.5 max-w-3xl">
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] uppercase tracking-wider font-extrabold text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800/60">
                            Convocatoria Nacional de Fábricas, Talleres y Comercios
                        </span>
                        <span class="text-xs text-slate-400">Jueves 5 de Noviembre &bull; 12:00 HS</span>
                    </div>
                    <h2 class="text-xl font-bold text-white tracking-tight">
                        "Mostrá tu producto argentino, defendé tu trabajo"
                    </h2>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Iniciativa unitaria de la <strong>CGERA</strong> (presidida por Marcelo Fernández) y la <strong>CSIRA</strong> (34 gremios industriales: UOM, SMATA, UTICRA calzado, UOYEP plásticos, AOT textiles, ASIMRA, Gráficos, Químicos, Madera, Vidrio) con movilización pacífica en las puertas de los establecimientos de todo el país mostrando lo que producimos y alertando sobre la caída de la actividad económica y el consumo.
                    </p>
                </div>
                <div class="grid grid-cols-2 gap-4 lg:border-l lg:border-slate-800 lg:pl-6 text-right">
                    <div class="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80">
                        <span class="text-[11px] text-slate-400 block font-medium">Adhesiones Registradas</span>
                        <span class="text-2xl font-black text-cyan-400">+2.339</span>
                        <span class="text-[10px] text-slate-500 block">visitas en el portal</span>
                    </div>
                    <div class="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80">
                        <span class="text-[11px] text-slate-400 block font-medium">Kit Visual Descargado</span>
                        <span class="text-2xl font-black text-emerald-400">+304</span>
                        <span class="text-[10px] text-slate-500 block">piezas gráficas</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Metric KPI Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Publicaciones</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_posts']}</p>
                <p class="text-[11px] text-cyan-400 mt-1">4 Redes + Oficial</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Interacciones Totales</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_engagement']:,}</p>
                <p class="text-[11px] text-emerald-400 mt-1">Likes + Comms + RTs</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Reproducciones / Vistas</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_views']:,}</p>
                <p class="text-[11px] text-indigo-400 mt-1">Alcance Estimado</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Compartidos / RTs</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_shares']:,}</p>
                <p class="text-[11px] text-amber-400 mt-1">Efecto multiplicador</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Empresas & Gremios</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['unique_authors']}</p>
                <p class="text-[11px] text-purple-400 mt-1">Voces únicas activas</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Prom. Interacciones</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['avg_engagement_per_post']}</p>
                <p class="text-[11px] text-rose-400 mt-1">Por publicación</p>
            </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Platform Breakdown Donut & Share Cards -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-semibold text-slate-200">Distribución de Publicaciones por Red</h3>
                    <span class="text-xs text-slate-500">Volumen & Participación %</span>
                </div>
                <div class="h-64 flex items-center justify-center">
                    <canvas id="platformDonutChart"></canvas>
                </div>
                <div class="mt-4 pt-4 border-t border-slate-800 grid grid-cols-2 sm:grid-cols-5 gap-2 text-center">
                    {"".join([f'''
                    <div class="p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                        <span class="text-[10px] font-bold uppercase text-slate-300">{p["platform"]}</span>
                        <p class="text-base font-extrabold text-white mt-0.5">{p["posts_count"]}</p>
                        <span class="text-[10px] text-slate-400">{p["share_pct"]}%</span>
                    </div>
                    ''' for p in platforms])}
                </div>
            </div>

            <!-- Sector Industrial Breakdown Bar Chart -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between shadow-sm">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-semibold text-slate-200">Interacciones por Sector Productivo</h3>
                    <span class="text-xs text-slate-500">Impacto total por rubro</span>
                </div>
                <div class="h-64">
                    <canvas id="sectorBarChart"></canvas>
                </div>
                <div class="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                    <span>Sectores clave: <strong>Tecnología, Metalúrgica, Calzado, Textil, Gremial</strong></span>
                    <span>Cobertura: <strong>Federal</strong></span>
                </div>
            </div>
        </div>

        <!-- Top Viral Convocatorias & Videos Destacados -->
        <section class="space-y-4">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-base font-bold text-white flex items-center gap-2">
                        <span>🔥 Convocatorias y Testimonios Destacados</span>
                    </h3>
                    <p class="text-xs text-slate-400">Publicaciones y videos con mayor tracción e impacto social</p>
                </div>
                <span class="text-xs text-slate-500 font-medium">Top {len(top_posts[:4])}</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {"".join([f'''
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between hover:border-slate-700 transition shadow-sm">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded badge-{p["platform"]}">
                                {p["platform"]}
                            </span>
                            <span class="text-[11px] text-slate-400 font-medium truncate max-w-[120px]">{p.get("location") or "Argentina"}</span>
                        </div>
                        <div class="mb-2">
                            <span class="text-[10px] font-medium px-2 py-0.5 rounded badge-sector">
                                {p.get("sector", "Industria Nacional")}
                            </span>
                        </div>
                        <h4 class="text-sm font-semibold text-slate-100 line-clamp-1">{p["author_name"]}</h4>
                        <p class="text-xs text-slate-400 mb-2">@{p["author_username"]}</p>
                        <p class="text-xs text-slate-300 line-clamp-3 leading-relaxed mb-4">
                            "{p["text_content"]}"
                        </p>
                    </div>
                    <div class="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                        <div class="flex items-center space-x-2 text-slate-400">
                            <span>❤️ {p["likes"]:,}</span>
                            <span>🔄 {p["shares"]:,}</span>
                            {f'<span>👁️ {p["views"]:,}</span>' if p.get("views") else ''}
                        </div>
                        <a href="{p["url"]}" target="_blank" class="text-cyan-400 hover:text-cyan-300 font-semibold inline-flex items-center gap-1">
                            Ver ↗
                        </a>
                    </div>
                </div>
                ''' for p in top_posts[:4]])}
            </div>
        </section>

        <!-- Interactive Searchable Data Table with Multi-Filter -->
        <section class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
            <div class="p-5 border-b border-slate-800 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                <div>
                    <h3 class="text-base font-bold text-white flex items-center gap-2">
                        <span>Relevamiento Federal Completo de Publicaciones</span>
                        <span id="resultsCounter" class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
                            {len(posts)} publicaciones
                        </span>
                    </h3>
                    <p class="text-xs text-slate-400">Filtrá en tiempo real por empresa, usuario, rubro o localidad</p>
                </div>
                <div class="flex flex-wrap items-center gap-2">
                    <input type="text" id="searchInput" onkeyup="filterPosts()" placeholder="Buscar por empresa, @usuario, localidad o texto..."
                           class="px-3 py-1.5 text-xs bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 w-72">
                    <select id="platformFilter" onchange="filterPosts()"
                            class="px-3 py-1.5 text-xs bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500">
                        <option value="all">Todas las Redes</option>
                        <option value="instagram">Instagram (Reels & Feed)</option>
                        <option value="tiktok">TikTok (Videos)</option>
                        <option value="x">X (Twitter)</option>
                        <option value="facebook">Facebook</option>
                        <option value="cgera">CGERA Oficial</option>
                    </select>
                    <select id="sectorFilter" onchange="filterPosts()"
                            class="px-3 py-1.5 text-xs bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500">
                        <option value="all">Todos los Sectores</option>
                        {sector_options_html}
                    </select>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-300" id="postsTable">
                    <thead class="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                        <tr>
                            <th class="px-4 py-3">Red</th>
                            <th class="px-4 py-3">Empresa / Autor</th>
                            <th class="px-4 py-3">Sector / Rubro</th>
                            <th class="px-4 py-3">Ubicación</th>
                            <th class="px-4 py-3">Mensaje / Convocatoria</th>
                            <th class="px-4 py-3 text-right">Likes</th>
                            <th class="px-4 py-3 text-right">Shares</th>
                            <th class="px-4 py-3 text-right">Vistas</th>
                            <th class="px-4 py-3 text-center">Acción</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800/60" id="postsTableBody">
                        <!-- Populated by JavaScript -->
                    </tbody>
                </table>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-950 py-6 mt-12 text-center text-xs text-slate-500">
        <p>Campaña Nacional: "Mostrá tu producto Argentino, Defendé tu trabajo" &bull; Convocatoria CGERA & CSIRA &bull; <strong>#queremostrabajar</strong></p>
        <p class="mt-1">Monitoreo multirred automatizado con ingesta de enlaces directos (yt-dlp) y procesamiento analítico.</p>
    </footer>

    <!-- Chart.js Scripts and Interactive Table Filter -->
    <script>
        const allPosts = {posts_json};

        function renderTable(posts) {{
            const tbody = document.getElementById("postsTableBody");
            const counter = document.getElementById("resultsCounter");
            if (counter) counter.innerText = `${{posts.length}} publicaciones`;

            if (posts.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="9" class="text-center py-10 text-slate-500">No se encontraron publicaciones con esos criterios de búsqueda.</td></tr>';
                return;
            }}

            tbody.innerHTML = posts.map(p => `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="px-4 py-3">
                        <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded badge-${{p.platform}}">
                            ${{p.platform}}
                        </span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                        <div class="font-semibold text-white">${{p.author_name}}</div>
                        <div class="text-[11px] text-slate-500">@${{p.author_username}}</div>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                        <span class="text-[10px] px-2 py-0.5 rounded badge-sector">${{p.sector || 'Industria Nacional'}}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-slate-400">${{p.location || 'Argentina'}}</td>
                    <td class="px-4 py-3 max-w-sm">
                        <div class="truncate text-slate-300" title="${{p.text_content.replace(/"/g, '&quot;')}}">
                            ${{p.text_content}}
                        </div>
                    </td>
                    <td class="px-4 py-3 text-right font-semibold text-slate-200">${{Number(p.likes).toLocaleString()}}</td>
                    <td class="px-4 py-3 text-right font-semibold text-slate-200">${{Number(p.shares).toLocaleString()}}</td>
                    <td class="px-4 py-3 text-right font-semibold text-slate-400">${{p.views ? Number(p.views).toLocaleString() : '-'}}</td>
                    <td class="px-4 py-3 text-center whitespace-nowrap">
                        <a href="${{p.url}}" target="_blank" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-400 font-semibold rounded text-[11px] transition inline-flex items-center gap-1">
                            Abrir ↗
                        </a>
                    </td>
                </tr>
            `).join('');
        }}

        function filterPosts() {{
            const search = document.getElementById("searchInput").value.toLowerCase();
            const platform = document.getElementById("platformFilter").value;
            const sector = document.getElementById("sectorFilter").value;

            const filtered = allPosts.filter(p => {{
                const matchesSearch = p.author_name.toLowerCase().includes(search) ||
                                      p.author_username.toLowerCase().includes(search) ||
                                      (p.location && p.location.toLowerCase().includes(search)) ||
                                      (p.sector && p.sector.toLowerCase().includes(search)) ||
                                      p.text_content.toLowerCase().includes(search);
                const matchesPlatform = (platform === "all" || p.platform === platform);
                const matchesSector = (sector === "all" || p.sector === sector);
                return matchesSearch && matchesPlatform && matchesSector;
            }});

            renderTable(filtered);
        }}

        // Initialize table
        renderTable(allPosts);

        // Platform Donut Chart
        new Chart(document.getElementById('platformDonutChart'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(platform_names)},
                datasets: [{{
                    data: {json.dumps(platform_posts)},
                    backgroundColor: ['#dc2743', '#00f2fe', '#0ea5e9', '#1877f2', '#6366f1'],
                    borderWidth: 2,
                    borderColor: '#0f172a'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }}
                }}
            }}
        }});

        // Sector Bar Chart
        new Chart(document.getElementById('sectorBarChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(sector_names)},
                datasets: [{{
                    label: 'Interacciones Totales',
                    data: {json.dumps(sector_eng)},
                    backgroundColor: '#0284c7',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8', maxRotation: 45, minRotation: 20 }}, grid: {{ display: false }} }},
                    y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#1e293b' }} }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path
