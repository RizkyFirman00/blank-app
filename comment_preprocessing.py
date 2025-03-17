import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class CommentPreprocessing:
    # Inisialisasi stemmer Sastrawi
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    @staticmethod
    def remove_urls(text: str) -> str:
        """Menghapus URL dari teks."""
        return re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    @staticmethod
    def remove_special_characters(text: str) -> str:
        """Menghapus karakter khusus dan angka."""
        return re.sub(r"[^a-zA-Z\s]", "", text)

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        """Menghapus spasi berlebihan."""
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def stemming(cls, text: str) -> str:
        """Melakukan stemming pada teks menggunakan Sastrawi."""
        return cls.stemmer.stem(text)

    @classmethod
    def clean_text(cls, text: str) -> str:
        """Melakukan pembersihan lengkap pada teks."""
        text = text.lower()  # Ubah ke huruf kecil
        text = cls.remove_urls(text)
        text = cls.remove_special_characters(text)
        text = cls.remove_extra_spaces(text)
        text = cls.stemming(text)  # Lakukan stemming
        return text
