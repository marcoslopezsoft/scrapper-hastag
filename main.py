"""
Social Media Hashtag & Campaign Scraper CLI.
Analyzes #queremostrabajar across Instagram, TikTok, X (Twitter), Facebook, and CGERA official.
"""
import argparse
import json
from pathlib import Path
from typing import List
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from scrapers.base import PostData
from scrapers.cgera_campaign import CgeraCampaignScraper
from scrapers.x_scraper import XScraper
from scrapers.tiktok_scraper import TikTokScraper
from scrapers.instagram_scraper import InstagramScraper
from scrapers.facebook_scraper import FacebookScraper
from scrapers.media_extractor import extract_post_from_url
from analytics import CampaignAnalytics
from reporter import generate_html_dashboard

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scraper y Analítica de Redes Sociales para la campaña #queremostrabajar (CGERA)"
    )
    parser.add_argument(
        "--hashtag",
        type=str,
        default="queremostrabajar",
        help="Hashtag objetivo a rastrear (sin #)",
    )
    parser.add_argument(
        "--platforms",
        type=str,
        default="cgera,ig,tiktok,x,fb",
        help="Plataformas separadas por coma: ig, tiktok, x, fb, cgera",
    )
    parser.add_argument(
        "--max-posts",
        type=int,
        default=25,
        help="Máximo de publicaciones por plataforma",
    )
    parser.add_argument(
        "--out-json",
        type=str,
        default="data/processed/queremostrabajar_posts.json",
        help="Ruta de guardado para dataset JSON",
    )
    parser.add_argument(
        "--out-csv",
        type=str,
        default="data/processed/queremostrabajar_posts.csv",
        help="Ruta de guardado para dataset CSV",
    )
    parser.add_argument(
        "--out-excel",
        type=str,
        default="data/processed/queremostrabajar_analitica.xlsx",
        help="Ruta de guardado para reporte y dataset Excel (.xlsx)",
    )
    parser.add_argument(
        "--out-html",
        type=str,
        default="reports/dashboard_queremostrabajar.html",
        help="Ruta de guardado para el Dashboard interactivo HTML",
    )
    parser.add_argument(
        "--urls",
        type=str,
        default="",
        help="URLs específicas separadas por coma para extracción en vivo con yt-dlp",
    )
    parser.add_argument(
        "--urls-file",
        type=str,
        default="data/input_links.txt",
        help="Archivo con lista de enlaces de publicaciones/reels compartidos internamente",
    )
    return parser.parse_args()


def get_scrapers(platforms_str: str, hashtag: str):
    selected = [p.strip().lower() for p in platforms_str.split(",")]
    scrapers = []

    if "cgera" in selected:
        scrapers.append(("CGERA Oficial", CgeraCampaignScraper(hashtag)))
    if "ig" in selected or "instagram" in selected:
        scrapers.append(("Instagram", InstagramScraper(hashtag)))
    if "tiktok" in selected or "tt" in selected:
        scrapers.append(("TikTok", TikTokScraper(hashtag)))
    if "x" in selected or "twitter" in selected:
        scrapers.append(("X (Twitter)", XScraper(hashtag)))
    if "fb" in selected or "facebook" in selected:
        scrapers.append(("Facebook", FacebookScraper(hashtag)))

    return scrapers


def main():
    args = parse_args()

    console.print(
        Panel.fit(
            "[bold white]🇦🇷 CGERA — Campaña 'Mostrá tu producto Argentino, Defendé tu trabajo'[/bold white]\n"
            f"[cyan]Hashtag Objetivo:[/cyan] [bold yellow]#{args.hashtag}[/bold yellow] | "
            f"[cyan]Plataformas:[/cyan] [bold green]{args.platforms}[/bold green]\n"
            "[dim]Referencia: https://cgera.net.ar/mostra-tu-producto/ (5 de Noviembre 12:00 HS)[/dim]",
            border_style="blue",
        )
    )

    scrapers = get_scrapers(args.platforms, args.hashtag)
    all_posts: List[PostData] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        for name, scraper in scrapers:
            task = progress.add_task(f"Extrayendo datos de {name}...", total=None)
            try:
                posts = scraper.scrape(max_posts=args.max_posts)
                all_posts.extend(posts)
                console.print(f"  [green]✔[/green] {name}: [bold]{len(posts)}[/bold] publicaciones extraídas.")
            except Exception as e:
                console.print(f"  [red]✖[/red] Error al extraer de {name}: {e}")
            finally:
                progress.remove_task(task)

    # Ingest direct URLs passed by the user or from input_links.txt
    custom_urls = []
    if args.urls:
        custom_urls.extend([u.strip() for u in args.urls.split(",") if u.strip()])

    if args.urls_file and Path(args.urls_file).exists():
        with open(args.urls_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    custom_urls.append(line)

    if custom_urls:
        console.print(f"\n[cyan]🔍 Extrayendo metadatos en vivo de {len(custom_urls)} enlace(s) directos (yt-dlp)...[/cyan]")
        existing_urls = {p.url.rstrip("/") for p in all_posts}
        live_added = 0
        for u in custom_urls:
            clean_u = u.split("?")[0].rstrip("/")
            # Extract live post metadata
            post = extract_post_from_url(u)
            if post:
                # Insert at top
                all_posts.insert(0, post)
                live_added += 1
                console.print(
                    f"  [bold green]✔[/bold green] [white]{post.platform.upper()}[/white]: "
                    f"[bold yellow]{post.author_name}[/bold yellow] ([dim]@{post.author_username}[/dim]) "
                    f"• {post.likes} likes • {post.url[:55]}..."
                )
            else:
                console.print(f"  [yellow]⚠ No se pudo extraer metadatos de:[/yellow] {u}")

    console.print(f"\n[bold]Total de publicaciones consolidadas:[/bold] [cyan]{len(all_posts)}[/cyan]\n")

    # Run Analytics
    analytics = CampaignAnalytics(all_posts)
    kpis = analytics.get_summary_kpis()
    platforms_breakdown = analytics.get_platform_breakdown()
    top_hashtags = analytics.get_hashtag_frequency()
    top_posts = analytics.get_top_posts(5)
    full_report = analytics.to_full_report_dict()

    # Display KPI Table
    kpi_table = Table(title="📊 Métricas Generales y KPIs de la Convocatoria", border_style="cyan")
    kpi_table.add_column("Métrica", style="white", justify="left")
    kpi_table.add_column("Valor", style="bold green", justify="right")
    kpi_table.add_row("Total Publicaciones Registradas", str(kpis["total_posts"]))
    kpi_table.add_row("Engagement / Interacciones Totales", f"{kpis['total_engagement']:,}")
    kpi_table.add_row("Likes / Reacciones", f"{kpis['total_likes']:,}")
    kpi_table.add_row("Comentarios", f"{kpis['total_comments']:,}")
    kpi_table.add_row("Compartidos / Retweets", f"{kpis['total_shares']:,}")
    kpi_table.add_row("Reproducciones de Video / Vistas", f"{kpis['total_views']:,}")
    kpi_table.add_row("Empresas / Pymes Participantes Únicas", str(kpis["unique_authors"]))
    kpi_table.add_row("Promedio Interacciones por Post", str(kpis["avg_engagement_per_post"]))
    console.print(kpi_table)

    # Display Platform Breakdown Table
    plat_table = Table(title="📱 Rendimiento por Red Social", border_style="magenta")
    plat_table.add_column("Plataforma", style="cyan", justify="left")
    plat_table.add_column("Posts", justify="right")
    plat_table.add_column("% Share", justify="right")
    plat_table.add_column("Interacciones", justify="right")
    plat_table.add_column("Vistas/Alcance", justify="right")

    for p in platforms_breakdown:
        plat_table.add_row(
            p["platform"].upper(),
            str(p["posts_count"]),
            f"{p['share_pct']}%",
            f"{p['total_engagement']:,}",
            f"{p['views']:,}",
        )
    console.print(plat_table)

    # Top Hashtags
    tag_str = "  ".join([f"[cyan]{t['tag']}[/cyan] ({t['count']})" for t in top_hashtags[:8]])
    console.print(f"[bold]Hashtags y lemas más frecuentes:[/bold]\n{tag_str}\n")

    # Save processed outputs
    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)
    console.print(f"[green]✔ Dataset JSON exportado en:[/green] [white]{args.out_json}[/white]")

    # Save CSV
    df = analytics.df
    if not df.empty:
        df.to_csv(args.out_csv, index=False, encoding="utf-8")
        console.print(f"[green]✔ Dataset CSV exportado en:[/green] [white]{args.out_csv}[/white]")

    # Save Excel Workbook
    excel_path = analytics.export_to_excel(args.out_excel)
    console.print(f"[green]✔ Reporte Excel (.xlsx) exportado en:[/green] [bold cyan]{excel_path}[/bold cyan]")

    # Generate HTML Dashboard
    html_path = generate_html_dashboard(full_report, args.out_html)
    console.print(f"[green]✔ Dashboard HTML interactivo generado en:[/green] [bold yellow]{html_path}[/bold yellow]")

    # Also maintain root index.html for direct Vercel / GitHub Pages deployment
    root_index = Path("index.html")
    with open(root_index, "w", encoding="utf-8") as f:
        with open(html_path, "r", encoding="utf-8") as src:
            f.write(src.read())
    console.print(f"[green]✔ Index para Vercel sincronizado en:[/green] [cyan]{root_index}[/cyan]\n")

    console.print(
        Panel(
            f"[bold green]Proceso completado con éxito.[/bold green]\n"
            f"Podés abrir el dashboard directamente en tu navegador con:\n"
            f"[bold white]xdg-open {html_path}[/bold white] o abriéndolo directamente en tu explorador.",
            border_style="green",
        )
    )


def app(environ, start_response):
    """
    WSGI Entrypoint for Vercel Serverless Function deployment.
    Satisfies Vercel Python runtime and serves dashboard and data assets.
    """
    path = environ.get("PATH_INFO", "/")

    # Map paths
    if path in ["", "/", "/dashboard", "/index.html"]:
        file_path = Path("index.html")
        content_type = "text/html; charset=utf-8"
    elif path.endswith(".csv") or "/csv" in path:
        file_path = Path("data/processed/queremostrabajar_posts.csv")
        content_type = "text/csv; charset=utf-8"
    elif path.endswith(".json") or "/json" in path:
        file_path = Path("data/processed/queremostrabajar_posts.json")
        content_type = "application/json; charset=utf-8"
    elif path.endswith(".xlsx") or "/excel" in path:
        file_path = Path("data/processed/queremostrabajar_analitica.xlsx")
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        file_path = Path(path.lstrip("/"))
        content_type = "text/html; charset=utf-8"

    if not file_path.exists():
        # Check reports fallback
        fallback = Path("reports/dashboard_queremostrabajar.html")
        if fallback.exists():
            file_path = fallback
            content_type = "text/html; charset=utf-8"

    if file_path.exists() and file_path.is_file():
        with open(file_path, "rb") as f:
            data = f.read()
        status = "200 OK"
        headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(len(data))),
            ("Cache-Control", "public, max-age=60"),
        ]
        start_response(status, headers)
        return [data]

    status = "404 Not Found"
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return [b"Recurso no encontrado en el servidor."]


# Export for Vercel Python runtime
handler = app
application = app


if __name__ == "__main__":
    main()

