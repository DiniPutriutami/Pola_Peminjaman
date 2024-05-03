import pandas as pd

class FacultyDataCleaner:
    def __init__(self, df):
        self.df = df

    def clean_and_combine_books_for_faculty(cleaner, faculty_mapping):
        cleaned_data = {}
        for faculty, keywords in faculty_mapping.items():
            cleaned_data[faculty] = cleaner.clean_and_combine_books(keywords)
        return cleaned_data
    
    def clean_faculty_data(self, faculty_name):
        # Clean data for specific faculty
        cleaned_df = self.df.dropna(subset=['fak_jur'])  # Drop rows with NaN values in 'fak_jur'
        cleaned_df = cleaned_df[cleaned_df['fak_jur'].str.lower().str.contains(faculty_name.lower())]
        return cleaned_df


    def combine_books(self, group):
        unique_books = sorted(set(group))
        cleaned_books = [book.strip().replace("'", '').replace('"', '').replace(',', '') for book in unique_books if book and book.strip() and book != 'None']
        cleaned_books_lower = [book.lower() for book in cleaned_books]  # Mengubah semua judul buku menjadi huruf kecil
        return ', '.join(cleaned_books_lower)



    def clean_and_combine_books(self, faculty_names):
        # Clean and combine books for specific faculty
        cleaned_dfs = []
        for faculty_name in faculty_names:
            if isinstance(faculty_name, str):
                cleaned_df = self.clean_faculty_data(faculty_name)
                cleaned_dfs.append(cleaned_df)

        combined_df = pd.concat(cleaned_dfs) # Combine data for all faculties
        combined_df = combined_df.groupby('nama_peminjam')['Judul Buku'].apply(lambda x: self.combine_books(x)).reset_index(name='transaksi')

        # Remove duplicates in transaksi column
        combined_df['transaksi'] = combined_df['transaksi'].apply(lambda x: ', '.join(sorted(set(x.split(', ')))))

        # Split transaksi column into separate columns
        df_transposed = combined_df['transaksi'].str.split(', ', expand=True)
        combined_df = pd.concat([combined_df, df_transposed], axis=1)
        combined_df.drop(columns=['transaksi', 'nama_peminjam'], inplace=True)  # Remove the original 'transaksi' column
        combined_df = combined_df.applymap(lambda x: '' if x is None else x)  # Replace None with empty string

        return combined_df


