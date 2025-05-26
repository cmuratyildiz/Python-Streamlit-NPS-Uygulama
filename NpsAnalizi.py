import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Streamlit ile NPS Analizi Uygulaması")

uploaded_file = st.file_uploader("CSV dosyanızı yükleyin", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Yüklenen Veri")
    st.dataframe(df)

    def classify(score):
        if score >= 9:
            return 'Promoter'
        elif score >= 7:
            return 'Passive'
        else:
            return 'Detractor'

    df['NPS_Kategorisi'] = df['NPS'].apply(classify)

    def nps_score(score):
        if score >= 9:
            return 100
        elif score >= 7:
            return 0
        else:
            return -100

    df['NPS_Puan'] = df['NPS'].apply(nps_score)

    st.subheader("Sınıflandırılmış Veri")
    st.dataframe(df)

    genel_nps = df['NPS_Puan'].mean()
    st.metric(label="Genel NPS Skoru", value=round(genel_nps, 2))

    st.subheader("Market Bazlı NPS Skorları")
    market_nps = df.groupby('Market')['NPS_Puan'].mean().reset_index()
    st.dataframe(market_nps)

    st.subheader("NPS Kategori Dağılımı")
    kategori_sayilari = df['NPS_Kategorisi'].value_counts().reset_index()
    kategori_sayilari.columns = ['Kategori', 'Adet']

    fig = px.bar(kategori_sayilari, x='Kategori', y='Adet', text='Adet', color='Kategori',
                 color_discrete_map={'Promoter': 'green', 'Passive': 'gray', 'Detractor': 'red'})
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


    st.subheader("CSV olarak dışarı aktar!")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Güncellenmiş CSV dosyasını indir",
        data=csv,
        file_name='guncellenmis_dosya.csv',
        mime='text/csv',
    )

    st.subheader("XLS olarak dışarı aktar!")
    xls = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Güncellenmiş XLS dosyasını indir",
        data=xls,
        file_name='guncellenmis_dosya.xls',
        mime='text/xls',
    )