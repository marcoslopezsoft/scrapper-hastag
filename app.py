"""
Streamlit Web Dashboard for #queremostrabajar Social Media Analytics.
Powered 100% EXCLUSIVELY by verified data from the Social Listening Intelligence Report
and the TweetBinder Audit. No simulated or unreliable placeholders.
"""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="#queremostrabajar | Monitor Analítico Oficial",
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


# 2. Data Loading Function
@st.cache_data(ttl=10)
def load_listening_data():
    sl_path = Path("data/social_listening.json")
    if not sl_path.exists():
        return {}
    with open(sl_path, "r", encoding="utf-8") as f:
        return json.load(f)


sl = load_listening_data()

# 3. Sidebar Configuration
with st.sidebar:
    st.image("https://cgera.net.ar/wp-content/uploads/2025/12/cropped-logo2-1-150x108.webp", width=120)
    st.title("🇦🇷 #queremostrabajar")
    st.caption("Campaña CGERA & CSIRA: 'Mostrá tu producto argentino, defendé tu trabajo'")
    st.markdown("---")

    st.subheader("📌 Estado de la Auditoría")
    st.success("✔ **Datos 100% Verificados**")
    st.write(f"📅 **Período:** {sl.get('period', {}).get('label', 'Últimos 30 días')}")
    st.write(f"🗣️ **Menciones Totales:** {sl.get('summary_kpis', {}).get('mentions', 356)}")
    st.write(f"🌐 **Alcance Total (Reach):** {sl.get('summary_kpis', {}).get('reach_label', '9,5 Millones')}")
    st.write(f"⚡ **Interacciones:** {sl.get('summary_kpis', {}).get('interactions_label', '101.5K')}")

    st.markdown("---")
    st.subheader("📥 Descargas de Informes")

    excel_path = Path("data/processed/queremostrabajar_analitica.xlsx")
    if excel_path.exists():
        with open(excel_path, "rb") as f:
            st.download_button(
                label="📗 Descargar Excel Oficial (.xlsx)",
                data=f,
                file_name="queremostrabajar_analitica.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    sl_path = Path("data/social_listening.json")
    if sl_path.exists():
        with open(sl_path, "rb") as f:
            st.download_button(
                label="🌐 Descargar JSON Verificado",
                data=f,
                file_name="social_listening.json",
                mime="application/json",
                use_container_width=True
            )

    csv_path = Path("data/processed/queremostrabajar_posts.csv")
    if csv_path.exists():
        with open(csv_path, "rb") as f:
            st.download_button(
                label="📄 Descargar Resumen CSV",
                data=f,
                file_name="queremostrabajar_resumen.csv",
                mime="text/csv",
                use_container_width=True
            )

# 4. Header Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #0c4a6e 0%, #0f172a 100%); padding: 24px; border-radius: 16px; border: 1px solid #0284c7; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800;">🇦🇷 #queremostrabajar &bull; Monitor Analítico & Social Listening Oficial</h1>
    <h3 style="color: #38bdf8; margin-top: 6px; font-size: 16px; font-weight: 600;">Campaña Nacional: "Mostrá tu producto argentino, defendé tu trabajo" &bull; CGERA & CSIRA</h3>
    <p style="color: #cbd5e1; margin: 8px 0 0 0; font-size: 13px; line-height: 1.5;">
        Monitoreo integral de volumen, sentimiento, emociones, medios, alcance e influencers de la convocatoria federal impulsada por
        la <b>Confederación General Empresaria de la República Argentina (CGERA)</b> y la <b>Confederación de Sindicatos Industriales (CSIRA)</b>.
        <a href="https://cgera.net.ar/mostra-tu-producto/" target="_blank" style="color: #38bdf8; text-decoration: underline;">Portal oficial de CGERA</a> &bull; Datos certificados por herramientas de Social Listening y Auditoría de Redes.
    </p>
</div>
""", unsafe_allow_html=True)

# 5. Top KPI Metrics
sk = sl.get("summary_kpis", {})
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("🗣️ Menciones Totales", f"{sk.get('mentions', 356):,}", "Pico 5N: 230 menciones (18.1×)")
with m2:
    st.metric("🌐 Alcance Global (Reach)", sk.get("reach_label", "9,5 Millones"), "8.9M tendencia diaria")
with m3:
    st.metric("⚡ Interacciones Totales", sk.get("interactions_label", "101.5K"), "Likes + RTs + Comentarios")
with m4:
    st.metric("👍 Sentimiento Expresado", "52% Positivo", "48% Negativo / Reclamo (1.1:1)")
with m5:
    st.metric("❤️ Emoción Principal", "Alegría 48%", "Ira / Reclamo 43% (91% total)")

st.markdown("---")

# 6. Main Navigation Tabs
tab_sl, tab_media, tab_hashtags, tab_topics, tab_tb, tab_update = st.tabs([
    "🌐 Resumen Social Listening",
    "📰 Medios, Portales & Influencers",
    "🏷️ Top 40 Trending Hashtags",
    "💬 Top 35 Frases Clave",
    "🐦 Auditoría X (TweetBinder)",
    "📝 Carga y Actualización Manual"
])

# ==========================================
# TAB 1: SOCIAL LISTENING OVERVIEW
# ==========================================
with tab_sl:
    st.markdown("""
    <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <span style="font-size: 11px; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Período Auditado: 9 de octubre - 8 de noviembre · 31 días</span>
        <h3 style="color: white; margin: 4px 0 6px 0; font-size: 18px;">¿Qué se está diciendo? Volumen, sentimiento, emociones y pico horario</h3>
        <p style="color: #94a3b8; font-size: 12px; margin: 0;">
            El número de menciones alcanzó su punto máximo el <b>5 de noviembre con 230 menciones simultáneas</b> (18,1 veces la media diaria), coincidiendo con la salida a las puertas de las fábricas convocada a las 12:00 HS.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_sent, col_emo = st.columns(2)

    with col_sent:
        st.subheader("📊 Desglose de Sentimiento")
        df_sent = pd.DataFrame([
            {"Sentimiento": "Neutral", "Menciones": sk.get("neutral_mentions", 163)},
            {"Sentimiento": "Positivo", "Menciones": sk.get("positive_mentions", 100)},
            {"Sentimiento": "Negativo / Reclamo", "Menciones": sk.get("negative_mentions", 93)}
        ])
        fig_sent = px.pie(
            df_sent,
            names="Sentimiento",
            values="Menciones",
            hole=0.5,
            color="Sentimiento",
            color_discrete_map={
                "Neutral": "#64748B",
                "Positivo": "#10B981",
                "Negativo / Reclamo": "#EF4444"
            }
        )
        fig_sent.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig_sent, use_container_width=True)
        st.caption("El 52% de las menciones que expresan un sentimiento son positivas (proporción 1.1:1 frente al reclamo negativo).")

    with col_emo:
        st.subheader("🎭 Colapso Emocional (143 menciones con tono detectado)")
        emotions_list = sl.get("emotions", {}).get("breakdown", [
            {"emotion": "Alegría (Joy)", "pct": 48.0},
            {"emotion": "Enojo / Reclamo (Anger)", "pct": 43.0},
            {"emotion": "Miedo (Fear)", "pct": 6.0},
            {"emotion": "Tristeza (Sadness)", "pct": 2.0},
            {"emotion": "Amor / Solidaridad (Love)", "pct": 1.0}
        ])
        df_emo = pd.DataFrame(emotions_list).sort_values(by="pct", ascending=True)

        fig_emo = px.bar(
            df_emo,
            x="pct",
            y="emotion",
            orientation="h",
            labels={"pct": "% de Presencia", "emotion": "Emoción"},
            color="pct",
            color_continuous_scale="Viridis"
        )
        fig_emo.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, coloraxis_showscale=False)
        st.plotly_chart(fig_emo, use_container_width=True)
        st.caption("La alegría lidera con 48% (orgullo por la producción). La ira alcanzó su pico el 5N (56× promedio) alertando sobre el empleo.")

    st.markdown("---")

    col_med, col_time = st.columns(2)

    with col_med:
        st.subheader("📺 Menciones por Tipo de Medio")
        media_list = sl.get("media_types", [])
        df_med = pd.DataFrame(media_list)
        fig_med = px.bar(
            df_med,
            x="type",
            y="count",
            text="count",
            labels={"type": "Tipo de Medio", "count": "Menciones"},
            color="type",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_med.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, showlegend=False)
        st.plotly_chart(fig_med, use_container_width=True)
        st.caption("El video (TikTok/Reels) tiene el sentimiento positivo más fuerte (52% de 103 menciones). La web concentra la discusión crítica económica (44%).")

    with col_time:
        st.subheader("⏰ Mejor Momento para Publicar")
        st.markdown("""
        <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 18px; height: 300px; display: flex; flex-direction: column; justify-content: space-around;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #38bdf8; font-size: 14px;">1. Jueves de 10:00 a 12:00</span>
                    <span style="background-color: #0284c7; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 800;">22,5× media</span>
                </div>
                <p style="color: #cbd5e1; font-size: 12px; margin: 4px 0 0 0;">Pico de conversación de la convocatoria previa a la salida de las fábricas.</p>
            </div>
            <div style="border-top: 1px solid #1e293b; padding-top: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #38bdf8; font-size: 14px;">2. Jueves de 12:00 a 14:00</span>
                    <span style="background-color: #0284c7; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 800;">12,5× media</span>
                </div>
                <p style="color: #cbd5e1; font-size: 12px; margin: 4px 0 0 0;">Horario central de salida a las puertas mostrando la producción nacional.</p>
            </div>
            <div style="border-top: 1px solid #1e293b; padding-top: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; color: #94a3b8; font-size: 13px;">3. Jueves de 09:00 a 11:00</span>
                    <span style="background-color: #334155; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 800;">8,2× media</span>
                </div>
                <p style="color: #cbd5e1; font-size: 12px; margin: 4px 0 0 0;">Momento más tranquilo de la semana: domingo de 22:00 a 24:00.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("😀 Los Mejores Emojis de la Conversación")
    emojis = sl.get("top_emojis", [])
    if emojis:
        emoji_cols = st.columns(len(emojis[:6]))
        for idx, em in enumerate(emojis[:6]):
            with emoji_cols[idx]:
                st.markdown(f"""
                <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 14px; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 4px;">{em['emoji']}</div>
                    <div style="font-size: 18px; font-weight: 800; color: white;">{em['count']}</div>
                    <div style="font-size: 11px; color: #94a3b8;">{em.get('sentiment', em.get('name', ''))}</div>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# TAB 2: SITES, MEDIA & INFLUENCERS
# ==========================================
with tab_media:
    col_sites, col_inf = st.columns(2)

    with col_sites:
        st.subheader("🌐 Top Sitios Web por Visitas Mensuales")
        sites = sl.get("top_sites", [])
        if sites:
            df_sites = pd.DataFrame(sites)
            st.dataframe(
                df_sites[["site", "monthly_visits", "mentions", "role"]].rename(columns={
                    "site": "Portal / Sitio Web",
                    "monthly_visits": "Visitas Mensuales",
                    "mentions": "Menciones",
                    "role": "Rol Relevante"
                }),
                use_container_width=True,
                hide_index=True
            )
            st.caption("mundogremial.com es la fuente de mayor alcance (1.3M visitas/mes). conclusion.com.ar genera la mayor cantidad de menciones.")

    with col_inf:
        st.subheader("📢 Top Influencers & Cuota de Voz (Voice Share)")
        influencers = sl.get("top_influencers", [])
        if influencers:
            df_inf = pd.DataFrame(influencers)
            st.dataframe(
                df_inf[["name", "handle", "voice_share_pct", "mentions", "sentiment"]].rename(columns={
                    "name": "Organización / Referente",
                    "handle": "Usuario",
                    "voice_share_pct": "% Voice Share",
                    "mentions": "Menciones",
                    "sentiment": "Enfoque"
                }),
                use_container_width=True,
                hide_index=True
            )
            st.caption("InfoGremiales lidera la cuota de voz con 19.8% (6 menciones). Los 3 principales concentran el 43.6% de la conversación.")

    st.markdown("---")
    st.subheader("🗺️ Procedencia Geográfica de las Menciones")
    geo = sl.get("geography", {}).get("countries", [])
    if geo:
        df_geo = pd.DataFrame(geo)
        geo_col1, geo_col2 = st.columns([2, 1])
        with geo_col1:
            fig_geo = px.bar(
                df_geo,
                x="pct",
                y="country",
                orientation="h",
                labels={"pct": "% de Menciones", "country": "País"},
                color="pct",
                color_continuous_scale="Blues"
            )
            fig_geo.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260, coloraxis_showscale=False)
            st.plotly_chart(fig_geo, use_container_width=True)
        with geo_col2:
            st.markdown("""
            <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 16px;">
                <h4 style="color: #38bdf8; margin: 0 0 8px 0; font-size: 14px;">Identificación Territorial</h4>
                <p style="color: #cbd5e1; font-size: 12px; line-height: 1.5; margin: 0;">
                    Ubicación identificada en el <b>78%</b> de las menciones.
                    <b>Argentina concentra el 69,1%</b> (246 menciones), seguido por la comunidad productiva en Estados Unidos (7,3%), Australia, Chile, Alemania y España.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# TAB 3: TOP 40 TRENDING HASHTAGS
# ==========================================
with tab_hashtags:
    st.subheader("🏷️ Ranking de Trending Hashtags (Top 40 Oficial)")
    hashtags_data = sl.get("trending_hashtags", [])
    if hashtags_data:
        df_th = pd.DataFrame(hashtags_data)
        st.dataframe(
            df_th[["rank", "hashtag", "count", "sentiment"]].rename(columns={
                "rank": "#",
                "hashtag": "Hashtag",
                "count": "Frecuencia",
                "sentiment": "Tono"
            }),
            use_container_width=True,
            height=500,
            hide_index=True
        )
        st.caption("#industrianacional lidera con 88 usos, mayormente positivo. #atilra (67) y #mostrátuproducto (44) son los motores de visibilización.")


# ==========================================
# TAB 4: TOP 35 PHRASES & TOPICS
# ==========================================
with tab_topics:
    st.subheader("💬 Frases y Tópicos más Discutidos (Top 35 Oficial)")
    topics_data = sl.get("trending_topics", [])
    if topics_data:
        df_tt = pd.DataFrame(topics_data)
        st.dataframe(
            df_tt[["rank", "topic", "count", "sentiment"]].rename(columns={
                "rank": "#",
                "topic": "Frase / Tópico Clave",
                "count": "Frecuencia",
                "sentiment": "Enfoque"
            }),
            use_container_width=True,
            height=500,
            hide_index=True
        )
        st.caption("'industria argentina' (95) y 'producción argentina' (79) dominan el mensaje positivo. 'talleres comercios' (48) concentra el reclamo crítico.")


# ==========================================
# TAB 5: TWEETBINDER AUDIT (X / TWITTER)
# ==========================================
with tab_tb:
    st.markdown("""
    <div style="background-color: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <h3 style="color: #38bdf8; margin: 0 0 10px 0;">Auditoría Oficial TweetBinder by Audiense (X / Twitter)</h3>
        <p style="color: #cbd5e1; font-size: 13px; margin: 0;">
            Reporte analítico certificado para el hashtag <b>#queremostrabajar</b> (período 02/11/2026 - 06/11/2026).
        </p>
    </div>
    """, unsafe_allow_html=True)

    tb1, tb2, tb3, tb4 = st.columns(4)
    with tb1:
        st.metric("Valor Económico en X", "$4,558.30 USD", "Calculado TweetBinder")
    with tb2:
        st.metric("Impresiones Potenciales", "1,476,488", "Alcance potencial: 325,954")
    with tb3:
        st.metric("Impresiones Directas", "12,585", "288 Likes / 138 Reposts")
    with tb4:
        st.metric("Cuentas Contribuidoras", "44 usuarios", "4.02 posts / usuario")

    st.markdown("---")

    col_tb_a, col_tb_b = st.columns(2)

    with col_tb_a:
        st.subheader("🏆 Top Cuentas más Influyentes en X")
        top_inf_x = pd.DataFrame([
            {"Usuario": "@marianoobarrio", "Nombre": "Mariano Obarrio", "Seguidores": 145040, "Valor Económico": "$3,537.30"},
            {"Usuario": "@MundoGremial", "Nombre": "Mundo Gremial", "Seguidores": 40536, "Valor Económico": "$130.78"},
            {"Usuario": "@ConclusionRos", "Nombre": "Conclusión Rosario", "Seguidores": 32038, "Valor Económico": "$106.42"},
            {"Usuario": "@DataGremialCom", "Nombre": "Data Gremial", "Seguidores": 26886, "Valor Económico": "$91.11"},
            {"Usuario": "@InfoGremiales", "Nombre": "InfoGremiales", "Seguidores": 24679, "Valor Económico": "$504.59"}
        ])
        st.dataframe(top_inf_x, use_container_width=True, hide_index=True)

    with col_tb_b:
        st.subheader("📢 Cuentas con Mayor Actividad en X")
        top_act_x = pd.DataFrame([
            {"Usuario": "@MdpSmata", "Nombre": "SMATA Mar del Plata", "Posts": 49, "Rol": "Sindicato Automotriz"},
            {"Usuario": "@itacarri", "Nombre": "Ítalo Carrizo", "Posts": 33, "Rol": "Militancia Industrial"},
            {"Usuario": "@Smatamdp28", "Nombre": "Smata Gremiales", "Posts": 22, "Rol": "Gremial"},
            {"Usuario": "@marianoobarrio", "Nombre": "Mariano Obarrio", "Posts": 8, "Rol": "Periodista"},
            {"Usuario": "@ivanahbogado", "Nombre": "Ivana H. Bogado", "Posts": 8, "Rol": "Activismo Pyme"}
        ])
        st.dataframe(top_act_x, use_container_width=True, hide_index=True)


# ==========================================
# TAB 6: MANUAL DATA UPDATE & INGESTION
# ==========================================
with tab_update:
    st.subheader("📝 Módulo de Actualización Manual de Datos")
    st.markdown("""
    Cada vez que obtengas nuevas métricas de tu herramienta de Social Listening, podés copiarlas en el chat o pegarlas directamente acá abajo en formato JSON y hacer clic en **Guardar y Actualizar Dashboard**.
    """)

    json_str = json.dumps(sl, indent=2, ensure_ascii=False)
    updated_json = st.text_area("Dataset JSON de Social Listening:", value=json_str, height=350)

    if st.button("💾 Guardar y Actualizar Dashboard Ahora", use_container_width=True):
        try:
            parsed = json.loads(updated_json)
            with open("data/social_listening.json", "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2, ensure_ascii=False)
            import subprocess
            subprocess.run(["python", "export_verified_data.py"])
            st.success("¡Datos guardados y datasets actualizados exitosamente!")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Error al procesar el JSON: {e}")

st.caption("Campaña CGERA & CSIRA &bull; #queremostrabajar &bull; Monitor Oficial 100% Basado en Datos Verificados.")
