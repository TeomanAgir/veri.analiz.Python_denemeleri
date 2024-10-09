# Modül 1: Veri Seti Yükleme ve Kontrol

import pandas as pd
from tkinter import Tk, filedialog, messagebox


def load_data():
    # Kullanıcıdan dosya seçmesini iste
    root = Tk()
    root.withdraw()  # Tkinter arayüzünü gizle
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])

    if file_path:
        # Dosya türünü kontrol et ve uygun olanı yükle
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            messagebox.showerror("Hata", "Lütfen CSV veya Excel dosyası seçin.")
            return None

        return df
    else:
        messagebox.showinfo("Bilgi", "Dosya seçimi iptal edildi.")
        return None


# Test için
if __name__ == "__main__":
    df = load_data()
    if df is not None:
        print("Veri seti başarıyla yüklendi.")
        print(df.head())
    else:
        print("Veri seti yüklenemedi.")

# Modül 2: Veri Tipi Seçimi ve Analiz

import tkinter as tk

class DataAnalyzerApp(tk.Tk):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.title("Veri Analiz Uygulaması")

        # Veri tipi seçimi için bir dropdown menü
        self.var = tk.StringVar(self)
        self.var.set("Veri Tipi Seçin")  # Varsayılan değer

        self.dropdown = tk.OptionMenu(self, self.var, "FATURA_TURU", "eFaturaSenaryosu", "Gelir/Gider", command=self.analyze_data)
        self.dropdown.pack()

    def analyze_data(self, selected_type):
        # Seçilen veri tipine göre analiz yap
        if selected_type == "FATURA_TURU":
            self.analyze_fatura_turu()
        elif selected_type == "eFaturaSenaryosu":
            self.analyze_efatura_senaryo()
        elif selected_type == "Gelir/Gider":
            self.analyze_gelir_gider()

    def analyze_fatura_turu(self):
        # Burada FATURA_TURU analizi yapılacak
        print("FATURA_TURU analizi yapılıyor...")
        print(self.df['FATURA_TURU'].value_counts())

    def analyze_efatura_senaryo(self):
        # Burada eFaturaSenaryosu analizi yapılacak
        print("eFaturaSenaryosu analizi yapılıyor...")
        print(self.df['eFaturaSenaryosu'].value_counts())

    def analyze_gelir_gider(self):
        # Burada Gelir/Gider analizi yapılacak
        print("Gelir/Gider analizi yapılıyor...")
        print(self.df[['Gelir', 'Gider']].sum())

# Test için
if __name__ == "__main__":
    df = load_data()
    if df is not None:
        app = DataAnalyzerApp(df)
        app.mainloop()
    else:
        print("Veri seti yüklenemedi, analiz yapılamıyor.")
