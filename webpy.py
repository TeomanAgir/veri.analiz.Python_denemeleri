import pandas as pd
import numpy as np


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

    # Fatura türlerini sayısal değerlere dönüştürmek için bir dictionary oluştur
    # fatura_turu_dict = {
    #     'SATIŞ İRSALİYESİ': 1,
    #     'MÜSTAHSİL': 2,
    #     'ALIŞ FATURASI': 3,
    #     'ALIŞ İRSALİYESİ': 4,
    #     'İPTAL': 5,
    #     'İPTAL SATIŞ FATURASI': 6,
    #     'SATIŞ FATURASI İADESİ': 7,
    #     'SATIŞ FATURASI': 8
    # }

    # Ters dictionary (sayısal değerden isme dönüşüm için)
    reverse_fatura_turu_dict = {v: k for k, v in fatura_turu_dict.items()}

    # Fatura türlerini sayısal değerlere dönüştür
    df['FATURA_TURU'] = df['FATURA_TURU'].map(fatura_turu_dict)

    # Temizlenmiş veri setini kaydet
    temiz_df = df.copy()

    # Temizlenmiş veri setini kaydetmeden önce "ÖDEME" sütununu ekleyin
    temiz_df['ÖDEME'] = np.where(temiz_df['TOPLAM'] == temiz_df['ALINAN'], 'Tamamlandı', 'Eksik')

    # Günlük analizler için veri çerçevesini gruplandır ve özetle
    gunluk_ozet = temiz_df.groupby(['Yıl', 'Ay', 'Gün']).agg({
        'TOPLAM': 'sum',
        'KDV': 'sum',
        'ALINAN': 'sum'
    }).reset_index()

    # Gelir, gider ve iptalleri hesapla
    gelir = temiz_df[temiz_df['FATURA_TURU'] == 'SATIŞ FATURASI'].groupby(['Yıl', 'Ay', 'Gün'])['TOPLAM'].sum().reset_index(
        name='Gelir')
    iptal = temiz_df[temiz_df['FATURA_TURU'].isin(['İPTAL', 'İPTAL SATIŞ FATURASI'])].groupby(['Yıl', 'Ay', 'Gün'])['TOPLAM'].sum().reset_index(
        name='İptal')
    gider = temiz_df[temiz_df['FATURA_TURU'] == 'ALIŞ FATURASI'].groupby(['Yıl', 'Ay', 'Gün'])['TOPLAM'].sum().reset_index(
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

    # Günlük fatura türlerini say
    gunluk_fatura_turleri = pd.pivot_table(temiz_df, values='TOPLAM', index=['Yıl', 'Ay', 'Gün'],
                                           columns=['FATURA_TURU'], aggfunc='count', fill_value=0).reset_index()
    gunluk_fatura_turleri.rename(columns=reverse_fatura_turu_dict, inplace=True)

    # Haftalık verileri gruplandır ve özetle
    temiz_df['Hafta'] = temiz_df['FAT_TARIH'].dt.isocalendar().week
    haftalik_ozet = temiz_df.groupby(['Yıl', 'Hafta']).agg({
        'TOPLAM': 'sum',
        'KDV': 'sum',
        'ALINAN': 'sum'
    }).reset_index()

    haftalik_ozet['İşlem Gün Sayısı'] = temiz_df.groupby(['Yıl', 'Hafta'])['Gün'].nunique().values
    # Gelir, gider ve iptalleri hesapla
    haftalik_gelir = temiz_df[temiz_df['FATURA_TURU'] == 8].groupby(['Yıl', 'Hafta'])['TOPLAM'].sum().reset_index(
        name='Gelir')
    haftalik_iptal = temiz_df[temiz_df['FATURA_TURU'].isin([5, 6])].groupby(['Yıl', 'Hafta'])[
        'TOPLAM'].sum().reset_index(name='İptal')
    haftalik_gider = temiz_df[temiz_df['FATURA_TURU'] == 3].groupby(['Yıl', 'Hafta'])['TOPLAM'].sum().reset_index(
        name='Gider')

    # Haftalık özet veri setini birleştir
    haftalik_ozet = haftalik_ozet.merge(haftalik_gelir, on=['Yıl', 'Hafta'], how='left')
    haftalik_ozet = haftalik_ozet.merge(haftalik_iptal, on=['Yıl', 'Hafta'], how='left')
    haftalik_ozet = haftalik_ozet.merge(haftalik_gider, on=['Yıl', 'Hafta'], how='left')

    # Null değerleri 0 ile değiştir
    haftalik_ozet.fillna(0, inplace=True)

    # Haftalık özet veri setini kaydet
    haftalar_df = haftalik_ozet.copy()

    # Haftalık özet veri setini kaydetmeden önce "ÖDEME" sütununu ekleyin
    haftalar_df['ÖDEME'] = np.where(haftalar_df['TOPLAM'] == haftalar_df['ALINAN'], 'Tamamlandı', 'Eksik')

    # Haftalık fatura türlerini say
    haftalik_fatura_turleri = pd.pivot_table(temiz_df, values='TOPLAM', index=['Yıl', 'Hafta'], columns=['FATURA_TURU'],
                                             aggfunc='count', fill_value=0).reset_index()
    haftalik_fatura_turleri.rename(columns=reverse_fatura_turu_dict, inplace=True)

    # Aylık verileri gruplandır ve özetle
    aylik_ozet = temiz_df.groupby(['Yıl', 'Ay']).agg({
        'TOPLAM': 'sum',
        'KDV': 'sum',
        'ALINAN': 'sum'
    }).reset_index()

    aylik_ozet['İşlem Gün Sayısı'] = temiz_df.groupby(['Yıl', 'Ay'])['Gün'].nunique().values
    # Gelir, gider ve iptalleri hesapla
    aylik_gelir = temiz_df[temiz_df['FATURA_TURU'] == 8].groupby(['Yıl', 'Ay'])['TOPLAM'].sum().reset_index(
        name='Gelir')
    aylik_iptal = temiz_df[temiz_df['FATURA_TURU'].isin([5, 6])].groupby(['Yıl', 'Ay'])['TOPLAM'].sum().reset_index(
        name='İptal')
    aylik_gider = temiz_df[temiz_df['FATURA_TURU'] == 3].groupby(['Yıl', 'Ay'])['TOPLAM'].sum().reset_index(
        name='Gider')

    # Aylık özet veri setini birleştir
    aylik_ozet = aylik_ozet.merge(aylik_gelir, on=['Yıl', 'Ay'], how='left')
    aylik_ozet = aylik_ozet.merge(aylik_iptal, on=['Yıl', 'Ay'], how='left')
    aylik_ozet = aylik_ozet.merge(aylik_gider, on=['Yıl', 'Ay'], how='left')

    # Null değerleri 0 ile değiştir
    aylik_ozet.fillna(0, inplace=True)

    # Aylık özet veri setini kaydet
    aylar_df = aylik_ozet.copy()

    # Aylık özet veri setini kaydetmeden önce "ÖDEME" sütununu ekleyin
    aylar_df['ÖDEME'] = np.where(aylar_df['TOPLAM'] == aylar_df['ALINAN'], 'Tamamlandı', 'Eksik')

    # Aylık fatura türlerini say
    aylik_fatura_turleri = pd.pivot_table(temiz_df, values='TOPLAM', index=['Yıl', 'Ay'], columns=['FATURA_TURU'],
                                          aggfunc='count', fill_value=0).reset_index()
    aylik_fatura_turleri.rename(columns=reverse_fatura_turu_dict, inplace=True)

    # Sayı formatlarını ayarla
    pd.options.display.float_format = '{:,.2f}'.format

    # hepsini dışarı veriyoruz. Bir sıkıntı gözükmüyor.
    return (temiz_df, gunler_df, gunluk_fatura_turleri, haftalar_df, haftalik_fatura_turleri,
            aylar_df, aylik_fatura_turleri)

