import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_excel('altin_dolar_euro_prophet.xlsx')

df.rename(columns={'ds':'date'}, inplace=True)

df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
st.set_page_config(page_title='Investuul', layout='wide', page_icon='wallet')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: url("https://media.giphy.com/media/ND6xkVPaj8tHO/giphy.gif?cid=790b7611chs91yhu66nu36dqdg3xedci7g80pltdz08wktxm&ep=v1_gifs_search&rid=giphy.gif&ct=g");
        background-size: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #E0EDF9; 
        background-image: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit başlatma
#st.sidebar.title('Navigation')
#page = st.sidebar.radio('Go to', ['Anasayfa', 'Time Series Forecasting', 'Investuul'])

with st.sidebar:
    selected = option_menu(
        menu_title= None,
        options=['Anasayfa','Time Series Forecasting', 'Investuul'],
        icons= ['house','activity','eye']
    )

def calculation_yatirim(tutar, dataframe, vade, column):
    today = datetime.today().strftime('%Y-%m-%d')
    today_tutar = dataframe[dataframe['date'] == today][column].values[0]
    yatirim = tutar / today_tutar

    vadeli_tarih = datetime.strptime(today, '%Y-%m-%d') + timedelta(days=vade)
    vadeli_tarih_str = vadeli_tarih.strftime('%Y-%m-%d')

    vadeli_degeri = dataframe[dataframe['date'] == vadeli_tarih_str][column].values[0]
    vadeli_yatirim = yatirim * vadeli_degeri

    return vadeli_yatirim

if selected == 'Anasayfa':
    st.title(':green[Yatırım Rehberi]')
    st.write('Bu uygulama, yatırım yapmayı planladığınız tutar ve vade süresine göre dolar, euro veya altın arasında en kârlı yatırım seçeneğini önerir.')
    st.divider()
    st.subheader(':orange[Modelin Amacı]')
    st.markdown('''
    - Yatırım seçeneklerinin karşılaştırılması ve en kârlı seçeneğin belirlenmesi.
    - Gelecekteki fiyat hareketlerini tahmin ederek yatırım kararlarının desteklenmesi.
    ''')

    st.subheader(':orange[Veri Hakkında]')
    st.markdown('''
    - Kullanılan veri seti: 01-01-2019 - 30-06-2024 tarihleri arasındaki günlük dolar, euro ve altın fiyatları.
    - Tahmin aracı: FbProphet modeli.
    - Tahmin süresi: Gelecek 12 ayı günlük olarak tahminler.''')

    st.subheader(':orange[Yatırım Hakkında]')
    st.markdown('''
    - Dolar 
        - *Küresel rezerv para birimi, yüksek likidite, ekonomik ve politik olaylardan etkilenir.*
        - *Güçlü ABD ekonomisi, kriz dönemlerinde güvenli liman.*
        - *FED faiz oranları, enflasyon, küresel ticaret.*
    ''')
    st.markdown('''
        - Euro 
            - *Avrupa Birliği'nin ortak para birimi, bölgesel ekonomik sağlığa bağlı.*
            - *Enflasyon/deflasyon oranları, bölgesel ekonomik krizler.*
            - *ECB politikaları, ekonomik veriler, siyasi gelişmeler.*
        ''')
    st.markdown('''
            - Altın 
                - *Değer saklama aracı, yüksek likidite, enflasyona karşı koruma.*
                - *Dalgalanma, kriz dönemlerinde artış.*
                - *Enflasyon, faiz oranları, küresel olaylar.*
            ''')


elif selected == 'Time Series Forecasting':
    st.title(':rainbow[Time Series Forecasting]')
    st.subheader(':orange[Veri hakkında:]')
    st.markdown('''
        - 2019 - 2024 yıllarının günlük olarak Dolar, Euro ve Altın tutarlarının TL karşılıklarıyla Prophet modeli geliştirilmiştir.
            - *Modelde yıllık ve haftalık seasonality bulunmaktadır.*
            - *Haftasonları borsalar kapalı olduğundan dolayı veriler boş gelmiştir. Veride boş olarak gelen haftasonları bir önceki cuma gününün değerleriyle doldurulmuştur.*
        ''')

    st.write('*Verinin satır, sütun sayısı:* ',df.shape)
    st.write('*Verideki sütunların yapısı: *',df.dtypes)
    st.write('*Veride bulun boş satırlar:*',df.isnull().sum())
    st.write('*Verilerin dağılımı*',df.quantile([0, 0.05, 0.50, 0.75, 0.95, 0.99, 1]))
    st.write(':green[Verideki minimum tarih:]', df['date'].min())
    st.write(':green[Verideki maximum tarih:]', df['date'].max())
    st.write('*Verinin dağılımı:*', df.describe())
    st.write('*Verideki ilk 5 satır:* ', df.head())
    st.write('*Verideki son 5 satır:*', df.tail())

    st.divider()

    st.subheader(':orange[Tarih Aralığını Seçin]')
    start_date = st.date_input('*Başlangıç Tarihi*', df['date'].min())
    end_date = st.date_input('*Bitiş Tarihi*', df['date'].max())
    filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
    st.subheader(':orange[*Dolar, Euro ve Altın Değerleri*]')
    fig, ax = plt.subplots(3, 1, figsize=(10, 15))

    sns.lineplot(data=filtered_df, x='date', y='dolar', ax=ax[0], color='green')
    ax[0].set_title('Günlük Dolar Değerleri')
    ax[0].set_xlabel('Tarih')
    ax[0].set_ylabel('USD')

    sns.lineplot(data=filtered_df, x='date', y='euro', ax=ax[1], color='blue')
    ax[1].set_title('Günlük Euro Değerleri')
    ax[1].set_xlabel('Tarih')
    ax[1].set_ylabel('EUR')

    sns.lineplot(data=filtered_df, x='date', y='altin', ax=ax[2], color='orange')
    ax[2].set_title('Günlük Altın Değerleri')
    ax[2].set_xlabel('Tarih')
    ax[2].set_ylabel('Altın')

    plt.tight_layout()
    st.pyplot(fig)

    # Ek açıklamalar
    st.markdown('''
    ### :orange[Grafikleri İnceleyin]
    - :grey[Yukarıdaki grafikler, seçtiğiniz tarih aralığındaki dolar, euro ve altın değerlerini göstermektedir.]
    - :grey[Grafikler, yatırım araçlarının zaman içindeki performansını görsel olarak karşılaştırmanıza olanak tanır.]
    - :grey[Tarih aralığını değiştirerek belirli dönemlerdeki performansları inceleyebilirsiniz.]
    ''')

elif selected == 'Investuul':
    st.title(':green[Investuul]')
    st.write('''*Gireceğiniz yatırım tutarına göre bugünün değeri ele alınarak Dolar, Euro ya da Altın 
    alınırsa seçtiğiniz vadeye sonunda yatırım araçlarından hangisinin daha kârlı olduğunun bilgisini 
    görebileceksiniz.*''')


    tutar = st.number_input('Yatırım tutarını giriniz:', min_value=0, step=1000)
    vade = st.selectbox('Vade süresini seçiniz (ay olarak):', [i for i in range(1, 12)])

    if st.button('Hesapla'):
        vade_gun = vade * 30  # Ayı gün sayısına çeviriyoruz

        dolar_sonuc = calculation_yatirim(tutar, df, vade_gun, 'dolar')
        euro_sonuc = calculation_yatirim(tutar, df, vade_gun, 'euro')
        altin_sonuc = calculation_yatirim(tutar, df, vade_gun, 'altin')

        yatirim_sonuclari = {
            "Altin": altin_sonuc,
            "Dolar": dolar_sonuc,
            "Euro": euro_sonuc
        }

        en_karli_yatirim = max(yatirim_sonuclari, key=yatirim_sonuclari.get)
        en_karli_yatirim_degeri = yatirim_sonuclari[en_karli_yatirim]

        st.write(f'{vade} ay sonrası yatırımlarınızın değeri:')
        st.write(f":green[Dolar $: {dolar_sonuc:.2f}]")
        st.write(f":blue[Euro £: {euro_sonuc:.2f}]")
        st.write(f":orange[Altın: {altin_sonuc:.2f}]")

        st.divider()

        st.write(f"*En kârlı yatırım aracı:* {en_karli_yatirim}")
        st.write(f"*En kârlı yatırımın değeri:* {en_karli_yatirim_degeri:.2f}")

        color_mapping = {
            "Dolar": 'green',
            "Euro": 'blue',
            "Altin": 'orange'
        }
        color = color_mapping[en_karli_yatirim]

        # Grafik oluşturma
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df[df['date'] >= '2024-01-01'], x='date', y=en_karli_yatirim.lower(), ax=ax, color=color)
        ax.set_title(f'{en_karli_yatirim} Değerleri')
        ax.set_xlabel('Tarih')
        ax.set_ylabel(en_karli_yatirim)

        st.pyplot(fig)

        st.caption('*Öncelikle yatırım tavsiyesi değildir*')
        st.caption('*Sadece biraz time series forecasting denemesi*')

