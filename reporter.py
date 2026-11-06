"""
HTML Dashboard and Report Generator for #queremostrabajar Social Media Analytics.
Produces a modern, standalone, interactive dashboard using Tailwind CSS and Chart.js.
"""
import json
from typing import Dict, Any
from pathlib import Path


def generate_html_dashboard(report_data: Dict[str, Any], output_path: str = "reports/dashboard_queremostrabajar.html") -> str:
    kpis = report_data["kpis"]
    platforms = report_data["platforms"]
    top_hashtags = report_data["top_hashtags"]
    top_posts = report_data["top_posts"]
    posts = report_data["posts"]

    # Prepare data for Chart.js
    platform_names = [p["platform"].upper() for p in platforms]
    platform_posts = [p["posts_count"] for p in platforms]
    platform_eng = [p["total_engagement"] for p in platforms]
    platform_views = [p["views"] for p in platforms]

    tag_labels = [t["tag"] for t in top_hashtags[:8]]
    tag_counts = [t["count"] for t in top_hashtags[:8]]

    posts_json = json.dumps(posts, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-950 text-slate-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campaña #queremostrabajar | Dashboard Analítico CGERA</title>
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
    </style>
</head>
<body class="min-h-full flex flex-col antialiased selection:bg-cyan-500 selection:text-white">

    <!-- Top Banner -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div class="flex items-center space-x-3">
                <span class="inline-flex items-center justify-center p-2 bg-gradient-to-tr from-cyan-600 to-blue-600 rounded-xl shadow-lg shadow-cyan-500/20 text-white font-black text-xl">
                    🇦🇷
                </span>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-xl font-bold tracking-tight text-white">#queremostrabajar</h1>
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-medium">
                            CGERA 5N
                        </span>
                    </div>
                    <p class="text-xs text-slate-400">
                        Campaña Nacional: "Mostrá tu producto Argentino, Defendé tu trabajo" &bull; 
                        <a href="https://cgera.net.ar/mostra-tu-producto/" target="_blank" class="text-cyan-400 hover:underline">cgera.net.ar/mostra-tu-producto</a>
                    </p>
                </div>
            </div>

            <!-- Header Quick Stats -->
            <div class="flex items-center gap-3">
                <span class="text-xs text-slate-400 hidden sm:inline">Monitoreo: <strong>Instagram, TikTok, X, Facebook</strong></span>
                <button onclick="window.print()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 transition">
                    🖨️ Exportar PDF
                </button>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        <!-- Executive Highlights Alert -->
        <div class="bg-gradient-to-r from-blue-950/60 via-slate-900 to-slate-900 border border-blue-800/60 rounded-2xl p-6 shadow-xl relative overflow-hidden">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="space-y-1">
                    <span class="text-xs uppercase tracking-wider font-bold text-cyan-400">Objetivo y Convocatoria Federal</span>
                    <h2 class="text-lg font-semibold text-slate-100">
                        Movilización en Fábricas, Talleres y Comercios — Jueves 5 de Noviembre 12:00 HS
                    </h2>
                    <p class="text-sm text-slate-300 max-w-3xl">
                        Convocatoria impulsada por CGERA (Confederación General Empresaria de la R.A.) para que trabajadores y empresarios salgan a la puerta de sus establecimientos con su producción, alertando sobre la situación de la industria y defendiendo el empleo formal.
                    </p>
                </div>
                <div class="flex md:flex-col items-center md:items-end justify-between border-t md:border-t-0 md:border-l border-slate-800 pt-3 md:pt-0 md:pl-6 text-right">
                    <span class="text-xs text-slate-400">Adhesiones Registradas</span>
                    <span class="text-2xl font-black text-cyan-400">+2.280 visitas</span>
                    <span class="text-xs text-slate-500">+296 kits descargados</span>
                </div>
            </div>
        </div>

        <!-- Metric KPI Cards -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 font-medium">Publicaciones</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_posts']}</p>
                <p class="text-[11px] text-cyan-400 mt-1">4 Redes + Oficial</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 font-medium">Interacciones Totales</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_engagement']:,}</p>
                <p class="text-[11px] text-emerald-400 mt-1">Likes + Comms + Shares</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 font-medium">Reproducciones</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_views']:,}</p>
                <p class="text-[11px] text-indigo-400 mt-1">Alcance Estimado</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 font-medium">Compartidos / RTs</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['total_shares']:,}</p>
                <p class="text-[11px] text-amber-400 mt-1">Efecto multiplicador</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 font-medium">Empresas / Pymes</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['unique_authors']}</p>
                <p class="text-[11px] text-purple-400 mt-1">Voces únicas activas</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4">
                <p class="text-xs text-slate-400 font-medium">Prom. Interacciones</p>
                <p class="text-2xl font-extrabold text-white mt-1">{kpis['avg_engagement_per_post']}</p>
                <p class="text-[11px] text-rose-400 mt-1">Por publicación</p>
            </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Platform Breakdown Donut & Table -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                <h3 class="text-sm font-semibold text-slate-200 mb-4 flex items-center justify-between">
                    <span>Distribución y Participación por Plataforma</span>
                    <span class="text-xs text-slate-500 font-normal">Volumen & Porcentaje</span>
                </h3>
                <div class="h-64 flex items-center justify-center">
                    <canvas id="platformDonutChart"></canvas>
                </div>
                <div class="mt-4 pt-4 border-t border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
                    {"".join([f'''
                    <div class="p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                        <span class="text-xs font-bold uppercase text-slate-300">{p["platform"]}</span>
                        <p class="text-base font-extrabold text-white mt-0.5">{p["posts_count"]}</p>
                        <span class="text-[10px] text-slate-400">{p["share_pct"]}% del total</span>
                    </div>
                    ''' for p in platforms])}
                </div>
            </div>

            <!-- Platform Engagement Bar Chart -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between">
                <h3 class="text-sm font-semibold text-slate-200 mb-4 flex items-center justify-between">
                    <span>Nivel de Engagement (Likes, Shares, Comentarios)</span>
                    <span class="text-xs text-slate-500 font-normal">Impacto total por red</span>
                </h3>
                <div class="h-64">
                    <canvas id="engagementBarChart"></canvas>
                </div>
                <div class="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                    <span>Red más viral: <strong>TikTok</strong> (Videos testimoniales verticales 9:16)</span>
                    <span>Red más institucional: <strong>X & Facebook</strong></span>
                </div>
            </div>
        </div>

        <!-- Top Viral Convocatorias & Testimonios -->
        <section class="space-y-4">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-base font-bold text-white">🔥 Convocatorias y Testimonios Destacados</h3>
                    <p class="text-xs text-slate-400">Publicaciones con mayor nivel de viralidad e impacto de la jornada</p>
                </div>
                <span class="text-xs text-slate-500">Top {len(top_posts[:4])}</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {"".join([f'''
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between hover:border-slate-700 transition">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-[11px] font-bold uppercase px-2 py-0.5 rounded badge-{p["platform"]}">
                                {p["platform"]}
                            </span>
                            <span class="text-xs text-slate-400">{p.get("location") or "Argentina"}</span>
                        </div>
                        <h4 class="text-sm font-semibold text-slate-100">{p["author_name"]}</h4>
                        <p class="text-xs text-slate-400 mb-3">@{p["author_username"]}</p>
                        <p class="text-xs text-slate-300 line-clamp-4 leading-relaxed mb-4">
                            "{p["text_content"]}"
                        </p>
                    </div>
                    <div class="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                        <div class="flex items-center space-x-2 text-slate-400">
                            <span>❤️ {p["likes"]:,}</span>
                            <span>🔄 {p["shares"]:,}</span>
                        </div>
                        <a href="{p["url"]}" target="_blank" class="text-cyan-400 hover:text-cyan-300 font-medium">Ver post &rarr;</a>
                    </div>
                </div>
                ''' for p in top_posts[:4]])}
            </div>
        </section>

        <!-- Interactive Searchable Data Table -->
        <section class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
            <div class="p-5 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h3 class="text-base font-bold text-white">Explorador Integral de Publicaciones</h3>
                    <p class="text-xs text-slate-400">Listado completo unificado de convocatorias y adhesiones en redes</p>
                </div>
                <div class="flex flex-wrap items-center gap-2">
                    <input type="text" id="searchInput" onkeyup="filterPosts()" placeholder="Buscar por pyme, ciudad o texto..."
                           class="px-3 py-1.5 text-xs bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500 w-64">
                    <select id="platformFilter" onchange="filterPosts()"
                            class="px-3 py-1.5 text-xs bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500">
                        <option value="all">Todas las Redes</option>
                        <option value="instagram">Instagram</option>
                        <option value="tiktok">TikTok</option>
                        <option value="x">X (Twitter)</option>
                        <option value="facebook">Facebook</option>
                        <option value="cgera">CGERA Oficial</option>
                    </select>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-300" id="postsTable">
                    <thead class="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                        <tr>
                            <th class="px-4 py-3">Red</th>
                            <th class="px-4 py-3">Autor / Pyme</th>
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
        <p>Campaña "Mostrá tu producto Argentino, Defendé tu trabajo" &bull; Monitoreo social hashtag <strong>#queremostrabajar</strong></p>
        <p class="mt-1">Generado automáticamente por el motor de analítica y scraping de CGERA 5N.</p>
    </footer>

    <!-- Chart.js Scripts and Interactive Table Filter -->
    <script>
        const allPosts = {posts_json};

        function renderTable(posts) {{
            const tbody = document.getElementById("postsTableBody");
            if (posts.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="8" class="text-center py-8 text-slate-500">No se encontraron publicaciones con esos criterios.</td></tr>';
                return;
            }}

            tbody.innerHTML = posts.map(p => `
                <tr class="hover:bg-slate-800/40 transition">
                    <td class="px-4 py-3">
                        <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded badge-${{p.platform}}">
                            ${{p.platform}}
                        </span>
                    </td>
                    <td class="px-4 py-3">
                        <div class="font-medium text-white">${{p.author_name}}</div>
                        <div class="text-[11px] text-slate-500">@${{p.author_username}}</div>
                    </td>
                    <td class="px-4 py-3 text-slate-400">${{p.location || 'Argentina'}}</td>
                    <td class="px-4 py-3 max-w-md">
                        <div class="truncate text-slate-300" title="${{p.text_content.replace(/"/g, '&quot;')}}">
                            ${{p.text_content}}
                        </div>
                    </td>
                    <td class="px-4 py-3 text-right font-semibold text-slate-200">${{Number(p.likes).toLocaleString()}}</td>
                    <td class="px-4 py-3 text-right font-semibold text-slate-200">${{Number(p.shares).toLocaleString()}}</td>
                    <td class="px-4 py-3 text-right font-semibold text-slate-400">${{p.views ? Number(p.views).toLocaleString() : '-'}}</td>
                    <td class="px-4 py-3 text-center">
                        <a href="${{p.url}}" target="_blank" class="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded text-[11px] transition">
                            Abrir ↗
                        </a>
                    </td>
                </tr>
            `).join('');
        }}

        function filterPosts() {{
            const search = document.getElementById("searchInput").value.toLowerCase();
            const platform = document.getElementById("platformFilter").value;

            const filtered = allPosts.filter(p => {{
                const matchesSearch = p.author_name.toLowerCase().includes(search) ||
                                      p.author_username.toLowerCase().includes(search) ||
                                      (p.location && p.location.toLowerCase().includes(search)) ||
                                      p.text_content.toLowerCase().includes(search);
                const matchesPlatform = (platform === "all" || p.platform === platform);
                return matchesSearch && matchesPlatform;
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

        // Engagement Bar Chart
        new Chart(document.getElementById('engagementBarChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(platform_names)},
                datasets: [{{
                    label: 'Interacciones Totales',
                    data: {json.dumps(platform_eng)},
                    backgroundColor: '#0284c7',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
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

