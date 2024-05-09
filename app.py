import streamlit as st
import pandas as pd
import seaborn as sns
import plotly_express as px
import matplotlib.pyplot as plt
import joblib

# Page configuration
st.set_page_config(
    page_title="Kualitas Udara di Jakarta",
    page_icon="🌡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
# Without K-Means Label
url = 'https://raw.githubusercontent.com/CAPSTONEDIGIPRODUCT-KELOMPOK-5/CAPSTONEDIGIPRODUCT_PDAB_KELOMPOK-5/main/Data%20Cleaned%20(4).csv'
df = pd.read_csv(url)

# With K-Means Label
url = 'https://raw.githubusercontent.com/CAPSTONEDIGIPRODUCT-KELOMPOK-5/CAPSTONEDIGIPRODUCT_PDAB_KELOMPOK-5/main/Modelling%20(K-Means)%202.csv'
df2 = pd.read_csv(url)

# Sidebar
with st.sidebar:
    st.image('pollution.png')

    st.title('🌡 Panel Kualitas Udara di Jakarta')

    selected_option = st.sidebar.radio('Pilih Opsi:', ['Dasbor', 'Visualisasi', 'Prediksi'])

# Dashboard Main Panel
if selected_option == 'Dasbor':

    year_list = sorted(df['year'].unique())
    selected_year = st.sidebar.selectbox('Pilih Tahun', year_list)
    df_selected_year = df[df['year'] == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="year", ascending=False)

    st.markdown("<h1 style='text-align: center;'>Analisis Kualitas Udara DKI Jakarta pada Tahun 2019 - 2021</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: justify;'>
        <h3>Jelajahi Data Kualitas Udara</h3>
    </div>
    """, unsafe_allow_html=True)

    # Menampilkan gambar di dashboard
    st.image('https://awsimages.detik.net.id/community/media/visual/2023/05/29/penyebab-polusi-udara-dan-cara-cara-pencegahannya_169.jpeg?w=600&q=90', caption='Polusi ', use_column_width=True)
    
    st.markdown("""
    <div style='text-align: justify;'>
        <p>Gunakan menu dropdown di sidebar untuk memilih tahun yang ingin ditampilkan data kualitas udaranya.
        Data ini mencakup parameter polusi yang diukur (pm10, so2, co, o3, no2), parameter polusi yang memiliki skor pengukuran tertinggi (max & critical), 
        lokasi stasiun pengukuran (stasiun), dan kategori kualitas udara (categori).</p>
    </div>
    """, unsafe_allow_html=True)

    # Daftar stasiun yang tersedia secara terurut
    station_options = sorted(df_selected_year_sorted['stasiun'].unique())

    # Daftar kategori yang tersedia secara terurut
    category_options = sorted(df_selected_year_sorted['categori'].unique())

    # Multiselect untuk memilih stasiun
    selected_stations = st.multiselect('Pilih Stasiun', options=station_options, default=station_options)
    st.caption('Stasiun: 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')

    # Multiselect untuk memilih kategori
    selected_categories = st.multiselect('Pilih Kategori', options=category_options, default=category_options)
    st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

    # Filter DataFrame berdasarkan stasiun dan kategori yang dipilih
    filtered_df = df_selected_year_sorted[(df_selected_year_sorted['stasiun'].isin(selected_stations)) & 
                                      (df_selected_year_sorted['categori'].isin(selected_categories))]
    
    # Tampilkan jumlah data
    st.write("Jumlah data:", len(filtered_df))

    # Tampilkan DataFrame yang telah difilter
    st.dataframe(filtered_df,
             column_order=["stasiun", "pm10", "so2", "co", "o3", "no2", "max", "critical", "categori"],
             hide_index=True,
             width=None, 
             height=None 
            )
    
    st.caption('Critical: 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

    st.markdown("""
    <div style='text-align: justify;'>
        <h3>Memahami Data</h3>
        
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
if selected_option == 'Visualisasi':

    selected_option2 = st.sidebar.selectbox('Pilih Visualisasi:', ['Distribusi', 'Korelasi', 'Perbandingan', 'Komposisi'])

    if selected_option2 == 'Distribusi':

        st.markdown("<h1 style='text-align: center;'>PANEL UTAMA DISTRIBUSI</h1>", unsafe_allow_html=True)

        # Visualisasi Histogram (Distribution)
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.countplot(x="categori", data=df, palette='viridis', ax=ax)
        for label in ax.containers:
            ax.bar_label(label)
        plt.title('Persebaran Kategori Kualitas Udara')
        st.pyplot(fig)

        st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

        with st.expander('Memahami Visualisasi', expanded=True):
            st.write('''
            Visualisasi histogram distribusi/penyebaran kategori kualitas udara dalam dataset "Air Quality Index in Jakarta (2019 - 2021)" menunjukkan frekuensi masing-masing kategori kualitas udara di Jakarta selama periode tersebut. 
            Setiap batang pada histogram mewakili frekuensi masing-masing kategori kualitas udara. Histogram memiliki sumbu-x yang menunjukkan kategori kualitas dan sumbu-y yang menunjukkan jumlah frekuensi setiap kategori.
            Dari visualisasi ini, dapat dilihat bahwa kategori 1 atau "Sedang" memiliki frekuensi tertinggi atau terbanyak yaitu 2.271, diikuti oleh kategori 0 atau "Baik", kategori 2 atau "Tidak sehat", dan kategori 3 atau "Sangat tidak sehat". 
            Ini menunjukkan bahwa sebagian besar waktu selama periode tersebut, kualitas udara di Jakarta dapat dikategorikan sebagai "Sedang". 
            ''')

# Relationship Main Panel
    if selected_option2 == 'Korelasi':

        st.markdown("<h1 style='text-align: center;'>PANEL UTAMA KORELASI</h1>", unsafe_allow_html=True)

        # Visualisasi Heatmap (Relationship)
        pollutants = ['max','pm10', 'so2', 'co', 'o3', 'no2']
        corr = df[pollutants].corr()
        fig, ax = plt.subplots(figsize=(10, 8))  # Membuat figure dan axes
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
        plt.title('Korelasi antara Polutan')
        st.pyplot(fig)

        with st.expander('Memahami Visualisasi', expanded=True):
            st.write('''
            Visualisasi heatmap relationship atau korelasi antara polutan dan nilai maksimal dalam dataset "Air Quality Index in Jakarta (2019 - 2021)" adalah cara yang efektif untuk memperlihatkan seberapa erat hubungan antara masing-masing polutan dan juga dengan nilai maksimal. 
            Warna setiap sel menunjukkan tingkat korelasi dan arah korelasi antar variabel. Semakin biru (gelap) warna selnya, maka semakin rendah tingkat korelasinya. Sebaliknya, semakin merah (gelap) warna selnya, maka semakin tinggi tingkat korelasinya. 
            Korelasi antara O3 dan nilai maksimal (Max) adalah 0.96, yang menunjukkan hubungan yang sangat kuat. Ini berarti konsentrasi O3 menjadi konsentrasi dengan perhitungan tertinggi (max) pada suatu waktu.
            ''')

# Comparison Main Panel
    if selected_option2 == 'Perbandingan':

        st.markdown("<h1 style='text-align: center;'>PANEL UTAMA PERBANDINGAN</h1>", unsafe_allow_html=True)

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

        st.caption('Stasiun (lokasi pengukuran kualitas udara): 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
        st.caption('Critical (nama parameter yang memiliki nilai tertinggi): 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

        with st.expander('Memahami Visualisasi', expanded=True):
            st.write('''
            Visualisasi stacked barplot ini bertujuan untuk menyoroti jumlah polutan terbanyak dalam setiap stasiun dalam dataset "Air Quality Index in Jakarta (2019 - 2021)". 
            Tinggi Stack Bar mewakili jumlah total polutan yang terukur di setiap stasiun. Stasiun 0 merepresentasikan DKI1 (Bunderan HI), Stasiun 1 merepresentasikan DKI2 (Kelapa Gading),
            Stasiun 2 merepresentasikan DKI3 (Jagakarsa), Stasiun 3 merepresentasikan DKI4 (Lubang Buaya), dan Stasiun 4 merepresentasikan DKI5 (Kebon Jeruk).
            Bagian dari Setiap Stack mewakili kontribusi masing-masing polutan terhadap total jumlah polutan di setiap stasiun. 
            Critical 0 merepresentasikan PM10, Critical 1 merepresentasikan SO2, Critical 2 merepresentasikan CO, Critical 3 merepresentasikan O3, dan Critical 4 merepresentasikan NO2. 
            Dalam kasus ini, Critical 3 atau parameter O3 (ozon) rata-rata menjadi parameter terbanyak di setiap stasiun.
            ''')

# Composition Main Panel
    if selected_option2 == 'Komposisi':

        st.markdown("<h1 style='text-align: center;'>PANEL UTAMA KOMPOSISI</h1>", unsafe_allow_html=True)

        # Visualisasi Pie Chart
        fig = px.pie(df['categori'].value_counts().reset_index(),
                 names=df['categori'].value_counts().index,
                 values='categori',
                 title='Persentase Kategori Kualitas Udara')
        st.plotly_chart(fig)

        st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

        with st.expander('Memahami Visualisasi', expanded=True):
            st.write('''
            Visualisasi Pie Chart untuk kategori kualitas udara dalam dataset "Air Quality Index in Jakarta (2019 - 2021)" menunjukkan proporsi persentase masing-masing kategori. 
            Kategori 0 merepresentasikan baik, Kategori 1 merepresentasikan sedang, Kategori 2 merepresentasikan tidak sehat, dan Kategori 3 merepresentasikan sangat tidak sehat.
            Kategori "sangat tidak sehat" memiliki proporsi terbesar dalam kualitas udara Jakarta dengan persentase sebesar 50%. 
            Ini menunjukkan bahwa kualitas udara yang dimonitor berada dalam kategori sangat tidak sehat setengah dari total waktu pengamatan.
            ''')

# Prediction Main Panel
if selected_option == 'Prediksi':

    # Option to select the view
    options = ['Prediksi dengan Algoritma KNN', 'Visualisasi Distribusi Klaster']
    selected_option3 = st.sidebar.selectbox('Pilih Opsi', options)


    if selected_option3 == 'Prediksi dengan Algoritma KNN':
        st.subheader('Prediksi Klaster Kualitas Udara di Jakarta Menggunakan Algoritma KNN')

        # Load the model from the .sav file
        knn_clf = joblib.load('knn.sav')
    
        # Get inputs
        stasiun = st.number_input('Stasiun:', min_value=0, max_value=4, value=0)
        st.caption('Stasiun (lokasi pengukuran kualitas udara): 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
        pm10 = float(st.number_input('PM10:', value=0.0))
        so2 = float(st.number_input('SO2:', value=0.0))
        co = float(st.number_input('CO:', value=0.0))
        o3 = float(st.number_input('O3:', value=0.0))
        no2 = float(st.number_input('NO2:', value=0.0))
        max = float(st.number_input('Max:', value=0.0))
        st.caption('Max (nilai parameter tertinggi)')
        critical = st.number_input('Critical:', min_value=0, max_value=4, value=0)
        st.caption('Critical (nama parameter yang memiliki nilai tertinggi): 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')
        categori = st.number_input('Categori:', min_value=0, max_value=4, value=0)
        st.caption('Categori (kategori kualitas udara): 0 = baik, 1 = sedang, 2 = tidak sehat, 3 = sangat tidak sehat, dan 4 = berbahaya.')
        year = st.number_input('Tahun:', min_value=2019, max_value=2021, value=2019)
        st.caption('Tahun (tahun pengukuran kualitas udara)')

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
            msg = 'Data Kualitas Udara ini berada pada Klaster 0'
        elif y_pred[0] == 1:
            msg = 'Data kualitas udara ini berada pada Klaster 1'
        elif y_pred[0] == 2:
            msg = 'Data kualitas udara ini berada pada Klaster 2'
        elif y_pred[0] == 3:
            msg = 'Data kualitas udara ini berada pada Klaster 3'
        elif y_pred[0] == 4:
            msg = 'Data kualitas udara ini berada pada Klaster 4'
        elif y_pred[0] == 5:
            msg = 'Data kualitas udara ini berada pada Klaster 5'
        else:
            msg = 'Tidak ada Data'

        # Update the prediction state with the message
        prediction_state.markdown(msg)

    elif selected_option3 == 'Visualisasi Distribusi Klaster':
        st.subheader('Visualisasi Label Klaster KMeans')

        df3 = pd.DataFrame(df2)
        # Mengurutkan data berdasarkan jumlahnya dari yang terbesar ke yang terkecil
        kmeans_label_counts = df3['kmeans_label'].value_counts().sort_values(ascending=False)

        # Membuat figure dan axes
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

        # Pie chart
        # Memplot dengan data yang sudah diurutkan
        axes[0].pie(kmeans_label_counts, labels=kmeans_label_counts.index, autopct='%1.1f%%', startangle=140)
        axes[0].set_title('Pie Chart Persentase KMeans Label')

        # Bar chart
        axes[1].bar(kmeans_label_counts.index, kmeans_label_counts.values, color='blue')
        axes[1].set_title('Jumlah KMeans Label')
        axes[1].set_xlabel('KMeans Label')
        axes[1].set_ylabel('Jumlah')

        # Menambahkan caption di bawah bar plot
        caption = "Jumlah data masing-masing cluster:"
        for label, count in kmeans_label_counts.items():
                caption += f"\nCluster {label}: {count} data,"

        # Menampilkan plot dan caption di Streamlit
        st.pyplot(fig)
        st.caption(caption)
