import streamlit as st
from apriori import Apriori
import matplotlib.pyplot as plt
from cleaning_data import DataCleaner
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

support_helper = ''' > Support(A) = (Jumlah peminjaman di mana A muncul)/(Total Jumlah peminjam') '''
confidence_helper = ''' > Confidence(A->B) = Support(AUB)/Support(A)') '''

uploaded_file = st.file_uploader("Upload data peminjaman buku perpustakaan Universitas Sriwijaya (.csv file)", type=['csv'], key="file_uploader")

rhs_var = "Confidence: "  # Nilai default untuk rhs_var
try:
    if uploaded_file is not None:
        # Membaca file CSV dengan encoding latin1
        df = pd.read_csv(uploaded_file, encoding='latin1')
        df = df.reset_index(drop=True)
        df.index += 1
        st.write(df)

        # Menghapus kolom 'nim', 'tanggal_pinjam', 'fak_jur', 'call_number'
        df_cleaned = df.drop(columns=['nim', 'tanggal_pinjam', 'fak_jur','call_number'])

        # Create an instance of DataCleaner
        cleaner = DataCleaner(df_cleaned)
        
        # Clean and combine books
        cleaned_df = cleaner.clean_and_combine_books()
        cleaned_df = cleaned_df.reset_index(drop=True)
        cleaned_df.index += 1

        # Save the dataset to a temporary CSV file
        temp_csv_file = "cleaned_data.csv"  # Nama file CSV sementara
        cleaned_df.columns = range(1, len(cleaned_df.columns) + 1)
        cleaned_df.to_csv(temp_csv_file, index=False, header=None)  # Menyimpan DataFrame ke file CSV tanpa indeks

        # Menampilkan hasil
        st.markdown("## Data Transaksi Peminjaman Buku:")
        st.write(cleaned_df)

        st.markdown('---')
        minSup = st.slider(
            "Tentukan Minimum Support Value", 
            min_value=0.000, 
            max_value=1.000, 
            value=0.000, 
            step=0.005,
            format="%.3f",
            help=support_helper
        )

        minCon = st.slider(
            "Tentukan Minimum Confidence Value", 
            min_value=0.000, 
            max_value=1.000, 
            value=0.000, 
            step=0.005,
            format="%.3f",
            help=confidence_helper
        )

        # Proses dataset dengan Apriori
        objApriori = Apriori(minSup, minCon)
        

        itemCountDict, freqSet = objApriori.fit("cleaned_data.csv")
        rules = objApriori.getSpecRules()


        # Mendapatkan data untuk top 3 buku yang paling banyak dipinjam
        top_books_data = {}
        book_codes = {}
        if 1 in freqSet:
            for i, itemset in enumerate(freqSet[1], 1):
                book = list(itemset)[0]  # Asumsikan itemset hanya berisi satu buku
                support = objApriori.getSupport(itemset)
                book_code = f"Judul Buku {i}"  # Membuat kode buku berdasarkan urutan peminjaman
                top_books_data[book_code] = support
                book_codes[book_code] = book  # Menyimpan kode buku dan judulnya

            if top_books_data:
                fig = objApriori.create_bar_chart(top_books_data)
                st.pyplot(fig)
                st.markdown("**Keterangan:**")
                # Tampilkan keterangan hanya untuk buku yang ada di grafik
                sorted_top_books = dict(sorted(top_books_data.items(), key=lambda x: x[1], reverse=True)[:3])
                for code in sorted_top_books.keys():
                    st.markdown(f"{code}: {book_codes[code]}")
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
                st.markdown(f"<span style='color:black'>Support: {support:.3f}</span>", unsafe_allow_html=True)  # Support dengan 3 angka desimal

        st.markdown("## Frequent Rules")
        if rules:
            for key, value in rules.items():
                antecedent = str(list(key[0]))  # Konversi set menjadi string
                consequent = key[1]
                lift_ratio = objApriori.getLiftRatio(frozenset(key[0]), frozenset([key[1]]))  # Hitung lift ratio
                st.markdown(f"<div style='background-color: #efcc00; padding: 10px; border-radius: 5px;'>{antecedent} -> {consequent} (Confidence: {value:.3f}, Lift Ratio: {lift_ratio:.3f})</div>", unsafe_allow_html=True)  # Confidence dan lift dengan 3 angka desimal
        else:
            st.markdown("<span style='color: red; font-size: 26px; font-weight: bold;'><strong>!!Tidak ada Rules yang tercipta!!</strong></span>", unsafe_allow_html=True)

    else:
        st.warning("Silakan unggah file CSV untuk melanjutkan.")
except pd.errors.ParserError:
    st.error("Format file yang diunggah tidak valid. Pastikan file yang diunggah adalah file CSV yang benar.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
