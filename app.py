import streamlit as st
import pandas as pd
import seaborn as sns
import plotly_express as px
import matplotlib.pyplot as plt
import joblib

# Page configuration
st.set_page_config(
    page_title="Air Quality in Jakarta",
    page_icon="🌡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
url = 'https://raw.githubusercontent.com/CAPSTONEDIGIPRODUCT-KELOMPOK-5/CAPSTONEDIGIPRODUCT_PDAB_KELOMPOK-5/main/Data%20Cleaned%20(4).csv'
df = pd.read_csv(url)

# Sidebar
with st.sidebar:
    st.image('pollution.png', width=260)
    
    st.title('🌡 Air Quality in Jakarta Panel')

    selected_option = st.sidebar.radio('Select an option:', ['Dashboard', 'Visualization', 'Prediction'])

# Dashboard Main Panel
if selected_option == 'Dashboard':

    year_list = sorted(df['year'].unique())
    selected_year = st.sidebar.selectbox('Select a year', year_list)
    df_selected_year = df[df['year'] == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="year", ascending=False)

    st.markdown("<h1 style='text-align: center;'>Analisis Kualitas Udara DKI Jakarta pada Tahun 2019 - 2021</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: justify;'>
        <h3>Explore Air Quality Data</h3>
    </div>
    """, unsafe_allow_html=True)

    # Menampilkan gambar di dashboard
    st.image('https://awsimages.detik.net.id/community/media/visual/2023/05/29/penyebab-polusi-udara-dan-cara-cara-pencegahannya_169.jpeg?w=600&q=90', caption='Polusi ', use_column_width=True)
    
    st.markdown("""
    <div style='text-align: justify;'>
        <p>Gunakan menu dropdown di sidebar untuk memilih tahun yang ingin ditampilkan datanya kualitas udaranya.
        Data ini mencakup parameter polusi yang diukur (pm10, so2, co, o3, no2), parameter polusi yang memiliki skor pengukuran tertinggi, 
        lokasi stasiun pengukuran, dan kategori kualitas udara.</p>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df_selected_year_sorted,
             column_order=["stasiun", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"],
             hide_index=True,
             width=None, 
             height=None 
            )
    selected_year_data = df[df['year'] == selected_year]

    st.markdown("""
    <div style='text-align: justify;'>
        <h3>Understanding the Data</h3>
        
        - Stasiun: Kolom ini berisi nama/lokasi pengukuran kualitas udara. 0 merepresentasikan DKI1 (Bunderan HI), 1 merepresentasikan DKI2 (Kelapa Gading),
                   2 merepresentasikan DKI3 (Jagakarsa), 3 merepresentasikan DKI4 (Lubang Buaya), dan 4 merepresentasikan DKI5 (Kebon Jeruk).
                
        - pm10: Kolom ini berisi partikulat materi dengan diameter < 10 mikrometer, salah satu parameter polusi yang diukur dalam pengukuran kualitas udara
                
        - so2: Kolom ini berisi kadar sulfur dioksida (SO2), salah satu parameter polusi yang diukur dalam pengukuran kualitas udara 
                
        - co: Kolom ini berisi kadar karbon dioksida (CO), salah satu parameter polusi yang diukur dalam pengukuran kualitas udara

        - o3: Kolom ini berisi kadar ozon (O3), salah satu parameter yang diukur dalam pengukuran kualitas udara
                
        - no2: Kolom ini berisi kadar nitrogen dioksida (NO2), salah satu parameter polusi yang diukur dalam pengukuran kualitas udara
                
        - max: Kolom ini berisi nilai tertinggi di antara semua parameter dalam pengukuran kualitas udara
                
        - critical: Kolom ini berisi nama parameter yang memiliki nilai tertinggi di antara semua parameter dalam pengukuran kualitas udara.
                    0 merepresentasikan PM10, 1 merepresentasikan SO2, 2 merepresentasikan CO, 3 merepresentasikan O3, dan 4 merepresentasikan NO2.
                
        - categori: Kolom ini berisi kategori kualitas udara berdasarkan Indeks Standar Polusi Udara dalam pengukuran kualitas udara.
                    0 merepresentasikan baik, 1 merepresentasikan sedang, 2 merepresentasikan tidak sehat, 3 merepresentasikan sangat tidak sehat,
                    dan 4 merepresentasikan berbahaya.
    </div>
    """, unsafe_allow_html=True)

# Distribution Main Panel
if selected_option == 'Visualization':

    selected_option2 = st.sidebar.selectbox('Select a visualization:', ['Distribution', 'Relationship', 'Comparison', 'Composition'])

    if selected_option2 == 'Distribution':

        st.markdown("<h1 style='text-align: center;'>DISTRIBUTION MAIN PANEL</h1>", unsafe_allow_html=True)

        # Visualisasi Histogram (Distribution)
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.countplot(x="categori", data=df, palette='viridis', ax=ax)
        for label in ax.containers:
            ax.bar_label(label)
        plt.title('Persebaran Kategori Kualitas Udara')
        st.pyplot(fig)

        with st.expander('Understanding the Visualization', expanded=True):
            st.write('''
            Visualisasi histogram distribusi/penyebaran kategori kualitas udara dalam dataset "Air Quality Index in Jakarta (2019 - 2021)" menunjukkan frekuensi masing-masing kategori kualitas udara di Jakarta selama periode tersebut. 
            Setiap batang pada histogram mewakili frekuensi masing-masing kategori kualitas udara. Histogram memiliki sumbu-x yang menunjukkan kategori kualitas dan sumbu-y yang menunjukkan jumlah frekuensi setiap kategori.
            Dari visualisasi ini, dapat dilihat bahwa kategori 1 atau "Sedang" memiliki frekuensi tertinggi atau terbanyak yaitu 2.271, diikuti oleh kategori 0 atau "Baik", kategori 2 atau "Tidak sehat", dan kategori 3 atau "Sangat tidak sehat". 
            Ini menunjukkan bahwa sebagian besar waktu selama periode tersebut, kualitas udara di Jakarta dapat dikategorikan sebagai "Sedang". 
            ''')

# Relationship Main Panel
    if selected_option2 == 'Relationship':

        st.markdown("<h1 style='text-align: center;'>RELATIONSHIP MAIN PANEL</h1>", unsafe_allow_html=True)

        # Visualisasi Heatmap (Relationship)
        pollutants = ['max','pm10', 'so2', 'co', 'o3', 'no2']
        corr = df[pollutants].corr()
        fig, ax = plt.subplots(figsize=(10, 8))  # Membuat figure dan axes
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
        plt.title('Korelasi antara Polutan')
        st.pyplot(fig)

        with st.expander('Understanding the Visualization', expanded=True):
            st.write('''
            Visualisasi heatmap relationship atau korelasi antara polutan dan nilai maksimal dalam dataset "Air Quality Index in Jakarta (2019 - 2021)" adalah cara yang efektif untuk memperlihatkan seberapa erat hubungan antara masing-masing polutan dan juga dengan nilai maksimal. 
            Warna setiap sel menunjukkan tingkat korelasi dan arah korelasi antar variabel. Semakin biru (gelap) warna selnya, maka semakin rendah tingkat korelasinya. Sebaliknya, semakin merah (gelap) warna selnya, maka semakin tinggi tingkat korelasinya. 
            Korelasi antara O3 dan nilai maksimal (Max) adalah 0.96, yang menunjukkan hubungan yang sangat kuat. Ini berarti konsentrasi O3 menjadi konsentrasi dengan perhitungan tertinggi (max) pada suatu waktu.
            ''')

# Comparison Main Panel
    if selected_option2 == 'Comparison':

        st.markdown("<h1 style='text-align: center;'>COMPARISON MAIN PANEL</h1>", unsafe_allow_html=True)

        # Visualisasi Stacked Bar
        # Kelompokkan data berdasarkan 'stasiun' dan 'critical' dan hitung jumlahnya
        grouped_data = df.groupby(['stasiun', 'critical']).size().unstack(fill_value=0)
        # Buat stacked bar chart
        fig, ax = plt.subplots(figsize=(14, 8))  # Tingkatkan ukuran figure
        grouped_data.plot(kind='bar', stacked=True, ax=ax, width=0.8)  # Meningkatkan lebar bar
        # Judul dan label
        plt.title('Jumlah Kolom Critical per Stasiun')
        plt.xlabel('Stasiun')
        plt.ylabel('Jumlah')
        # Menampilkan legenda
        plt.legend(title='Critical', loc='upper right')
        # Tambahkan label pada tiap bagian dari stacked bar
        for container in ax.containers:
            ax.bar_label(container, label_type='center', fontsize=8, color='white')  # Kecilkan font dan ubah warna jadi putih
        # Tampilkan plot
        st.pyplot(fig)

        with st.expander('Understanding the Visualization', expanded=True):
            st.write('''
            Visualisasi stacked barplot ini bertujuan untuk menyoroti jumlah polutan terbanyak dalam setiap stasiun dalam dataset "Air Quality Index in Jakarta (2019 - 2021)". 
            Tinggi Stack Bar mewakili jumlah total polutan yang terukur di setiap stasiun. Stasiun 0 merepresentasikan DKI1 (Bunderan HI), Stasiun 1 merepresentasikan DKI2 (Kelapa Gading),
            Stasiun 2 merepresentasikan DKI3 (Jagakarsa), Stasiun 3 merepresentasikan DKI4 (Lubang Buaya), dan Stasiun 4 merepresentasikan DKI5 (Kebon Jeruk).
            Bagian dari Setiap Stack mewakili kontribusi masing-masing polutan terhadap total jumlah polutan di setiap stasiun. 
            Critical 0 merepresentasikan PM10, Critical 1 merepresentasikan SO2, Critical 2 merepresentasikan CO, Critical 3 merepresentasikan O3, dan Critical 4 merepresentasikan NO2. 
            Dalam kasus ini, Critical 3 atau parameter O3 (ozon) rata-rata menjadi parameter terbanyak di setiap stasiun.
            ''')

# Composition Main Panel
    if selected_option2 == 'Composition':

        st.markdown("<h1 style='text-align: center;'>COMPOSITION MAIN PANEL</h1>", unsafe_allow_html=True)

        # Visualisasi Pie Chart
        fig = px.pie(df['categori'].value_counts().reset_index(),
                 names=df['categori'].value_counts().index,
                 values='categori',
                 title='Persentase Kategori Kualitas Udara')
        st.plotly_chart(fig)

        with st.expander('Understanding the Visualization', expanded=True):
            st.write('''
            Visualisasi Pie Chart untuk kategori kualitas udara dalam dataset "Air Quality Index in Jakarta (2019 - 2021)" menunjukkan proporsi persentase masing-masing kategori. 
            Kategori 0 merepresentasikan baik, Kategori 1 merepresentasikan sedang, Kategori 2 merepresentasikan tidak sehat, dan Kategori 3 merepresentasikan sangat tidak sehat.
            Kategori "sangat tidak sehat" memiliki proporsi terbesar dalam kualitas udara Jakarta dengan persentase sebesar 50%. 
            Ini menunjukkan bahwa kualitas udara yang dimonitor berada dalam kategori sangat tidak sehat setengah dari total waktu pengamatan.
            ''')

# Prediction Main Panel
if selected_option == 'Prediction':
        
    st.subheader('Air Quality Cluster Prediction in Jakarta Using KNN Algorithm')

    # Load the model from the .sav file
    knn_clf = joblib.load('knn.sav')
    
    # Get inputs
    stasiun = st.number_input('Stasiun:', min_value=0, max_value=4, value=0)
    pm10 = float(st.number_input('PM10:', value=0.0))
    so2 = float(st.number_input('SO2:', value=0.0))
    co = float(st.number_input('CO:', value=0.0))
    o3 = float(st.number_input('O3:', value=0.0))
    no2 = float(st.number_input('NO2:', value=0.0))
    max = float(st.number_input('Max:', value=0.0))
    critical = st.number_input('Critical:', min_value=0, max_value=4, value=0)
    categori = st.number_input('Categori:', min_value=0, max_value=4, value=0)
    year = st.number_input('Year:', min_value=2019, max_value=2021, value=2019)

    # Create a DataFrame with the input data
    data = pd.DataFrame({
        'stasiun': [stasiun],
        'pm10': [pm10],
        'so2': [so2],
        'co': [co],
        'o3': [o3],
        'no2': [no2],
        'max': [max],
        'critical': [critical],
        'categori': [categori],
        'year': [year]
    })

    # This is how to dynamically change text
    prediction_state = st.markdown('Calculating...')

    # Perform prediction using the loaded model
    y_pred = knn_clf.predict(data)

    # Determine the prediction message based on the predicted label
    if y_pred[0] == 0:
        msg = 'This air quality is in Cluster 0'
    elif y_pred[0] == 1:
        msg = 'This air quality is in Cluster 0'
    elif y_pred[0] == 2:
        msg = 'This air quality is in Cluster 2'
    elif y_pred[0] == 3:
        msg = 'This air quality is in Cluster 3'
    elif y_pred[0] == 4:
        msg = 'This air quality is in Cluster 4'
    elif y_pred[0] == 5:
        msg = 'This air quality is in Cluster 5'
    else:
        msg = 'undefined'

    # Update the prediction state with the message
    prediction_state.markdown(msg)
