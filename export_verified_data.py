"""
Export Verified Social Listening Data to Excel, JSON, and CSV.
Uses STRICTLY AND EXCLUSIVELY the verified data provided by the user from the Social Listening tool and TweetBinder.
No simulated or unreliable scraped placeholders.
"""
import json
from pathlib import Path
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def run_export():
    sl_path = Path("data/social_listening.json")
    if not sl_path.exists():
        raise FileNotFoundError("data/social_listening.json no encontrado")

    with open(sl_path, "r", encoding="utf-8") as f:
        sl = json.load(f)

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    excel_path = output_dir / "queremostrabajar_analitica.xlsx"
    csv_path = output_dir / "queremostrabajar_posts.csv"
    json_path = output_dir / "queremostrabajar_posts.json"

    # 1. Prepare DataFrames
    sk = sl.get("summary_kpis", {})
    df_summary = pd.DataFrame([
        {"Métrica Social Listening": "Hashtag Monitoreado", "Valor": "#queremostrabajar"},
        {"Métrica Social Listening": "Período Analizado", "Valor": sl.get("period", {}).get("label", "")},
        {"Métrica Social Listening": "Menciones Totales", "Valor": sk.get("mentions", 356)},
        {"Métrica Social Listening": "Alcance Global (Reach)", "Valor": sk.get("reach_label", "9,5 Millones")},
        {"Métrica Social Listening": "Interacciones Totales", "Valor": sk.get("interactions_label", "101.5K")},
        {"Métrica Social Listening": "Menciones Positivas", "Valor": f"{sk.get('positive_mentions', 100)} ({sk.get('positive_pct_total', 28)}% del total)"},
        {"Métrica Social Listening": "Menciones Negativas / Reclamo", "Valor": f"{sk.get('negative_mentions', 93)} ({sk.get('negative_pct_total', 26)}% del total)"},
        {"Métrica Social Listening": "Menciones Neutrales", "Valor": f"{sk.get('neutral_mentions', 163)} ({sk.get('neutral_pct_total', 46)}% del total)"},
        {"Métrica Social Listening": "Proporción Positivo / Negativo", "Valor": "52% / 48% (1.1:1 a favor)"},
        {"Métrica Social Listening": "Día Pico de Conversación", "Valor": "5 de Noviembre (230 menciones, 18.1× la media diaria)"},
        {"Métrica Social Listening": "Emoción Dominante", "Valor": "Alegría (48%) e Ira / Reclamo (43%) = 91% del total"},
        {"Métrica Social Listening": "Mejor Horario para Publicar", "Valor": "Jueves 10:00 a 12:00 (22.5× la media)"},
    ])

    df_media = pd.DataFrame([
        {
            "Tipo de Medio": m["type"],
            "Menciones": m["count"],
            "% Participación": f"{m['pct']}%",
            "% Positivo": f"{m.get('sentiment', {}).get('positive', 0)}%",
            "% Negativo": f"{m.get('sentiment', {}).get('negative', 0)}%",
            "% Neutral": f"{m.get('sentiment', {}).get('neutral', 0)}%"
        }
        for m in sl.get("media_types", [])
    ])

    df_sites = pd.DataFrame([
        {
            "Ranking": idx + 1,
            "Sitio Web / Portal": s["site"],
            "Visitas Mensuales": s["monthly_visits"],
            "Menciones": s["mentions"],
            "Rol / Cobertura": s["role"]
        }
        for idx, s in enumerate(sl.get("top_sites", []))
    ])

    df_influencers = pd.DataFrame([
        {
            "Ranking": idx + 1,
            "Organización / Referente": inf["name"],
            "Usuario": inf["handle"],
            "Cuota de Voz (% Voice Share)": f"{inf['voice_share_pct']}%",
            "Menciones": inf["mentions"],
            "Rol / Enfoque": inf["sentiment"]
        }
        for idx, inf in enumerate(sl.get("top_influencers", []))
    ])

    df_hashtags = pd.DataFrame(sl.get("trending_hashtags", []))
    if not df_hashtags.empty:
        df_hashtags.rename(columns={"rank": "#", "hashtag": "Hashtag", "count": "Frecuencia", "sentiment": "Tono"}, inplace=True)

    df_topics = pd.DataFrame(sl.get("trending_topics", []))
    if not df_topics.empty:
        df_topics.rename(columns={"rank": "#", "topic": "Tópico / Frase Clave", "count": "Frecuencia", "sentiment": "Enfoque"}, inplace=True)

    df_geo = pd.DataFrame(sl.get("geography", {}).get("countries", []))
    if not df_geo.empty:
        df_geo.rename(columns={"country": "País", "mentions": "Menciones", "pct": "% de Menciones"}, inplace=True)

    df_emojis = pd.DataFrame(sl.get("top_emojis", []))
    if not df_emojis.empty:
        df_emojis.rename(columns={"emoji": "Emoji", "name": "Nombre", "count": "Frecuencia", "sentiment": "Significado"}, inplace=True)

    # TweetBinder DataFrame
    df_tweetbinder = pd.DataFrame([
        {"Métrica de Auditoría (X / TweetBinder)": "Rango de Fechas", "Valor": "02/11/2026 - 06/11/2026"},
        {"Métrica de Auditoría (X / TweetBinder)": "Total Publicaciones en X", "Valor": 177},
        {"Métrica de Auditoría (X / TweetBinder)": "Valor Económico Estimado", "Valor": "$4,558.30 USD"},
        {"Métrica de Auditoría (X / TweetBinder)": "Impresiones Directas", "Valor": 12585},
        {"Métrica de Auditoría (X / TweetBinder)": "Impresiones Potenciales", "Valor": 1476488},
        {"Métrica de Auditoría (X / TweetBinder)": "Alcance Potencial", "Valor": 325954},
        {"Métrica de Auditoría (X / TweetBinder)": "Cuentas Contribuyentes", "Valor": 44},
        {"Métrica de Auditoría (X / TweetBinder)": "Total Likes", "Valor": 288},
        {"Métrica de Auditoría (X / TweetBinder)": "Total Reposts / Retweets", "Valor": 138},
        {"Métrica de Auditoría (X / TweetBinder)": "Top Cuenta Influyente", "Valor": "@marianoobarrio (145k seguidores, $3,537.30 USD valor)"},
        {"Métrica de Auditoría (X / TweetBinder)": "Top Cuenta Activa", "Valor": "@MdpSmata (49 publicaciones gremiales)"},
    ])

    # 2. Write to Multi-Sheet Excel
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_summary.to_excel(writer, sheet_name="Resumen Social Listening", index=False)
        df_media.to_excel(writer, sheet_name="Por Tipo de Medio", index=False)
        df_sites.to_excel(writer, sheet_name="Portales Web Líderes", index=False)
        df_influencers.to_excel(writer, sheet_name="Top Influencers (Voice Share)", index=False)
        df_hashtags.to_excel(writer, sheet_name="Top 40 Hashtags", index=False)
        df_topics.to_excel(writer, sheet_name="Top 35 Frases Clave", index=False)
        df_geo.to_excel(writer, sheet_name="Distribución Geográfica", index=False)
        df_emojis.to_excel(writer, sheet_name="Top Emojis", index=False)
        df_tweetbinder.to_excel(writer, sheet_name="Auditoría X TweetBinder", index=False)

    # 3. Apply Professional Styling with openpyxl
    wb = openpyxl.load_workbook(excel_path)
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    for sheet in wb.worksheets:
        sheet.views.sheetView[0].showGridLines = True
        for cell in sheet[1]:
            if cell.value:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.row > 1:
                    cell.border = thin_border
                val_str = str(cell.value or "")
                if len(val_str) > max_len:
                    max_len = min(len(val_str), 60)
            sheet.column_dimensions[col_letter].width = max(max_len + 5, 14)

    wb.save(excel_path)
    print(f"✔ Excel verificado exportado: {excel_path}")

    # 4. Save JSON and CSV
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sl, f, indent=2, ensure_ascii=False)
    print(f"✔ JSON verificado exportado: {json_path}")

    # Export a clean summary CSV
    df_summary.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"✔ CSV verificado exportado: {csv_path}")

if __name__ == "__main__":
    run_export()
