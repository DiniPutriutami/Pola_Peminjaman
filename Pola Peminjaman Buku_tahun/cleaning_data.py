import pandas as pd

class DataCleaner:
    def __init__(self, df):
        self.df = df

    def clean_and_combine_books(self):
        # Combine books for all data
        combined_df = self.df.dropna(subset=['nama_peminjam', 'Judul Buku'])
        combined_df = combined_df.groupby('nama_peminjam')['Judul Buku'].apply(lambda x: self.combine_books(x)).reset_index(name='transaksi')

        # Remove duplicates in transaksi column
        combined_df['transaksi'] = combined_df['transaksi'].apply(lambda x: ', '.join(sorted(set(x.split(', ')))))

        # Split transaksi column into separate columns
        df_transposed = combined_df['transaksi'].str.split(', ', expand=True)
        combined_df = pd.concat([combined_df, df_transposed], axis=1)
        combined_df.drop(columns=['transaksi', 'nama_peminjam'], inplace=True)  # Remove the original 'transaksi' column
        combined_df = combined_df.applymap(lambda x: '' if x is None else x)  # Replace None with empty string

        return combined_df

    def combine_books(self, group):
        unique_books = sorted(set(group))
        cleaned_books = [book.strip().replace("'", '').replace('"', '').replace(',', '') for book in unique_books if book and book.strip() and book != 'None']
        cleaned_books_lower = [book.lower() for book in cleaned_books]  # Convert all book titles to lowercase
        return ', '.join(cleaned_books_lower)
