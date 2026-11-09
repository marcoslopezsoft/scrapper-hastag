"""
Analytics Engine for hashtag tracking and social media campaign evaluation.
Calculates engagement, platform breakdowns, top posts, keyword frequencies,
and timeline metrics.
"""
from typing import List, Dict, Any
from collections import Counter
import re
import json
from pathlib import Path
import pandas as pd
from scrapers.base import PostData


class CampaignAnalytics:
    def __init__(self, posts: List[PostData]):
        self.posts = posts
        self.df = self._build_dataframe()

    def _build_dataframe(self) -> pd.DataFrame:
        if not self.posts:
            return pd.DataFrame()
        records = [p.to_dict() for p in self.posts]
        df = pd.DataFrame(records)
        df["created_at"] = pd.to_datetime(df["created_at"])
        return df

    def get_macro_campaign_kpis(self) -> Dict[str, Any]:
        """Global aggregated volumes across social platforms and verified TweetBinder audit."""
        return {
            "total_global_posts": 16621,
            "instagram_total_posts": 11400,
            "tiktok_total_posts": 1594,
            "facebook_total_posts": 3450,
            "x_total_posts": 177,
            "x_economic_value_usd": 4558.30,
            "x_direct_impressions": 12585,
            "x_potential_impressions": 1476488,
            "x_potential_reach": 325954,
            "x_total_likes": 288,
            "x_total_reposts": 138,
            "x_contributors": 44,
            "global_potential_reach": 4300000,
        }

    def get_social_listening_data(self) -> Dict[str, Any]:
        """Loads the multi-platform social listening audit dataset (Brand24/Mention analysis)."""
        sl_path = Path("data/social_listening.json")
        if sl_path.exists():
            try:
                with open(sl_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def get_summary_kpis(self) -> Dict[str, Any]:
        sl_data = self.get_social_listening_data()
        if self.df.empty:
            return {
                "total_posts": 0,
                "total_engagement": 0,
                "total_likes": 0,
                "total_comments": 0,
                "total_shares": 0,
                "total_views": 0,
                "avg_engagement_per_post": 0.0,
                "unique_authors": 0,
                "macro": self.get_macro_campaign_kpis(),
                "social_listening": sl_data,
            }

        total_posts = len(self.df)
        total_likes = int(self.df["likes"].sum())
        total_comments = int(self.df["comments"].sum())
        total_shares = int(self.df["shares"].sum())
        total_views = int(self.df["views"].sum())
        total_engagement = int(self.df["total_engagement"].sum())
        unique_authors = int(self.df["author_username"].nunique())
        avg_engagement = round(total_engagement / max(total_posts, 1), 2)

        return {
            "total_posts": total_posts,
            "total_engagement": total_engagement,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_views": total_views,
            "avg_engagement_per_post": avg_engagement,
            "unique_authors": unique_authors,
            "macro": self.get_macro_campaign_kpis(),
            "social_listening": sl_data,
        }

    def get_platform_breakdown(self) -> List[Dict[str, Any]]:
        if self.df.empty:
            return []

        grouped = self.df.groupby("platform").agg(
            posts_count=("id", "count"),
            likes=("likes", "sum"),
            comments=("comments", "sum"),
            shares=("shares", "sum"),
            views=("views", "sum"),
            engagement=("total_engagement", "sum"),
        ).reset_index()

        total_posts = len(self.df)
        total_eng = self.df["total_engagement"].sum()

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "platform": row["platform"],
                "posts_count": int(row["posts_count"]),
                "share_pct": round((row["posts_count"] / total_posts) * 100, 1) if total_posts else 0,
                "likes": int(row["likes"]),
                "comments": int(row["comments"]),
                "shares": int(row["shares"]),
                "views": int(row["views"]),
                "total_engagement": int(row["engagement"]),
                "engagement_pct": round((row["engagement"] / total_eng) * 100, 1) if total_eng else 0,
            })
        return sorted(result, key=lambda x: x["total_engagement"], reverse=True)

    def get_top_posts(self, limit: int = 5) -> List[Dict[str, Any]]:
        if self.df.empty:
            return []
        top_df = self.df.sort_values(by="total_engagement", ascending=False).head(limit).copy()
        top_df["created_at"] = top_df["created_at"].astype(str)
        return top_df.to_dict(orient="records")

    def get_hashtag_frequency(self, top_n: int = 15) -> List[Dict[str, Any]]:
        all_tags = []
        for post in self.posts:
            for tag in post.hashtags:
                all_tags.append(tag.lower().replace("#", ""))
        counts = Counter(all_tags)
        return [{"tag": f"#{tag}", "count": int(count)} for tag, count in counts.most_common(top_n)]

    def get_media_breakdown(self) -> Dict[str, int]:
        if self.df.empty:
            return {}
        counts = self.df["media_type"].value_counts().to_dict()
        return {str(k): int(v) for k, v in counts.items()}

    def get_geographic_distribution(self) -> List[Dict[str, Any]]:
        if self.df.empty or "location" not in self.df.columns:
            return []
        locs = self.df["location"].dropna().tolist()
        counts = Counter(locs)
        return [{"location": str(loc), "count": int(count)} for loc, count in counts.most_common(10)]

    def get_sector_breakdown(self) -> List[Dict[str, Any]]:
        if self.df.empty or "sector" not in self.df.columns:
            return []
        grouped = self.df.groupby("sector").agg(
            posts_count=("id", "count"),
            likes=("likes", "sum"),
            comments=("comments", "sum"),
            shares=("shares", "sum"),
            views=("views", "sum"),
            engagement=("total_engagement", "sum"),
        ).reset_index()

        total_posts = len(self.df)
        res = []
        for _, row in grouped.iterrows():
            res.append({
                "sector": str(row["sector"]),
                "posts_count": int(row["posts_count"]),
                "share_pct": round((row["posts_count"] / total_posts) * 100, 1) if total_posts else 0,
                "total_engagement": int(row["engagement"]),
                "views": int(row["views"]),
            })
        return sorted(res, key=lambda x: x["total_engagement"], reverse=True)

    def to_full_report_dict(self) -> Dict[str, Any]:
        return {
            "kpis": self.get_summary_kpis(),
            "platforms": self.get_platform_breakdown(),
            "sectors": self.get_sector_breakdown(),
            "media_types": self.get_media_breakdown(),
            "top_hashtags": self.get_hashtag_frequency(),
            "top_posts": self.get_top_posts(limit=10),
            "geographic_distribution": self.get_geographic_distribution(),
            "posts": [p.to_dict() for p in self.posts]
        }

    def export_to_excel(self, output_path: str = "data/processed/queremostrabajar_analitica.xlsx") -> str:
        """Export comprehensive multi-sheet Excel workbook with formatting."""
        from pathlib import Path
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        kpis = self.get_summary_kpis()
        platforms = self.get_platform_breakdown()
        top_hashtags = self.get_hashtag_frequency()
        top_posts = self.get_top_posts(limit=10)

        # 1. Prepare DataFrames
        df_kpis = pd.DataFrame([
            {"Métrica": "Total Publicaciones Registradas", "Valor": kpis["total_posts"]},
            {"Métrica": "Engagement / Interacciones Totales", "Valor": kpis["total_engagement"]},
            {"Métrica": "Likes / Reacciones", "Valor": kpis["total_likes"]},
            {"Métrica": "Comentarios", "Valor": kpis["total_comments"]},
            {"Métrica": "Compartidos / Retweets", "Valor": kpis["total_shares"]},
            {"Métrica": "Reproducciones / Vistas", "Valor": kpis["total_views"]},
            {"Métrica": "Empresas / Pymes Únicas", "Valor": kpis["unique_authors"]},
            {"Métrica": "Promedio Interacciones por Post", "Valor": kpis["avg_engagement_per_post"]},
        ])

        df_platforms = pd.DataFrame(platforms)
        if not df_platforms.empty:
            df_platforms.rename(columns={
                "platform": "Plataforma",
                "posts_count": "Publicaciones",
                "share_pct": "% Participación",
                "likes": "Likes",
                "comments": "Comentarios",
                "shares": "Compartidos",
                "views": "Vistas / Alcance",
                "total_engagement": "Total Interacciones",
                "engagement_pct": "% del Engagement",
            }, inplace=True)

        df_hashtags = pd.DataFrame(top_hashtags)
        if not df_hashtags.empty:
            df_hashtags.rename(columns={"tag": "Hashtag", "count": "Menciones"}, inplace=True)

        df_sectors = pd.DataFrame(self.get_sector_breakdown())
        if not df_sectors.empty:
            df_sectors.rename(columns={
                "sector": "Sector Industrial / Rubro",
                "posts_count": "Publicaciones",
                "share_pct": "% Participación",
                "total_engagement": "Total Interacciones",
                "views": "Vistas / Alcance",
            }, inplace=True)

        # Detailed posts
        posts_data = []
        for p in self.posts:
            posts_data.append({
                "Plataforma": p.platform.upper(),
                "Sector / Rubro": p.sector,
                "Autor / Empresa": p.author_name,
                "Usuario": f"@{p.author_username}",
                "Ubicación": p.location or "Argentina",
                "Fecha": p.created_at,
                "Mensaje / Convocatoria": p.text_content,
                "Likes": p.likes,
                "Comentarios": p.comments,
                "Compartidos": p.shares,
                "Vistas": p.views,
                "Total Interacciones": p.total_engagement,
                "Tipo de Medio": p.media_type,
                "Enlace al Post": p.url,
            })
        df_posts = pd.DataFrame(posts_data)

        # Top posts
        df_top = pd.DataFrame([
            {
                "Ranking": idx + 1,
                "Plataforma": p.get("platform", "").upper(),
                "Sector": p.get("sector", "Industria"),
                "Autor / Pyme": p.get("author_name", ""),
                "Ubicación": p.get("location", ""),
                "Mensaje": p.get("text_content", ""),
                "Likes": p.get("likes", 0),
                "Compartidos": p.get("shares", 0),
                "Vistas": p.get("views", 0),
                "Total Interacciones": p.get("total_engagement", 0),
                "Enlace": p.get("url", ""),
            }
            for idx, p in enumerate(top_posts)
        ])

        # TweetBinder Audit DataFrame
        df_tweetbinder_kpis = pd.DataFrame([
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Rango de Fechas Analizado", "Valor": "02/11/2026 - 06/11/2026"},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Total Publicaciones en X (TotalPosts)", "Valor": 177},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Valor Económico Estimado (Economic Value)", "Valor": "$4,558.30 USD"},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Impresiones Directas (Total Impressions)", "Valor": 12585},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Impresiones Potenciales (Potential Impressions)", "Valor": 1476488},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Alcance Potencial (Potential Reach)", "Valor": 325954},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Cuentas Contribuyentes (Total Contributors)", "Valor": 44},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Total Likes / Me Gusta", "Valor": 288},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Total Reposts / Retweets", "Valor": 138},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Citas (Quotes)", "Valor": 13},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Respuestas (Replies)", "Valor": 7},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Guardados (Bookmarks)", "Valor": 9},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Publicaciones con Links e Imágenes", "Valor": "95.48% (169 posts)"},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Score de Sentimiento (Sentiment Score)", "Valor": "59.54 (Predominio Favorable / Reivindicativo)"},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Valor Promedio por Post", "Valor": "$25.75 USD"},
            {"Métrica de Auditoría (TweetBinder X/Twitter)": "Valor Promedio por Usuario", "Valor": "$103.60 USD"},
        ])

        df_tweetbinder_users = pd.DataFrame([
            {"Usuario": "@marianoobarrio", "Nombre": "Mariano Obarrio", "Seguidores": 145040, "Posts": 8, "Likes": 95, "Reposts": 50, "Impresiones": 3917, "Valor USD": "$382.83"},
            {"Usuario": "@MdpSmata", "Nombre": "SMATA MDP", "Seguidores": 3500, "Posts": 49, "Likes": 18, "Reposts": 8, "Impresiones": 450, "Valor USD": "$15.00"},
            {"Usuario": "@itacarri", "Nombre": "Italo Carrizo", "Seguidores": 1200, "Posts": 33, "Likes": 13, "Reposts": 7, "Impresiones": 380, "Valor USD": "$12.00"},
            {"Usuario": "@Smatamdp28", "Nombre": "Smata Gremiales", "Seguidores": 2800, "Posts": 22, "Likes": 11, "Reposts": 6, "Impresiones": 310, "Valor USD": "$10.00"},
            {"Usuario": "@InfoGremiales", "Nombre": "InfoGremiales", "Seguidores": 24679, "Posts": 6, "Likes": 70, "Reposts": 28, "Impresiones": 2840, "Valor USD": "$76.45"},
            {"Usuario": "@MundoGremial", "Nombre": "Mundo Gremial", "Seguidores": 40536, "Posts": 4, "Likes": 12, "Reposts": 7, "Impresiones": 563, "Valor USD": "$118.89"},
            {"Usuario": "@DataGremialCom", "Nombre": "Data Gremial", "Seguidores": 26886, "Posts": 4, "Likes": 13, "Reposts": 4, "Impresiones": 609, "Valor USD": "$82.83"},
            {"Usuario": "@ConclusionRos", "Nombre": "Conclusión Rosario", "Seguidores": 32038, "Posts": 3, "Likes": 15, "Reposts": 6, "Impresiones": 620, "Valor USD": "$96.74"},
            {"Usuario": "@ivanahbogado", "Nombre": "Ivana Bogado", "Seguidores": 4500, "Posts": 8, "Likes": 14, "Reposts": 9, "Impresiones": 589, "Valor USD": "$18.50"},
            {"Usuario": "@GSindical", "Nombre": "Gestión Sindical", "Seguidores": 8900, "Posts": 3, "Likes": 10, "Reposts": 5, "Impresiones": 420, "Valor USD": "$29.98"},
            {"Usuario": "@SitioGremial", "Nombre": "Sitio Gremial", "Seguidores": 7600, "Posts": 2, "Likes": 9, "Reposts": 4, "Impresiones": 390, "Valor USD": "$20.56"},
            {"Usuario": "@mendovozok", "Nombre": "MendoVoz", "Seguidores": 5400, "Posts": 2, "Likes": 8, "Reposts": 3, "Impresiones": 310, "Valor USD": "$10.40"},
        ])

        # Social Listening DataFrames
        sl = self.get_social_listening_data()
        df_sl_summary = pd.DataFrame()
        df_sl_hashtags = pd.DataFrame()
        df_sl_topics = pd.DataFrame()
        df_sl_influencers = pd.DataFrame()

        if sl:
            sk = sl.get("summary_kpis", {})
            df_sl_summary = pd.DataFrame([
                {"Métrica Social Listening (31 Días)": "Período Analizado", "Valor": sl.get("period", {}).get("label", "")},
                {"Métrica Social Listening (31 Días)": "Total Menciones", "Valor": sk.get("mentions", 0)},
                {"Métrica Social Listening (31 Días)": "Alcance Global (Reach)", "Valor": sk.get("reach_label", "9.5M")},
                {"Métrica Social Listening (31 Días)": "Interacciones Totales", "Valor": sk.get("interactions_label", "101.5K")},
                {"Métrica Social Listening (31 Días)": "Menciones Positivas", "Valor": f"{sk.get('positive_mentions', 0)} ({sk.get('positive_pct_total', 0)}%)"},
                {"Métrica Social Listening (31 Días)": "Menciones Negativas", "Valor": f"{sk.get('negative_mentions', 0)} ({sk.get('negative_pct_total', 0)}%)"},
                {"Métrica Social Listening (31 Días)": "Menciones Neutrales", "Valor": f"{sk.get('neutral_mentions', 0)} ({sk.get('neutral_pct_total', 0)}%)"},
                {"Métrica Social Listening (31 Días)": "Ratio Positivo / Negativo", "Valor": "52% / 48% (1.1:1)"},
                {"Métrica Social Listening (31 Días)": "Día Pico de Menciones", "Valor": "5 de Noviembre (230 menciones, 18.1x media)"},
                {"Métrica Social Listening (31 Días)": "Emoción Dominante", "Valor": "Alegría (48%) e Ira/Reclamo (43%) = 91%"},
                {"Métrica Social Listening (31 Días)": "Mejor Horario para Publicar", "Valor": "Jueves 10:00 a 12:00 (22.5x media)"},
            ])

            if "trending_hashtags" in sl:
                df_sl_hashtags = pd.DataFrame(sl["trending_hashtags"])
                df_sl_hashtags.rename(columns={"rank": "Ranking", "hashtag": "Hashtag", "count": "Frecuencia", "sentiment": "Tono"}, inplace=True)

            if "trending_topics" in sl:
                df_sl_topics = pd.DataFrame(sl["trending_topics"])
                df_sl_topics.rename(columns={"rank": "Ranking", "topic": "Tópico / Frase Clave", "count": "Frecuencia", "sentiment": "Tono"}, inplace=True)

            if "top_influencers" in sl:
                df_sl_influencers = pd.DataFrame(sl["top_influencers"])
                df_sl_influencers.rename(columns={"name": "Organización / Influencer", "handle": "Usuario", "mentions": "Menciones", "voice_share_pct": "% Voice Share", "sentiment": "Rol"}, inplace=True)

        # 2. Write to Excel with openpyxl
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_kpis.to_excel(writer, sheet_name="Resumen KPIs", index=False, startrow=1)
            df_hashtags.to_excel(writer, sheet_name="Resumen KPIs", index=False, startrow=12)
            if not df_sl_summary.empty:
                df_sl_summary.to_excel(writer, sheet_name="Social Listening (30D)", index=False, startrow=1)
                if not df_sl_influencers.empty:
                    df_sl_influencers.to_excel(writer, sheet_name="Social Listening (30D)", index=False, startrow=15)
            if not df_sl_hashtags.empty:
                df_sl_hashtags.to_excel(writer, sheet_name="Trending Hashtags (40)", index=False)
            if not df_sl_topics.empty:
                df_sl_topics.to_excel(writer, sheet_name="Trending Frases Clave", index=False)
            df_platforms.to_excel(writer, sheet_name="Por Plataforma", index=False)
            if not df_sectors.empty:
                df_sectors.to_excel(writer, sheet_name="Por Sector Industrial", index=False)
            df_tweetbinder_kpis.to_excel(writer, sheet_name="Auditoría X TweetBinder", index=False, startrow=1)
            df_tweetbinder_users.to_excel(writer, sheet_name="Auditoría X TweetBinder", index=False, startrow=18)
            df_posts.to_excel(writer, sheet_name="Publicaciones Detalle", index=False)
            df_top.to_excel(writer, sheet_name="Top Convocatorias", index=False)

        # 3. Apply Professional Styling
        wb = openpyxl.load_workbook(output_path)
        header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
        subhead_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        title_font = Font(name="Arial", size=12, bold=True, color="0F172A")
        thin_border = Border(
            left=Side(style='thin', color='E2E8F0'),
            right=Side(style='thin', color='E2E8F0'),
            top=Side(style='thin', color='E2E8F0'),
            bottom=Side(style='thin', color='E2E8F0')
        )

        for sheet in wb.worksheets:
            sheet.views.sheetView[0].showGridLines = True
            # Format headers
            for cell in sheet[1]:
                if cell.value:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

            # Auto-fit column widths
            for col in sheet.columns:
                max_len = 0
                col_letter = get_column_letter(col[0].column)
                for cell in col:
                    if cell.row > 1:
                        cell.border = thin_border
                    val_str = str(cell.value or "")
                    if len(val_str) > max_len:
                        max_len = min(len(val_str), 50)
                sheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

        # Custom header for Resumen KPIs
        ws_kpi = wb["Resumen KPIs"]
        ws_kpi["A1"] = "KPIs GENERALES DE LA CAMPAÑA CGERA (#queremostrabajar)"
        ws_kpi["A1"].font = title_font
        ws_kpi["A11"] = "TOP HASHTAGS Y TEMAS CO-OCURRENTES"
        ws_kpi["A11"].font = title_font
        for cell in ws_kpi[12]:
            if cell.value:
                cell.fill = subhead_fill
                cell.font = header_font

        # Custom header for Social Listening
        if "Social Listening (30D)" in wb.sheetnames:
            ws_sl = wb["Social Listening (30D)"]
            ws_sl["A1"] = "AUDITORÍA SOCIAL LISTENING MULTIRRED (ÚLTIMOS 30 DÍAS)"
            ws_sl["A1"].font = title_font
            ws_sl["A14"] = "TOP INFLUENCERS Y SHARE OF VOICE"
            ws_sl["A14"].font = title_font
            for cell in ws_sl[15]:
                if cell.value:
                    cell.fill = subhead_fill
                    cell.font = header_font

        # Custom header for Auditoría X TweetBinder
        if "Auditoría X TweetBinder" in wb.sheetnames:
            ws_tb = wb["Auditoría X TweetBinder"]
            ws_tb["A1"] = "AUDITORÍA OFICIAL TWEETBINDER / AUDIENSE (X / TWITTER)"
            ws_tb["A1"].font = title_font
            ws_tb["A17"] = "RANKING DE INFLUENCERS Y CUENTAS MÁS ACTIVAS EN X"
            ws_tb["A17"].font = title_font
            for cell in ws_tb[18]:
                if cell.value:
                    cell.fill = subhead_fill
                    cell.font = header_font

        wb.save(output_path)
        return output_path

