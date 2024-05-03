import streamlit as st
from apriori import Apriori, create_bar_chart
from cleaning_data import FacultyDataCleaner
from PIL import Image
import pandas as pd

st.markdown("## Penentuan Pola peminjaman Buku Perpustakaan Universitas Sriwijaya Palembang dan Indralaya Menggunakan Algoritma Apriori")
logo_image = Image.open("logo unsri.png")
st.sidebar.image(logo_image, use_column_width=True)
st.sidebar.markdown(
    """Universitas Sriwijaya

> # ABOUT:
1.    Menghasilkan sistem untuk mengetahui bagaimana implementasi aturan asosiasi data mining yang baik untuk data peminjaman buku di perpustakaan Universitas Sriwijaya Palembang dan Indralaya untuk tujuan analisis.
2.    Mengetahui data peminjaman buku perpustakaan yang sering muncul sehingga dapat memenuhi batasan- batasan yang ditentukan untuk tujuan menghasilkan rekomendasi yang baik terhadap kecenderungan peminjaman buku berdasarkan data mining.
3.    Mengetahui kinerja Algoritma Apriori untuk menentukan frekuensi tinggi dalam menganalisis pola peminjaman buku di perpustakaan Universitas Sriwijaya Palembang dan Indralaya."""
)
st.sidebar.markdown("---")
st.sidebar.markdown("## Evaluasi")

st.sidebar.markdown('''
    **Support** menunjukkan transaksi dengan item yang dibeli bersamaan dalam satu transaksi.
    
    **Nilai Minimal Support:** Nilai ini sebaiknya dipilih sedemikian rupa sehingga hanya itemset yang relevan atau menarik bagi analisis yang disertakan. Jika nilai support terlalu rendah, maka banyak itemset yang muncul dalam hasil, yang mungkin sulit untuk diinterpretasikan. Nilai yang umum digunakan adalah sekitar 1% hingga 5% dari jumlah total transaksi.
    
    **Confidence** menunjukkan transaksi di mana barang dibeli satu demi satu.
    
    **Nilai Minimum Confidence:** Nilai ini sebaiknya dipilih agar aturan yang dihasilkan cukup kuat untuk digunakan dalam pengambilan keputusan. Nilai confidence yang tinggi (misalnya, di atas 70% atau 80%) umumnya dianggap baik, tetapi Anda juga perlu mempertimbangkan konteks spesifik dari analisis Anda.
''')

st.sidebar.markdown('Support and Confidence terhadap Itemsets A and B dapat diwakili oleh rumus berikut:')
st.sidebar.markdown('> Support(A) = (Jumlah transaksi di mana A muncul)/(Total Jumlah Transaksi)') 
st.sidebar.markdown('> Confidence(A->B) = Support(AUB)/Support(A)')

support_helper = ''' > Support(A) = (Number of transactions in which A appears)/(Total Number of Transactions') '''
confidence_helper = ''' > Confidence(A->B) = Support(AUB)/Support(A)') '''

uploaded_file = st.file_uploader("Upload data peminjaman buku perpustakaan Universitas Sriwijaya (.csv file)", type=['csv'])

rhs_var = "Confidence: "  # Nilai default untuk rhs_var

if uploaded_file is not None:
    # Membaca file CSV dengan encoding latin1
    df = pd.read_csv(uploaded_file, encoding='latin1')
    st.write(df)

    # Menghapus kolom 'nim', 'tanggal_pinjam', 'fak_jur', 'call_number'
    df_cleaned = df.drop(columns=['nim', 'tanggal_pinjam', 'call_number'])

    # Create an instance of FacultyDataCleaner
    cleaner = FacultyDataCleaner(df_cleaned)
    
    # Clean and combine books
    faculty_mapping = {
    "Fakultas Ekonomi": ["fe", "ekonomi"],
    "Fakultas Hukum": ["fh", "hukum"],
    "Fakultas Kedokteran": ["fk", "kedokteran"],
    "Fakultas Teknik": ["ft", "teknik"],
    "Fakultas Pertanian": ["fp", "pertanian"],
    "Fakultas Keguruan dan Ilmu Pendidikan": ["fkip", "keguruan"],
    "Fakultas Ilmu Sosial dan Ilmu Politik": ["fisip", "sosial"],
    "Fakultas Matematika dan Ilmu Pengetahuan Alam": ["fmipa", "alam"],
    "Fakultas Ilmu Komputer": ["fasilkom", "komputer"],
    "Fakultas Kesehatan Masyarakat": ["fkm", "masyarakat"]
    }

    # Menampilkan multiselect dengan nama fakultas
    # Menampilkan multiselect dengan nama fakultas
    selected_faculties = st.multiselect("Pilih Fakultas", list(faculty_mapping.keys()))

    if not selected_faculties:
        st.warning("!!Pilih fakultas terlebih dahulu!! ")
    else:
        # Menggunakan kata kunci untuk filtering data
        keywords = [keyword for faculty in selected_faculties for keyword in faculty_mapping[faculty]]
        cleaned_df = cleaner.clean_and_combine_books(keywords)
        # Save the dataset to a temporary CSV file
        temp_csv_file = "cleaned_data.csv"  # Nama file CSV sementara
        cleaned_df.to_csv(temp_csv_file, index=False, header=None)  # Menyimpan DataFrame ke file CSV tanpa indeks

        # Menampilkan hasil
        st.markdown("## Data yang telah dibersihkan:")
        st.write(cleaned_df)

        st.markdown('---')
        minSup = st.slider("Tentukan Minimum Support Value", min_value=0.1,
                        max_value=1.0, value=0.0,
                        help=support_helper)

        minCon = st.slider("Tentukan Minimum Confidence Value", min_value=0.0,
                        max_value=1.00, value=0.0, help=confidence_helper)
        

        # Proses dataset dengan Apriori
        objApriori = Apriori(minSup, minCon)
    

        itemCountDict, freqSet = objApriori.fit("cleaned_data.csv")
        rules = objApriori.getSpecRules()


        # Mendapatkan data untuk top 5 buku yang paling banyak dipinjam
        top_books_data = {}
        if 1 in freqSet:
            for itemset in freqSet[1]:
                book = list(itemset)[0]  # Asumsikan itemset hanya berisi satu buku
                support = objApriori.getSupport(itemset)
                top_books_data[book] = support

            if not top_books_data:
                st.markdown("<span style='color: red; font-size: 24px; font-weight: bold;'><strong>!!Tidak ada Grafik item yang memenuhi nilai support yang diberikan!!</strong></span>", unsafe_allow_html=True)
            else:
                st.markdown("#### Grafik Peminjaman Buku Perpustakaan Universitas Sriwijaya")
                fig = create_bar_chart(top_books_data)
                st.pyplot(fig)
        else:
            st.markdown("<span style='color: red; font-size: 24px; font-weight: bold;'><strong>!!Tidak ada Grafik Peminjaman Buku Perpustakaan Universitas Sriwijaya yang memenuhi nilai support yang diberikan!!</strong></span>", unsafe_allow_html=True)

        st.markdown("# **HASIL**")
        # Menampilkan item terbanyak di freq 1 term set
        for key, value in freqSet.items():
            st.markdown(f"### Frequent {key}-term set:")
            for itemset in value:
                itemset_list = list(itemset)
                support = objApriori.getSupport(itemset)
                st.markdown(f"<span style='color:#ff7f00'>{itemset_list}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:black'>Support: {support}</span>", unsafe_allow_html=True)

        st.markdown("## Frequent Rules")
        if rules:
            for key, value in rules.items():
                antecedent = str(list(key[0]))  # Konversi set menjadi string
                consequent = value
                st.markdown(f"<div style='background-color: #efcc00; padding: 10px; border-radius: 5px;'>{antecedent} -> {key[1]} (Confidence: {consequent})</div>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: red; font-size: 26px; font-weight: bold;'><strong>!!Tidak ada Rules yang tercipta!!</strong></span>", unsafe_allow_html=True)