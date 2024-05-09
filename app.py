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
    options = ['Prediksi dengan Algoritma KNN', 'Visualisasi Klaster']
    selected_option3 = st.sidebar.selectbox('Pilih Opsi:', options)


    if selected_option3 == 'Prediksi dengan Algoritma KNN':
        st.markdown("<h1 style='text-align: center;'>Prediksi Klaster Kualitas Udara di Jakarta Menggunakan Algoritma KNN</h1>", unsafe_allow_html=True)

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

    elif selected_option3 == 'Visualisasi Klaster':
        # Menambahkan opsi pemilihan visualisasi
        visualization_option = st.selectbox("Pilih Visualisasi:", ['Distribusi Klaster', 'Komposisi Klaster 0', 'Komposisi Klaster 1', 'Komposisi Klaster 2', 'Komposisi Klaster 3', 'Komposisi Klaster 4', 'Komposisi Klaster 5'])

        if visualization_option == 'Distribusi Klaster':
            st.markdown("<h1 style='text-align: center;'>Visualisasi Distribusi Klaster</h1>", unsafe_allow_html=True)

            df3 = pd.DataFrame(df2)

            kmeans_label_counts = df3['kmeans_label'].value_counts()

            # Membuat warna: biru untuk yang terbanyak, abu-abu untuk lainnya
            colors = ['blue' if i == kmeans_label_counts.index[0] else 'grey' for i in kmeans_label_counts.index]

            # Membuat figure dan axes
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

            # Pie chart
            axes[0].pie(kmeans_label_counts, labels=kmeans_label_counts.index, autopct='%1.1f%%', startangle=140)
            axes[0].set_title('Pie Chart Persentase KMeans Label')

            # Bar chart
            axes[1].bar(kmeans_label_counts.index, kmeans_label_counts.values, color=colors)
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

        elif visualization_option == 'Komposisi Klaster 0':
            # Load data
            url = 'https://raw.githubusercontent.com/Lidiaaprilia/CapstoneDigiProduct-Dataset/main/Cluster%200.csv'
            df_clust0 = pd.read_csv(url)

            # Menampilkan dataframe
            st.subheader('DataFrame Klaster 0')
            st.write(df_clust0)

            # Tampilkan jumlah data
            st.write("Jumlah data Klaster 0:", len(df_clust0))

            # Membagi layout menjadi 2 kolom
            col1, col2 = st.columns(2)

            # Menampilkan bar chart jumlah data per kolom 'stasiun' dan 'critical' di kolom 1
            with col1:
                st.subheader("Visualisasi Jumlah Data per Stasiun dan Critical")

                # Plot stasiun
                fig, ax = plt.subplots()
                stasiun_counts = df_clust0['stasiun'].value_counts()
                bars = stasiun_counts.plot(kind='bar', color=['red', 'grey', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Stasiun')
                ax.set_xlabel('Stasiun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Stasiun: 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
    
                # Plot critical
                fig, ax = plt.subplots()
                critical_counts = df_clust0['critical'].value_counts()
                bars = critical_counts.plot(kind='bar', color=['cyan', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Critical')
                ax.set_xlabel('Critical')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Critical: 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

            # Menampilkan bar chart jumlah data per kolom 'tahun' dan 'categori' di kolom 2
            with col2:
                st.subheader("Visualisasi Jumlah Data per Tahun dan Categori")

                # Plot tahun
                fig, ax = plt.subplots()
                tahun_counts = df_clust0['year'].value_counts()
                bars = tahun_counts.plot(kind='bar', color=['gold', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Tahun')
                ax.set_xlabel('Tahun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
    
                # Plot categori
                fig, ax = plt.subplots()
                categori_counts = df_clust0['categori'].value_counts()
                bars = categori_counts.plot(kind='bar', color=['lightsalmon', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Categori')
                ax.set_xlabel('Categori')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

            # Menghitung rata-rata pm10, so2, co, o3, dan no2
            st.write("Rata-rata parameter polusi:")
            st.write("- Rata-rata PM10:", df_clust0['pm10'].mean())
            st.write("- Rata-rata SO2:", df_clust0['so2'].mean())
            st.write("- Rata-rata CO:", df_clust0['co'].mean())
            st.write("- Rata-rata O3:", df_clust0['o3'].mean())
            st.write("- Rata-rata NO2:", df_clust0['no2'].mean())

            with st.expander('Memahami Visualisasi', expanded=True):
                st.write('''
                * Air Quality Index: [AQI](https://plutusias.com/air-quality-index/).
                *   Berdasarkan hasil rata-rata dari PM10, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari SO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari CO, parameter polusi ini masuk ke dalam kategori AQI 'Buruk'.
                *   Berdasarkan hasil rata-rata dari O3, parameter polusi ini masuk ke dalam kategori AQI 'Cukup tercemar'.
                *   Berdasarkan hasil rata-rata dari NO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Stasiun DKI5 (Kebon Jeruk) menjadi stasiun pengukuran terbanyak diantara stasiun pengukuran lainnya pada cluster 0.
                *   Kategori 'Tidak Sehat' menjadi kategori udara terbanyak diantara kategori udara lainnya pada cluster 0.
                *   Tahun 2019 menjadi tahun pengukuran terbanyak diantara tahun pengukuran lainnya pada cluster 0.
                ''')

        elif visualization_option == 'Komposisi Klaster 1':
            # Load data
            url = 'https://raw.githubusercontent.com/Lidiaaprilia/CapstoneDigiProduct-Dataset/main/Cluster%201.csv'
            df_clust1 = pd.read_csv(url)

            # Menampilkan dataframe
            st.subheader('DataFrame Klaster 1')
            st.write(df_clust1)

            # Tampilkan jumlah data
            st.write("Jumlah data Klaster 1:", len(df_clust1))

            # Membagi layout menjadi 2 kolom
            col1, col2 = st.columns(2)

            # Menampilkan bar chart jumlah data per kolom 'stasiun' dan 'critical' di kolom 1
            with col1:
                st.subheader("Visualisasi Jumlah Data per Stasiun dan Critical")

                # Plot stasiun
                fig, ax = plt.subplots()
                stasiun_counts = df_clust1['stasiun'].value_counts()
                bars = stasiun_counts.plot(kind='bar', color=['red', 'grey', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Stasiun')
                ax.set_xlabel('Stasiun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Stasiun: 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
    
                # Plot critical
                fig, ax = plt.subplots()
                critical_counts = df_clust1['critical'].value_counts()
                bars = critical_counts.plot(kind='bar', color=['cyan', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Critical')
                ax.set_xlabel('Critical')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Critical: 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

            # Menampilkan bar chart jumlah data per kolom 'tahun' dan 'categori' di kolom 2
            with col2:
                st.subheader("Visualisasi Jumlah Data per Tahun dan Categori")

                # Plot tahun
                fig, ax = plt.subplots()
                tahun_counts = df_clust1['year'].value_counts()
                bars = tahun_counts.plot(kind='bar', color=['gold', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Tahun')
                ax.set_xlabel('Tahun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
    
                # Plot categori
                fig, ax = plt.subplots()
                categori_counts = df_clust1['categori'].value_counts()
                bars = categori_counts.plot(kind='bar', color=['lightsalmon', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Categori')
                ax.set_xlabel('Categori')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

            # Menghitung rata-rata pm10, so2, co, o3, dan no2
            st.write("Rata-rata parameter polusi:")
            st.write("- Rata-rata PM10:", df_clust1['pm10'].mean())
            st.write("- Rata-rata SO2:", df_clust1['so2'].mean())
            st.write("- Rata-rata CO:", df_clust1['co'].mean())
            st.write("- Rata-rata O3:", df_clust1['o3'].mean())
            st.write("- Rata-rata NO2:", df_clust1['no2'].mean())

            with st.expander('Memahami Visualisasi', expanded=True):
                st.write('''
                * Air Quality Index: [AQI](https://plutusias.com/air-quality-index/).
                *   Berdasarkan hasil rata-rata dari PM10, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari SO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari CO, parameter polusi ini masuk ke dalam kategori AQI 'Sangat Buruk'.
                *   Berdasarkan hasil rata-rata dari O3, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari NO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Stasiun DKI1 (Bundaran HI) menjadi stasiun pengukuran terbanyak diantara stasiun pengukuran lainnya pada cluster 1.
                *   Kategori 'Sedang' menjadi kategori udara terbanyak diantara kategori udara lainnya pada cluster 1.
                *   Tahun 2019 menjadi tahun pengukuran terbanyak diantara tahun pengukuran lainnya pada cluster 1.
                ''')


        elif visualization_option == 'Komposisi Klaster 2':
            # Load data
            url = 'https://raw.githubusercontent.com/Lidiaaprilia/CapstoneDigiProduct-Dataset/main/Cluster%202.csv'
            df_clust2 = pd.read_csv(url)

            # Menampilkan dataframe
            st.subheader('DataFrame Klaster 2')
            st.write(df_clust2)

            # Tampilkan jumlah data
            st.write("Jumlah data Klaster 2:", len(df_clust2))

            # Membagi layout menjadi 2 kolom
            col1, col2 = st.columns(2)

            # Menampilkan bar chart jumlah data per kolom 'stasiun' dan 'critical' di kolom 1
            with col1:
                st.subheader("Visualisasi Jumlah Data per Stasiun dan Critical")

                # Plot stasiun
                fig, ax = plt.subplots()
                stasiun_counts = df_clust2['stasiun'].value_counts()
                bars = stasiun_counts.plot(kind='bar', color=['red', 'grey', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Stasiun')
                ax.set_xlabel('Stasiun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Stasiun: 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
    
                # Plot critical
                fig, ax = plt.subplots()
                critical_counts = df_clust2['critical'].value_counts()
                bars = critical_counts.plot(kind='bar', color=['cyan', 'grey', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Critical')
                ax.set_xlabel('Critical')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Critical: 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

            # Menampilkan bar chart jumlah data per kolom 'tahun' dan 'categori' di kolom 2
            with col2:
                st.subheader("Visualisasi Jumlah Data per Tahun dan Categori")

                # Plot tahun
                fig, ax = plt.subplots()
                tahun_counts = df_clust2['year'].value_counts()
                bars = tahun_counts.plot(kind='bar', color=['gold', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Tahun')
                ax.set_xlabel('Tahun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
    
                # Plot categori
                fig, ax = plt.subplots()
                categori_counts = df_clust2['categori'].value_counts()
                bars = categori_counts.plot(kind='bar', color=['lightsalmon', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Categori')
                ax.set_xlabel('Categori')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

            # Menghitung rata-rata pm10, so2, co, o3, dan no2
            st.write("Rata-rata parameter polusi:")
            st.write("- Rata-rata PM10:", df_clust2['pm10'].mean())
            st.write("- Rata-rata SO2:", df_clust2['so2'].mean())
            st.write("- Rata-rata CO:", df_clust2['co'].mean())
            st.write("- Rata-rata O3:", df_clust2['o3'].mean())
            st.write("- Rata-rata NO2:", df_clust2['no2'].mean())

            with st.expander('Memahami Visualisasi', expanded=True):
                st.write('''
                * Air Quality Index: [AQI](https://plutusias.com/air-quality-index/).
                *   Berdasarkan hasil rata-rata dari PM10, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari SO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari CO, parameter polusi ini masuk ke dalam kategori AQI 'Berbahaya/Parah'.
                *   Berdasarkan hasil rata-rata dari O3, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari NO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Stasiun DKI5 (Kebon Jeruk) menjadi stasiun pengukuran terbanyak diantara stasiun pengukuran lainnya pada cluster 2.
                *   Kategori 'Sedang' menjadi kategori udara terbanyak diantara kategori udara lainnya pada cluster 2.
                *   Tahun 2020 menjadi tahun pengukuran terbanyak diantara tahun pengukuran lainnya pada cluster 2.
                ''')

        elif visualization_option == 'Komposisi Klaster 3':
            # Load data
            url = 'https://raw.githubusercontent.com/Lidiaaprilia/CapstoneDigiProduct-Dataset/main/Cluster%203.csv'
            df_clust3 = pd.read_csv(url)

            # Menampilkan dataframe
            st.subheader('DataFrame Klaster 3')
            st.write(df_clust3)

            # Tampilkan jumlah data
            st.write("Jumlah data Klaster 3:", len(df_clust3))

            # Membagi layout menjadi 2 kolom
            col1, col2 = st.columns(2)

            # Menampilkan bar chart jumlah data per kolom 'stasiun' dan 'critical' di kolom 1
            with col1:
                st.subheader("Visualisasi Jumlah Data per Stasiun dan Critical")

                # Plot stasiun
                fig, ax = plt.subplots()
                stasiun_counts = df_clust3['stasiun'].value_counts()
                bars = stasiun_counts.plot(kind='bar', color=['red', 'grey', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Stasiun')
                ax.set_xlabel('Stasiun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Stasiun: 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
    
                # Plot critical
                fig, ax = plt.subplots()
                critical_counts = df_clust3['critical'].value_counts()
                bars = critical_counts.plot(kind='bar', color=['cyan', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Critical')
                ax.set_xlabel('Critical')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Critical: 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

            # Menampilkan bar chart jumlah data per kolom 'tahun' dan 'categori' di kolom 2
            with col2:
                st.subheader("Visualisasi Jumlah Data per Tahun dan Categori")

                # Plot tahun
                fig, ax = plt.subplots()
                tahun_counts = df_clust3['year'].value_counts()
                bars = tahun_counts.plot(kind='bar', color=['gold', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Tahun')
                ax.set_xlabel('Tahun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
    
                # Plot categori
                fig, ax = plt.subplots()
                categori_counts = df_clust3['categori'].value_counts()
                bars = categori_counts.plot(kind='bar', color=['lightsalmon', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Categori')
                ax.set_xlabel('Categori')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

            # Menghitung rata-rata pm10, so2, co, o3, dan no2
            st.write("Rata-rata parameter polusi:")
            st.write("- Rata-rata PM10:", df_clust3['pm10'].mean())
            st.write("- Rata-rata SO2:", df_clust3['so2'].mean())
            st.write("- Rata-rata CO:", df_clust3['co'].mean())
            st.write("- Rata-rata O3:", df_clust3['o3'].mean())
            st.write("- Rata-rata NO2:", df_clust3['no2'].mean())

            with st.expander('Memahami Visualisasi', expanded=True):
                st.write('''
                * Air Quality Index: [AQI](https://plutusias.com/air-quality-index/).
                *   Berdasarkan hasil rata-rata dari PM10, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari SO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari CO, parameter polusi ini masuk ke dalam kategori AQI 'Buruk'.
                *   Berdasarkan hasil rata-rata dari O3, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari NO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Stasiun DKI5 (Kebon Jeruk) menjadi stasiun pengukuran terbanyak diantara stasiun pengukuran lainnya pada cluster 3.
                *   Kategori 'Baik' menjadi kategori udara terbanyak diantara kategori udara lainnya pada cluster 3.
                *   Tahun 2020 menjadi tahun pengukuran terbanyak diantara tahun pengukuran lainnya pada cluster 3.
                ''')
            
        elif visualization_option == 'Komposisi Klaster 4':
            # Load data
            url = 'https://raw.githubusercontent.com/Lidiaaprilia/CapstoneDigiProduct-Dataset/main/Cluster%204.csv'
            df_clust4 = pd.read_csv(url)

            # Menampilkan dataframe
            st.subheader('DataFrame Klaster 4')
            st.write(df_clust4)

            # Tampilkan jumlah data
            st.write("Jumlah data Klaster 4:", len(df_clust4))

            # Membagi layout menjadi 2 kolom
            col1, col2 = st.columns(2)

            # Menampilkan bar chart jumlah data per kolom 'stasiun' dan 'critical' di kolom 1
            with col1:
                st.subheader("Visualisasi Jumlah Data per Stasiun dan Critical")

                # Plot stasiun
                fig, ax = plt.subplots()
                stasiun_counts = df_clust4['stasiun'].value_counts()
                bars = stasiun_counts.plot(kind='bar', color=['red', 'grey', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Stasiun')
                ax.set_xlabel('Stasiun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Stasiun: 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
    
                # Plot critical
                fig, ax = plt.subplots()
                critical_counts = df_clust4['critical'].value_counts()
                bars = critical_counts.plot(kind='bar', color=['cyan', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Critical')
                ax.set_xlabel('Critical')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Critical: 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

            # Menampilkan bar chart jumlah data per kolom 'tahun' dan 'categori' di kolom 2
            with col2:
                st.subheader("Visualisasi Jumlah Data per Tahun dan Categori")

                # Plot tahun
                fig, ax = plt.subplots()
                tahun_counts = df_clust4['year'].value_counts()
                bars = tahun_counts.plot(kind='bar', color=['gold', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Tahun')
                ax.set_xlabel('Tahun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
    
                # Plot categori
                fig, ax = plt.subplots()
                categori_counts = df_clust4['categori'].value_counts()
                bars = categori_counts.plot(kind='bar', color=['lightsalmon', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Categori')
                ax.set_xlabel('Categori')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

            # Menghitung rata-rata pm10, so2, co, o3, dan no2
            st.write("Rata-rata parameter polusi:")
            st.write("- Rata-rata PM10:", df_clust4['pm10'].mean())
            st.write("- Rata-rata SO2:", df_clust4['so2'].mean())
            st.write("- Rata-rata CO:", df_clust4['co'].mean())
            st.write("- Rata-rata O3:", df_clust4['o3'].mean())
            st.write("- Rata-rata NO2:", df_clust4['no2'].mean())

            with st.expander('Memahami Visualisasi', expanded=True):
                st.write('''
                * Air Quality Index: [AQI](https://plutusias.com/air-quality-index/).
                *   Berdasarkan hasil rata-rata dari PM10, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari SO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari CO, parameter polusi ini masuk ke dalam kategori AQI 'Buruk'.
                *   Berdasarkan hasil rata-rata dari O3, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari NO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Stasiun DKI2 (Kelapa Gading) menjadi stasiun pengukuran terbanyak diantara stasiun pengukuran lainnya pada cluster 4.
                *   Kategori 'Sedang' menjadi kategori udara terbanyak diantara kategori udara lainnya pada cluster 4.
                *   Tahun 2019 menjadi tahun pengukuran terbanyak diantara tahun pengukuran lainnya pada cluster 4.
                ''')

        elif visualization_option == 'Komposisi Klaster 5':
            # Load data
            url = 'https://raw.githubusercontent.com/Lidiaaprilia/CapstoneDigiProduct-Dataset/main/Cluster%205.csv'
            df_clust5 = pd.read_csv(url)

            # Menampilkan dataframe
            st.subheader('DataFrame Klaster 5')
            st.write(df_clust5)

            # Tampilkan jumlah data
            st.write("Jumlah data Klaster 5:", len(df_clust5))

            # Membagi layout menjadi 2 kolom
            col1, col2 = st.columns(2)

            # Menampilkan bar chart jumlah data per kolom 'stasiun' dan 'critical' di kolom 1
            with col1:
                st.subheader("Visualisasi Jumlah Data per Stasiun dan Critical")

                # Plot stasiun
                fig, ax = plt.subplots()
                stasiun_counts = df_clust5['stasiun'].value_counts()
                bars = stasiun_counts.plot(kind='bar', color=['red', 'grey', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Stasiun')
                ax.set_xlabel('Stasiun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Stasiun: 0 = DKI1 (Bunderan HI), 1 = DKI2 (Kelapa Gading), 2 = DKI3 (Jagakarsa), 3 = DKI4 (Lubang Buaya), dan 4 = DKI5 (Kebon Jeruk).')
    
                # Plot critical
                fig, ax = plt.subplots()
                critical_counts = df_clust5['critical'].value_counts()
                bars = critical_counts.plot(kind='bar', color=['cyan', 'grey', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Critical')
                ax.set_xlabel('Critical')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Critical: 0 = pm10, 1 = so2, 2 = co, 3 = o3, dan 4 = no2.')

            # Menampilkan bar chart jumlah data per kolom 'tahun' dan 'categori' di kolom 2
            with col2:
                st.subheader("Visualisasi Jumlah Data per Tahun dan Categori")

                # Plot tahun
                fig, ax = plt.subplots()
                tahun_counts = df_clust5['year'].value_counts()
                bars = tahun_counts.plot(kind='bar', color=['gold', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Tahun')
                ax.set_xlabel('Tahun')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
    
                # Plot categori
                fig, ax = plt.subplots()
                categori_counts = df_clust5['categori'].value_counts()
                bars = categori_counts.plot(kind='bar', color=['lightsalmon', 'grey', 'grey'], ax=ax)
                ax.set_title('Jumlah per Categori')
                ax.set_xlabel('Categori')
                ax.set_ylabel('Jumlah')
                for bar in bars.patches:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(int(bar.get_height())),
                    ha='center', va='bottom')
                st.pyplot(fig)
                st.caption('Kategori: 0 = baik, 1 = sedang, 2 = tidak sehat, dan 3 = sangat tidak sehat.')

            # Menghitung rata-rata pm10, so2, co, o3, dan no2
            st.write("Rata-rata parameter polusi:")
            st.write("- Rata-rata PM10:", df_clust5['pm10'].mean())
            st.write("- Rata-rata SO2:", df_clust5['so2'].mean())
            st.write("- Rata-rata CO:", df_clust5['co'].mean())
            st.write("- Rata-rata O3:", df_clust5['o3'].mean())
            st.write("- Rata-rata NO2:", df_clust5['no2'].mean())

            with st.expander('Memahami Visualisasi', expanded=True):
                st.write('''
                * Air Quality Index: [AQI](https://plutusias.com/air-quality-index/).
                *   Berdasarkan hasil rata-rata dari PM10, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari SO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Berdasarkan hasil rata-rata dari CO, parameter polusi ini masuk ke dalam kategori AQI 'Buruk'.
                *   Berdasarkan hasil rata-rata dari O3, parameter polusi ini masuk ke dalam kategori AQI 'Memuaskan'.
                *   Berdasarkan hasil rata-rata dari NO2, parameter polusi ini masuk ke dalam kategori AQI 'Baik'.
                *   Stasiun DKI4 (Lubang Buaya) menjadi stasiun pengukuran terbanyak diantara stasiun pengukuran lainnya pada cluster 5.
                *   Kategori 'Sedang' menjadi kategori udara terbanyak diantara kategori udara lainnya pada cluster 5.
                *   Tahun 2020 menjadi tahun pengukuran terbanyak diantara tahun pengukuran lainnya pada cluster 5.
                ''')
