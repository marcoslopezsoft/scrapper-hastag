"""
Streamlit Web Dashboard for #queremostrabajar Social Media Analytics.
Interactive visualization, live filters, sector analytics, and instant data exports.
"""
import streamlit as st
import pandas as pd
import json
import subprocess
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="#queremostrabajar | Dashboard CGERA & CSIRA",
    page_icon="🇦🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .badge-cgera {
        background-color: #0284c7;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-ig {
        background: linear-gradient(45deg, #f09433, #dc2743, #bc1888);
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }
    .badge-tt {
        background-color: #000000;
        border: 1px solid #ff0050;
        color: #00f2fe;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# 2. Data Loading Functions
@st.cache_data(ttl=60)
def load_data():
    csv_path = Path("data/processed/queremostrabajar_posts.csv")
    json_path = Path("data/processed/queremostrabajar_posts.json")

    if not csv_path.exists() or not json_path.exists():
        return None, None

    df = pd.read_csv(csv_path)
    with open(json_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    return df, report


df, report = load_data()

# 3. Sidebar Configuration & Controls
with st.sidebar:
    st.image("https://cgera.net.ar/wp-content/uploads/2025/12/cropped-logo2-1-150x108.webp", width=120)
    st.title("🇦🇷 #queremostrabajar")
    st.caption("Campaña CGERA & CSIRA: 'Mostrá tu producto argentino, defendé tu trabajo'")
    st.markdown("---")

    st.subheader("🔍 Filtros de Visualización")

    if df is not None and not df.empty:
        # Platform filter
        all_platforms = ["Todas"] + sorted(list(df["platform"].str.upper().unique()))
        selected_platform = st.selectbox("Plataforma", all_platforms)

        # Sector filter
        all_sectors = ["Todos"] + sorted(list(df["sector"].dropna().unique()))
        selected_sector = st.selectbox("Sector Industrial / Rubro", all_sectors)

        # Search term
        search_term = st.text_input("Buscador libre (empresa, pyme o texto)", placeholder="Ej: laclasedigital, robotica, calzado...")

        st.markdown("---")
        st.subheader("📥 Exportaciones Directas")

        excel_path = Path("data/processed/queremostrabajar_analitica.xlsx")
        if excel_path.exists():
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="📗 Descargar Excel (.xlsx)",
                    data=f,
                    file_name="queremostrabajar_analitica.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        csv_path = Path("data/processed/queremostrabajar_posts.csv")
        if csv_path.exists():
            with open(csv_path, "rb") as f:
                st.download_button(
                    label="📄 Descargar CSV",
                    data=f,
                    file_name="queremostrabajar_posts.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        json_path = Path("data/processed/queremostrabajar_posts.json")
        if json_path.exists():
            with open(json_path, "rb") as f:
                st.download_button(
                    label="📦 Descargar JSON",
                    data=f,
                    file_name="queremostrabajar_posts.json",
                    mime="application/json",
                    use_container_width=True
                )

        st.markdown("---")
        if st.button("🔄 Re-escanear y Actualizar Datos", use_container_width=True):
            with st.spinner("Ejecutando scraper y actualizando métricas..."):
                res = subprocess.run(["python", "main.py"], capture_output=True, text=True)
                if res.returncode == 0:
                    st.success("¡Datos actualizados con éxito!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Error al actualizar: {res.stderr}")


# 4. Main Page Display
if df is None or df.empty:
    st.warning("No se encontraron datos procesados. Ejecutá el scraper para generar los datasets.")
    if st.button("Iniciar Extracción Ahora"):
        with st.spinner("Scrapeando publicaciones..."):
            subprocess.run(["python", "main.py"])
            st.rerun()
    st.stop()

# Filter Data according to Sidebar Inputs
filtered_df = df.copy()

if selected_platform != "Todas":
    filtered_df = filtered_df[filtered_df["platform"].str.upper() == selected_platform]

if selected_sector != "Todos":
    filtered_df = filtered_df[filtered_df["sector"] == selected_sector]

if search_term:
    q = search_term.lower()
    filtered_df = filtered_df[
        filtered_df["author_name"].astype(str).str.lower().str.contains(q) |
        filtered_df["author_username"].astype(str).str.lower().str.contains(q) |
        filtered_df["location"].astype(str).str.lower().str.contains(q) |
        filtered_df["text_content"].astype(str).str.lower().str.contains(q) |
        filtered_df["sector"].astype(str).str.lower().str.contains(q)
    ]

# Header Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #0c4a6e 0%, #0f172a 100%); padding: 24px; border-radius: 16px; border: 1px solid #0284c7; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800;">🇦🇷 #queremostrabajar &bull; Monitor Analítico Federal</h1>
    <h3 style="color: #38bdf8; margin-top: 6px; font-size: 16px; font-weight: 600;">Campaña Nacional: "Mostrá tu producto argentino, defendé tu trabajo" &bull; CGERA & CSIRA</h3>
    <p style="color: #cbd5e1; margin: 8px 0 0 0; font-size: 13px; line-height: 1.5;">
        Convocatoria nacional a todas las industrias, fábricas, talleres y comercios del país para alertar sobre la situación de la producción nacional y el empleo formal.
        <a href="https://cgera.net.ar/mostra-tu-producto/" target="_blank" style="color: #38bdf8; text-decoration: underline;">Portal oficial de CGERA</a> &bull; +2.339 visitas registradas &bull; +304 kits visuales descargados.
    </p>
</div>
""", unsafe_allow_html=True)

# Macro Stats Callout
macro = report.get("kpis", {}).get("macro", {}) if report else {}
m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
with m_col1:
    st.metric("📸 Instagram Macro", f"{macro.get('instagram_total_posts', 11200):,} posts", "11.2k publicaciones")
with m_col2:
    st.metric("🎵 TikTok Macro", f"{macro.get('tiktok_total_posts', 1582):,} posts", "1.58k videos")
with m_col3:
    st.metric("🐦 X (TweetBinder)", f"{macro.get('x_total_posts', 174):,} posts", "Auditado TweetBinder")
with m_col4:
    st.metric("👥 Facebook Macro", f"{macro.get('facebook_total_posts', 3400):,} posts", "Comunidades / Pymes")
with m_col5:
    st.metric("🌐 Alcance Potencial", "4.2M+", "Impacto federal")

st.markdown("---")

tab_general, tab_tweetbinder, tab_table = st.tabs([
    "📊 Métricas & Gráficos",
    "🐦 Auditoría Certificada X (TweetBinder / Audiense)",
    "📋 Relevamiento Detallado de Publicaciones"
])

with tab_general:
    # 5. Top KPI Metric Cards
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        st.metric(
            label="Muestreo Relevado",
            value=f"{len(filtered_df):,}",
            delta=f"{len(df)} posts analizados",
        )

    with kpi2:
        st.metric(
            label="Interacciones Muestreo",
            value=f"{int(filtered_df['total_engagement'].sum()):,}",
            delta="Likes + RTs + Comms",
        )

    with kpi3:
        st.metric(
            label="Reproducciones / Vistas",
            value=f"{int(filtered_df['views'].sum()):,}",
            delta="Vistas calculadas",
        )

    with kpi4:
        st.metric(
            label="Empresas & Gremios",
            value=f"{filtered_df['author_username'].nunique()}",
            delta="Voces activas",
        )

    with kpi5:
        avg_eng = round(filtered_df['total_engagement'].mean(), 1) if not filtered_df.empty else 0
        st.metric(
            label="Prom. Engagement / Post",
            value=f"{avg_eng:,}",
            delta="Impacto promedio",
        )

    st.markdown("---")

    # 6. Interactive Visualizations (Plotly)
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📱 Distribución del Muestreo por Red")
        plat_counts = filtered_df["platform"].str.upper().value_counts().reset_index()
        plat_counts.columns = ["Plataforma", "Publicaciones"]

        fig_pie = px.pie(
            plat_counts,
            values="Publicaciones",
            names="Plataforma",
            hole=0.45,
            color="Plataforma",
            color_discrete_map={
                "INSTAGRAM": "#E1306C",
                "TIKTOK": "#00F2FE",
                "X": "#475569",
                "FACEBOOK": "#1877F2",
                "CGERA": "#0284C7"
            }
        )
        fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("🏭 Interacciones por Sector Industrial")
        sector_eng = filtered_df.groupby("sector")["total_engagement"].sum().reset_index()
        sector_eng = sector_eng.sort_values(by="total_engagement", ascending=True)

        fig_bar = px.bar(
            sector_eng,
            x="total_engagement",
            y="sector",
            orientation="h",
            labels={"total_engagement": "Interacciones Totales", "sector": "Sector"},
            color="total_engagement",
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # 7. Highlighted Top Viral Posts & User Reel
    st.subheader("🔥 Convocatorias y Testimonios Destacados")

    top_viral = filtered_df.sort_values(by="total_engagement", ascending=False).head(4)
    card_cols = st.columns(len(top_viral) if len(top_viral) > 0 else 1)

    for idx, (_, post) in enumerate(top_viral.iterrows()):
        with card_cols[idx]:
            st.markdown(f"""
            <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 14px; min-height: 220px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #38bdf8;">{post['platform']}</span>
                        <span style="font-size: 11px; color: #94a3b8;">{post.get('location', 'Argentina')}</span>
                    </div>
                    <div style="font-size: 10px; background: #1e293b; color: #38bdf8; padding: 2px 6px; border-radius: 6px; display: inline-block; margin-bottom: 6px;">
                        {post.get('sector', 'Industria')}
                    </div>
                    <div style="font-size: 13px; font-weight: 700; color: white;">{post['author_name']}</div>
                    <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">@{post['author_username']}</div>
                    <div style="font-size: 12px; color: #cbd5e1; line-height: 1.4; max-height: 60px; overflow: hidden;">
                        "{str(post['text_content'])[:120]}..."
                    </div>
                </div>
                <div style="border-top: 1px solid #1e293b; padding-top: 8px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #94a3b8;">
                    <span>❤️ {int(post['likes']):,}</span>
                    <span>🔄 {int(post['shares']):,}</span>
                    <a href="{post['url']}" target="_blank" style="color: #38bdf8; font-weight: 700; text-decoration: none;">Ver enlace ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_tweetbinder:
    st.markdown("""
    <div style="background-color: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <h3 style="color: #38bdf8; margin: 0 0 10px 0;">Auditoría Oficial TweetBinder by Audiense (X / Twitter)</h3>
        <p style="color: #cbd5e1; font-size: 13px; margin: 0;">
            Datos certificados del reporte analítico de X para el hashtag <b>#queremostrabajar</b> (período 02/11/2026 - 05/11/2026).
        </p>
    </div>
    """, unsafe_allow_html=True)

    tb1, tb2, tb3, tb4 = st.columns(4)
    with tb1:
        st.metric("Valor Económico", "$4,559.42 USD", "Calculado TweetBinder")
    with tb2:
        st.metric("Impresiones Potenciales", "1,474,013", "Alcance potencial: 325,904")
    with tb3:
        st.metric("Impresiones Directas", "11,824", "281 Likes / 135 Reposts")
    with tb4:
        st.metric("Cuentas Contribuidoras", "43 usuarios", "4.05 posts / usuario")

    st.markdown("---")

    col_tb_a, col_tb_b = st.columns(2)

    with col_tb_a:
        st.subheader("🏆 Top Cuentas más Influyentes (Seguidores)")
        top_inf = pd.DataFrame([
            {"Usuario": "@marianoobarrio", "Nombre": "Mariano Obarrio", "Seguidores": 145040, "Valor Económico": "$3,544.98"},
            {"Usuario": "@MundoGremial", "Nombre": "Mundo Gremial", "Seguidores": 40532, "Valor Económico": "$131.05"},
            {"Usuario": "@ConclusionRos", "Nombre": "Conclusión Rosario", "Seguidores": 32039, "Valor Económico": "$106.65"},
            {"Usuario": "@DataGremialCom", "Nombre": "Data Gremial", "Seguidores": 26888, "Valor Económico": "$91.31"},
            {"Usuario": "@InfoGremiales", "Nombre": "InfoGremiales", "Seguidores": 24680, "Valor Económico": "$505.69"}
        ])
        st.dataframe(top_inf, use_container_width=True, hide_index=True)

    with col_tb_b:
        st.subheader("📢 Cuentas con Mayor Actividad (Posts)")
        top_act = pd.DataFrame([
            {"Usuario": "@MdpSmata", "Nombre": "SMATA Mar del Plata", "Posts": 49, "Rol": "Sindicato Automotriz"},
            {"Usuario": "@itacarri", "Nombre": "Ítalo Carrizo", "Posts": 33, "Rol": "Militancia Industrial"},
            {"Usuario": "@Smatamdp28", "Nombre": "Smata Gremiales", "Posts": 22, "Rol": "Gremial"},
            {"Usuario": "@marianoobarrio", "Nombre": "Mariano Obarrio", "Posts": 8, "Rol": "Periodista"},
            {"Usuario": "@ivanahbogado", "Nombre": "Ivana H. Bogado", "Posts": 8, "Rol": "Activismo Pyme"}
        ])
        st.dataframe(top_act, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("💡 Hashtags Asociados en la Conversación de X")
    st.write("**#queremostrabajar** (174) &bull; **#industrianacional** (80) &bull; **#trabajoargentino** (75) &bull; **#abramoslaspersianas** (10) &bull; **#csira** (9) &bull; **#infogremiales** (6) &bull; **#periodismosindical** (6) &bull; **#cgera** (5)")

with tab_table:
    # 8. Interactive Data Table
    st.subheader(f"📋 Relevamiento Detallado ({len(filtered_df)} de {len(df)} publicaciones)")

    display_cols = [
        "platform", "author_name", "author_username", "sector", "location",
        "created_at", "likes", "shares", "views", "total_engagement", "url"
    ]

    table_df = filtered_df[display_cols].copy()
    table_df.columns = [
        "Red", "Empresa / Autor", "Usuario", "Sector", "Ubicación",
        "Fecha", "Likes", "Compartidos", "Vistas", "Engagement Total", "Enlace al Post"
    ]

    st.dataframe(
        table_df,
        use_container_width=True,
        column_config={
            "Enlace al Post": st.column_config.LinkColumn(
                "Enlace al Post",
                help="Hacé clic para abrir la publicación original",
                validate=r"^https?://.+",
                max_chars=40
            ),
            "Likes": st.column_config.NumberColumn(format="%d"),
            "Compartidos": st.column_config.NumberColumn(format="%d"),
            "Vistas": st.column_config.NumberColumn(format="%d"),
            "Engagement Total": st.column_config.NumberColumn(format="%d"),
        },
        hide_index=True
    )

st.caption("Campaña CGERA & CSIRA &bull; #queremostrabajar &bull; Desarrollado para monitoreo y seguimiento federal de la producción nacional.")

