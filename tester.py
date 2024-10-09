
import pandas as pd
import numpy as np
import os
from openpyxl import Workbook
import psutil
import time

def the_all_mighty():
    # Veriyi oku
    veri_yolu = 'C:/Users/teoma/Desktop/BilsoftFaturalar.xlsx'
    df = pd.read_excel(veri_yolu)

    # Gerekli sütunları seç ve veri tiplerini düzenle
    df = df[['FAT_TARIH', 'TOPLAM', 'KDV', 'ALINAN', 'eFaturaSenaryo', 'FATURA_TURU']]

    # Virgül ve noktaları düzelt
    df['TOPLAM'] = df['TOPLAM'].astype(str).str.replace(',', '.').astype(float)
    df['KDV'] = df['KDV'].astype(str).str.replace(',', '.').astype(float)
    df['ALINAN'] = df['ALINAN'].astype(str).str.replace(',', '.').astype(float)

    # Tarih sütununu datetime tipine çevir
    df['FAT_TARIH'] = pd.to_datetime(df['FAT_TARIH'], dayfirst=True)

    # Gün, Ay ve Yıl sütunlarını ekle
    df['Gün'] = df['FAT_TARIH'].dt.day
    df['Ay'] = df['FAT_TARIH'].dt.month
    df['Yıl'] = df['FAT_TARIH'].dt.year

    # Ay isimlerini ekle
    ay_isimleri = {1: 'Ocak', 2: 'Şubat', 3: 'Mart', 4: 'Nisan', 5: 'Mayıs', 6: 'Haziran', 7: 'Temmuz', 8: 'Ağustos',
                   9: 'Eylül', 10: 'Ekim', 11: 'Kasım', 12: 'Aralık'}
    df['Ay İsmi'] = df['Ay'].map(ay_isimleri)

    temiz_df = df.copy()

    # Temizlenmiş veri setini kaydetmeden önce "ÖDEME" sütununu ekleyin
    temiz_df['ÖDEME'] = np.where(temiz_df['TOPLAM'] == temiz_df['ALINAN'], 'Tamamlandı', 'Eksik')

    temiz_df = temiz_df.drop(columns= ['FAT_TARIH'])

    x = temiz_df.pop('Gün')
    temiz_df.insert(0, 'Gün', x)
    y = temiz_df.pop('Ay')
    temiz_df.insert(0, 'Ay', y)
    z = temiz_df.pop('Yıl')
    temiz_df.insert(0, 'Yıl', z)

#-----------------------------------
    # Günlük analizler için veri çerçevesini gruplandır ve özetle
    gunluk_ozet = temiz_df.groupby(['Yıl', 'Ay', 'Gün']).agg({
        'TOPLAM': 'sum',
        'KDV': 'sum',
        'ALINAN': 'sum'
    }).reset_index()

    # Gelir, gider ve iptalleri hesapla
    gelir = temiz_df[temiz_df['FATURA_TURU'] == 'SATIŞ FATURASI'].groupby(['Yıl', 'Ay', 'Gün'])[
        'TOPLAM'].sum().reset_index(
        name='Gelir')
    iptal = temiz_df[temiz_df['FATURA_TURU'].isin(['İPTAL', 'İPTAL SATIŞ FATURASI'])].groupby(['Yıl', 'Ay', 'Gün'])[
        'TOPLAM'].sum().reset_index(
        name='İptal')
    gider = temiz_df[temiz_df['FATURA_TURU'] == 'ALIŞ FATURASI'].groupby(['Yıl', 'Ay', 'Gün'])[
        'TOPLAM'].sum().reset_index(
        name='Gider')

    # Günlük özet veri setini birleştir
    gunluk_ozet = gunluk_ozet.merge(gelir, on=['Yıl', 'Ay', 'Gün'], how='left')
    gunluk_ozet = gunluk_ozet.merge(iptal, on=['Yıl', 'Ay', 'Gün'], how='left')
    gunluk_ozet = gunluk_ozet.merge(gider, on=['Yıl', 'Ay', 'Gün'], how='left')

    # Null değerleri 0 ile değiştir
    gunluk_ozet.fillna(0, inplace=True)

    # Günlük özet veri setini kaydet
    gunler_df = gunluk_ozet.copy()

    # Günlük özet veri setini kaydetmeden önce "ÖDEME" sütununu ekleyin
    gunler_df['ÖDEME'] = np.where(gunler_df['TOPLAM'] == gunler_df['ALINAN'], 'Tamamlandı', 'Eksik')

#--------------------------------------------------
    # Aylık verileri gruplandır ve özetle
    aylik_ozet = temiz_df.groupby(['Yıl', 'Ay']).agg({
        'TOPLAM': 'sum',
        'KDV': 'sum',
        'ALINAN': 'sum'
    }).reset_index()

    aylik_ozet['İşlem Yapılan Gün Sayısı'] = temiz_df.groupby(['Yıl', 'Ay'])['Gün'].nunique().values
    # Gelir, gider ve iptalleri hesapla
    aylik_gelir = temiz_df[temiz_df['FATURA_TURU'] == 'SATIŞ FATURASI'].groupby(['Yıl', 'Ay'])['TOPLAM'].sum().reset_index(
        name='Gelir')
    aylik_iptal = temiz_df[temiz_df['FATURA_TURU'].isin(['İPTAL SATIŞ FATURASI','İPTAL'])].groupby(['Yıl', 'Ay'])['TOPLAM'].sum().reset_index(
        name='İptal')
    aylik_gider = temiz_df[temiz_df['FATURA_TURU'] == 'ALIŞ FATURASI'].groupby(['Yıl', 'Ay'])['TOPLAM'].sum().reset_index(
        name='Gider')

    # Aylık özet veri setini birleştir
    aylik_ozet = aylik_ozet.merge(aylik_gelir, on=['Yıl', 'Ay'], how='left')
    aylik_ozet = aylik_ozet.merge(aylik_iptal, on=['Yıl', 'Ay'], how='left')
    aylik_ozet = aylik_ozet.merge(aylik_gider, on=['Yıl', 'Ay'], how='left')

    # Null değerleri 0 ile değiştir
    aylik_ozet.fillna(0, inplace=True)

    aylik_faturalar = pd.pivot_table(temiz_df, values='TOPLAM', index=['Yıl', 'Ay'], columns=['FATURA_TURU'],
                                          aggfunc='count', fill_value=0).reset_index()
    aylik_senaryolar = pd.pivot_table(temiz_df, values='TOPLAM', index=['Yıl', 'Ay'], columns=['eFaturaSenaryo'],
                                          aggfunc='count', fill_value=0).reset_index()
    # Aylık özet veri setini kaydet
    aylar_df = aylik_ozet.copy()

    # Aylık özet veri setini kaydetmeden önce "ÖDEME" sütununu ekleyin
    aylar_df['ÖDEME'] = np.where(aylar_df['TOPLAM'] == aylar_df['ALINAN'], 'Tamamlandı', 'Eksik')

    # Sayı formatlarını ayarla
    pd.options.display.float_format = '{:,.2f}'.format
# #---------------------------------------------------------------------------------------EXCEL

    # Masaüstü yolunu bulma
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # Yeni bir Excel dosyası oluşturma
    workbook = Workbook()
    sheet = workbook.active
    # Excel dosyasını masaüstüne kaydetme
    file_path = os.path.join(desktop, "ciktilar.xlsx")
    workbook.save(file_path)
    print(f"Excel dosyası başarıyla oluşturuldu: {file_path}")
    excel_dosyasi = file_path

    with pd.ExcelWriter(excel_dosyasi) as writer:
        temiz_df.to_excel(writer, sheet_name='Temiz Veri', index=False)
        gunler_df.to_excel(writer, sheet_name='Gunler', index=False)
        aylar_df.to_excel(writer, sheet_name='Aylar', index=False)
        aylik_faturalar.to_excel(writer, sheet_name='Aylik_Faturalar', index=False)
        aylik_senaryolar.to_excel(writer, sheet_name='Aylik_Senaryolar', index=False)

    os.startfile(file_path)

    # Excel sürecinin çalışıp çalışmadığını kontrol etmek için süreklilikle kontrol etme
    excel_process_name = "EXCEL.EXE"  # Windows için Excel'in süreç adı
    file_open = True

    while file_open:
        # Tüm çalışan süreçleri kontrol et
        file_open = False
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == excel_process_name:
                file_open = True
                break
        # Biraz bekle ve tekrar kontrol et
        time.sleep(1)

    # Excel süreci sona erdikten sonra dosyayı silme
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} dosyası başarıyla silindi.")
    else:
        print(f"{file_path} dosyası bulunamadı.")
    #----------------------------------------------------------EXCEL
    # hepsini dışarı veriyoruz. Bir sıkıntı gözükmüyor.
    return (temiz_df, gunler_df, aylar_df, aylik_faturalar, aylik_senaryolar)

the_all_mighty()
        