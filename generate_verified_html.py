"""
Generates the standalone HTML Dashboard based 100% on the verified Social Listening & TweetBinder Report.
Outputs to reports/dashboard_queremostrabajar.html and index.html.
"""
import json
from pathlib import Path

def generate_html():
    with open("data/social_listening.json", "r", encoding="utf-8") as f:
        sl = json.load(f)

    sk = sl.get("summary_kpis", {})
    emotions = sl.get("emotions", {}).get("breakdown", [])
    media_types = sl.get("media_types", [])
    sites = sl.get("top_sites", [])
    influencers = sl.get("top_influencers", [])
    hashtags = sl.get("trending_hashtags", [])
    topics = sl.get("trending_topics", [])
    emojis = sl.get("top_emojis", [])

    html_content = f"""<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-950 text-slate-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#queremostrabajar | Monitor Analítico Oficial CGERA & CSIRA</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
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
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-semibold">
                            Auditoría Oficial Social Listening
                        </span>
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-indigo-950 text-indigo-400 border border-indigo-800 font-semibold hidden sm:inline">
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
            <div class="flex flex-wrap items-center gap-2">
                <a href="data/processed/queremostrabajar_analitica.xlsx" download
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-800 rounded-lg text-xs font-semibold shadow-sm transition">
                    📗 Descargar Excel (.xlsx)
                </a>
                <a href="data/social_listening.json" download
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold transition">
                    📦 JSON Verificado
                </a>
                <button onclick="window.print()"
                   class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-cyan-950 hover:bg-cyan-900 text-cyan-300 border border-cyan-800 rounded-lg text-xs font-semibold transition">
                    🖨️ Imprimir / PDF
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 space-y-8 w-full">

        <!-- Executive Banner -->
        <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-sky-950 via-slate-900 to-indigo-950 border border-slate-800 p-6 sm:p-8 shadow-xl">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
                <div class="lg:col-span-2 space-y-2">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-900/40 border border-cyan-700/50 text-cyan-300 text-xs font-semibold">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                        Período Auditado: 9 de octubre al 8 de noviembre · 31 días (Últimos 30 días)
                    </div>
                    <h2 class="text-2xl font-bold text-white tracking-tight">
                        "Mostrá tu producto argentino, defendé tu trabajo"
                    </h2>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Iniciativa federal de la <strong>CGERA</strong> (Marcelo Fernández) y la <strong>CSIRA</strong> (34 gremios industriales) convocando a industrias, fábricas, talleres y pymes a visibilizar la producción nacional en las puertas de cada establecimiento.
                    </p>
                </div>
                <div class="grid grid-cols-2 gap-3 text-right">
                    <div class="p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                        <span class="text-[11px] text-slate-400 block font-medium">Pico de Menciones</span>
                        <span class="text-2xl font-black text-cyan-400">230</span>
                        <span class="text-[10px] text-slate-500 block">Jueves 5 Nov (18.1× media)</span>
                    </div>
                    <div class="p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                        <span class="text-[11px] text-slate-400 block font-medium">Alcance Global (Reach)</span>
                        <span class="text-2xl font-black text-emerald-400">9,5M</span>
                        <span class="text-[10px] text-slate-500 block">personas expuestas</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Metric KPI Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Menciones Totales</p>
                <p class="text-3xl font-extrabold text-white mt-1">{sk.get('mentions', 356)}</p>
                <p class="text-[11px] text-cyan-400 mt-1">Pico 5N: 230 posts</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Alcance Global (Reach)</p>
                <p class="text-3xl font-extrabold text-white mt-1">{sk.get('reach_label', '9,5M')}</p>
                <p class="text-[11px] text-emerald-400 mt-1">8.9M diario</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Interacciones Totales</p>
                <p class="text-3xl font-extrabold text-white mt-1">{sk.get('interactions_label', '101.5K')}</p>
                <p class="text-[11px] text-indigo-400 mt-1">Likes + RTs + Comms</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Sentimiento Expresado</p>
                <p class="text-3xl font-extrabold text-emerald-400 mt-1">52%</p>
                <p class="text-[11px] text-slate-400 mt-1">Positivo vs 48% Reclamo (1.1:1)</p>
            </div>
            <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm">
                <p class="text-xs text-slate-400 font-medium">Emoción Dominante</p>
                <p class="text-3xl font-extrabold text-amber-400 mt-1">48%</p>
                <p class="text-[11px] text-slate-400 mt-1">Alegría (91% con Enojo/Ira)</p>
            </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Sentiment Donut Chart -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-semibold text-slate-200">Desglose de Sentimiento</h3>
                    <span class="text-xs text-slate-400">Total: 356 menciones</span>
                </div>
                <div class="h-64 flex items-center justify-center">
                    <canvas id="sentimentChart"></canvas>
                </div>
                <div class="mt-4 pt-4 border-t border-slate-800 grid grid-cols-3 gap-2 text-center text-xs">
                    <div class="p-2 rounded-lg bg-emerald-950/40 border border-emerald-900">
                        <span class="text-emerald-400 font-bold">Positivo</span>
                        <p class="text-base font-extrabold text-white mt-0.5">{sk.get('positive_mentions', 100)}</p>
                        <span class="text-slate-400">28% total</span>
                    </div>
                    <div class="p-2 rounded-lg bg-rose-950/40 border border-rose-900">
                        <span class="text-rose-400 font-bold">Negativo / Reclamo</span>
                        <p class="text-base font-extrabold text-white mt-0.5">{sk.get('negative_mentions', 93)}</p>
                        <span class="text-slate-400">26% total</span>
                    </div>
                    <div class="p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                        <span class="text-slate-300 font-bold">Neutral</span>
                        <p class="text-base font-extrabold text-white mt-0.5">{sk.get('neutral_mentions', 163)}</p>
                        <span class="text-slate-400">46% total</span>
                    </div>
                </div>
            </div>

            <!-- Media Types Bar Chart -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-semibold text-slate-200">Menciones por Tipo de Medio</h3>
                    <span class="text-xs text-slate-400">Canales de difusión</span>
                </div>
                <div class="h-64">
                    <canvas id="mediaChart"></canvas>
                </div>
                <div class="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                    <span>Video (TikTok/Reels): <strong>52% positivo</strong></span>
                    <span>Web: <strong>44% crítico económico</strong></span>
                </div>
            </div>
        </div>

        <!-- Portales Web & Influencers Tables -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Portales Web -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-bold text-white">🌐 Sitios Web Líderes por Visitas Mensuales</h3>
                    <span class="text-xs text-cyan-400">Mayor alcance</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-xs text-left">
                        <thead class="text-slate-400 uppercase bg-slate-950/60 border-b border-slate-800">
                            <tr>
                                <th class="py-2.5 px-3">Portal Web</th>
                                <th class="py-2.5 px-3 text-right">Visitas / Mes</th>
                                <th class="py-2.5 px-3 text-center">Menciones</th>
                                <th class="py-2.5 px-3">Rol</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800 text-slate-200">
                            {"".join([f'''
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2 px-3 font-semibold text-white">{s["site"]}</td>
                                <td class="py-2 px-3 text-right text-emerald-400 font-bold">{s["monthly_visits"]}</td>
                                <td class="py-2 px-3 text-center">{s["mentions"]}</td>
                                <td class="py-2 px-3 text-slate-400">{s["role"]}</td>
                            </tr>
                            ''' for s in sites])}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Top Influencers -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm font-bold text-white">📢 Top Influencers & Cuota de Voz (% Voice Share)</h3>
                    <span class="text-xs text-cyan-400">Líderes de opinión</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-xs text-left">
                        <thead class="text-slate-400 uppercase bg-slate-950/60 border-b border-slate-800">
                            <tr>
                                <th class="py-2.5 px-3">Referente / Medio</th>
                                <th class="py-2.5 px-3">Usuario</th>
                                <th class="py-2.5 px-3 text-right">% Cuota de Voz</th>
                                <th class="py-2.5 px-3 text-center">Menciones</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800 text-slate-200">
                            {"".join([f'''
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-2 px-3 font-semibold text-white">{inf["name"]}</td>
                                <td class="py-2 px-3 text-cyan-400 font-mono">{inf["handle"]}</td>
                                <td class="py-2 px-3 text-right text-amber-400 font-bold">{inf["voice_share_pct"]}%</td>
                                <td class="py-2 px-3 text-center">{inf["mentions"]}</td>
                            </tr>
                            ''' for inf in influencers])}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Top Trending Hashtags & Topics -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Hashtags -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
                <h3 class="text-sm font-bold text-white">🏷️ Top Trending Hashtags (Primeros 15 de 40)</h3>
                <div class="overflow-x-auto max-h-96">
                    <table class="w-full text-xs text-left">
                        <thead class="text-slate-400 uppercase bg-slate-950/60 border-b border-slate-800 sticky top-0">
                            <tr>
                                <th class="py-2 px-3 text-center">#</th>
                                <th class="py-2 px-3">Hashtag</th>
                                <th class="py-2 px-3 text-right">Usos</th>
                                <th class="py-2 px-3">Tono</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800 text-slate-200">
                            {"".join([f'''
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-1.5 px-3 text-center text-slate-500 font-mono">{h["rank"]}</td>
                                <td class="py-1.5 px-3 font-bold text-cyan-300 font-mono">{h["hashtag"]}</td>
                                <td class="py-1.5 px-3 text-right font-bold text-white">{h["count"]}</td>
                                <td class="py-1.5 px-3 text-slate-400">{h["sentiment"]}</td>
                            </tr>
                            ''' for h in hashtags[:15]])}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Topics -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
                <h3 class="text-sm font-bold text-white">💬 Frases y Tópicos más Discutidos (Primeros 15 de 35)</h3>
                <div class="overflow-x-auto max-h-96">
                    <table class="w-full text-xs text-left">
                        <thead class="text-slate-400 uppercase bg-slate-950/60 border-b border-slate-800 sticky top-0">
                            <tr>
                                <th class="py-2 px-3 text-center">#</th>
                                <th class="py-2 px-3">Frase Clave</th>
                                <th class="py-2 px-3 text-right">Frecuencia</th>
                                <th class="py-2 px-3">Enfoque</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800 text-slate-200">
                            {"".join([f'''
                            <tr class="hover:bg-slate-800/40">
                                <td class="py-1.5 px-3 text-center text-slate-500 font-mono">{t["rank"]}</td>
                                <td class="py-1.5 px-3 font-semibold text-white">{t["topic"]}</td>
                                <td class="py-1.5 px-3 text-right font-bold text-emerald-400">{t["count"]}</td>
                                <td class="py-1.5 px-3 text-slate-400">{t["sentiment"]}</td>
                            </tr>
                            ''' for t in topics[:15]])}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-900/60 py-6 mt-12 text-center text-xs text-slate-400">
        <p>Campaña #queremostrabajar &bull; Confederación General Empresaria de la República Argentina (CGERA) &bull; CSIRA</p>
        <p class="mt-1 text-slate-500">Monitor Oficial 100% Basado en Datos Verificados de Social Listening & Auditoría de Redes.</p>
    </footer>

    <script>
        // Sentiment Chart
        const ctxSent = document.getElementById('sentimentChart').getContext('2d');
        new Chart(ctxSent, {{
            type: 'doughnut',
            data: {{
                labels: ['Neutral', 'Positivo', 'Negativo / Reclamo'],
                datasets: [{{
                    data: [{sk.get('neutral_mentions', 163)}, {sk.get('positive_mentions', 100)}, {sk.get('negative_mentions', 93)}],
                    backgroundColor: ['#64748B', '#10B981', '#EF4444'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ labels: {{ color: '#CBD5E1' }} }} }}
            }}
        }});

        // Media Types Chart
        const ctxMedia = document.getElementById('mediaChart').getContext('2d');
        new Chart(ctxMedia, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([m["type"] for m in media_types])},
                datasets: [{{
                    label: 'Menciones',
                    data: {json.dumps([m["count"] for m in media_types])},
                    backgroundColor: '#0284C7',
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{ grid: {{ color: '#1E293B' }}, ticks: {{ color: '#94A3B8' }} }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#94A3B8' }} }}
                }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});
    </script>
</body>
</html>
"""
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_file = reports_dir / "dashboard_queremostrabajar.html"
    index_file = Path("index.html")

    report_file.write_text(html_content, encoding="utf-8")
    index_file.write_text(html_content, encoding="utf-8")
    print(f"✔ HTML Dashboard generado en: {report_file} y sincronizado en: {index_file}")

if __name__ == "__main__":
    generate_html()
