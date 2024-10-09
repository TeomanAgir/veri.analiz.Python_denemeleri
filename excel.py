import os

# Masaüstü yolunu bulma
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Silinecek Excel dosyasının yolu
file_path = os.path.join(desktop, "ciktilar.xlsx")

# Dosyanın var olup olmadığını kontrol etme ve silme
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} dosyası başarıyla silindi.")
else:
    print(f"{file_path} dosyası bulunamadı.")