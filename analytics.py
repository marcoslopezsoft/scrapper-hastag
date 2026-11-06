"""
Analytics Engine for hashtag tracking and social media campaign evaluation.
Calculates engagement, platform breakdowns, top posts, keyword frequencies,
and timeline metrics.
"""
from typing import List, Dict, Any
from collections import Counter
import re
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

    def get_summary_kpis(self) -> Dict[str, Any]:
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

    def to_full_report_dict(self) -> Dict[str, Any]:
        return {
            "kpis": self.get_summary_kpis(),
            "platforms": self.get_platform_breakdown(),
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

        # Detailed posts
        posts_data = []
        for p in self.posts:
            posts_data.append({
                "Plataforma": p.platform.upper(),
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

        # 2. Write to Excel with openpyxl
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_kpis.to_excel(writer, sheet_name="Resumen KPIs", index=False, startrow=1)
            df_hashtags.to_excel(writer, sheet_name="Resumen KPIs", index=False, startrow=12)
            df_platforms.to_excel(writer, sheet_name="Por Plataforma", index=False)
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

        wb.save(output_path)
        return output_path

