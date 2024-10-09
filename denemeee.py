from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
from tester import the_all_mighty  # tester.py dosyasından the_all_mighty fonksiyonunu içe aktarıyoruz
import matplotlib
matplotlib.use('agg')
import gc


# Veriyi işleme fonksiyonunuzu çalıştırıyoruz
temiz_df, gunler_df, aylar_df, aylik_faturalar, aylik_senaryolar = the_all_mighty()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.left_panel = QtWidgets.QWidget(self.splitter)
        self.left_panel.setObjectName("left_panel")
        self.left_layout = QtWidgets.QVBoxLayout(self.left_panel)
        self.left_layout.setObjectName("left_layout")

        self.year_dropdown = QtWidgets.QComboBox(self.left_panel)
        self.year_dropdown.setObjectName("year_dropdown")
        self.year_dropdown.addItem("Yıl Seçimi")
        self.year_dropdown.addItems(["2020", "2021", "2022", "2023", "2024"])
        self.left_layout.addWidget(self.year_dropdown)

        self.month_dropdown = QtWidgets.QComboBox(self.left_panel)
        self.month_dropdown.setObjectName("month_dropdown")
        self.month_dropdown.addItem("Ay Seçimi")
        self.month_dropdown.addItems([
            "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
            "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık", "Tüm yıl"
        ])
        self.left_layout.addWidget(self.month_dropdown)

        self.upload_button = QtWidgets.QPushButton(self.left_panel)
        self.upload_button.setObjectName("upload_button")
        self.upload_button.setText("Dosya Yükle")
        self.left_layout.addWidget(self.upload_button)

        # Eski analiz butonunu ikiye ayırıyoruz
        self.eFaturaAnalizi_button = QtWidgets.QPushButton(self.left_panel)
        self.eFaturaAnalizi_button.setObjectName("eFaturaAnalizi_button")
        self.eFaturaAnalizi_button.setText("eFatura Analizi")
        self.left_layout.addWidget(self.eFaturaAnalizi_button)

        self.faturaTuruAnalizi_button = QtWidgets.QPushButton(self.left_panel)
        self.faturaTuruAnalizi_button.setObjectName("faturaTuruAnalizi_button")
        self.faturaTuruAnalizi_button.setText("Fatura Türü Analizi")
        self.left_layout.addWidget(self.faturaTuruAnalizi_button)

        self.AylikOzet_button = QtWidgets.QPushButton(self.left_panel)
        self.AylikOzet_button.setObjectName("AylikOzet_button")
        self.AylikOzet_button.setText("Aylık Özet")
        self.left_layout.addWidget(self.AylikOzet_button)

        self.right_panel = QtWidgets.QWidget(self.splitter)
        self.right_panel.setObjectName("right_panel")
        self.right_layout = QtWidgets.QVBoxLayout(self.right_panel)
        self.right_layout.setObjectName("right_layout")

        # Grafik alanı için üstteki widget ve layout
        self.plotArea = QtWidgets.QWidget(self.right_panel)
        self.plotArea.setMinimumSize(QtCore.QSize(0, 800))  # Grafiğin yüksekliğini artırıyoruz
        self.plotArea.setObjectName("plotArea")

        self.plot_layout = QtWidgets.QVBoxLayout(self.plotArea)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.addWidget(self.plotArea)

        # Aşağıda tabloyu içeren scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.right_panel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 280, 200))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.table_widget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.table_widget.setObjectName("table_widget")
        self.verticalLayout_2.addWidget(self.table_widget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.right_layout.addWidget(self.scrollArea)

        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Veri Analiz Arayüzü"))

class MainWindow(QMainWindow, Ui_MainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.setupUi(self)

            # Plot alanı için matplotlib canvas oluştur
            self.canvas = MplCanvas(self.plotArea, width=5, height=4, dpi=100)
            self.plot_layout.addWidget(self.canvas)  # Grafiği layout'a ekliyoruz

            # Butonlara işlev atama
            self.upload_button.clicked.connect(self.load_file)
            self.eFaturaAnalizi_button.clicked.connect(self.eFaturaAnalizi)
            self.faturaTuruAnalizi_button.clicked.connect(self.faturaTuruAnalizi)
            self.AylikOzet_button.clicked.connect(self.AylikOzet)

        def load_file(self):
            # Dosya yükleme işlemi
            file_name, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "CSV Files (*.csv)")
            if file_name:
                # Dosya yüklendikten sonra işlemler burada yapılabilir
                pass

        def filter_data(self, df):
            selected_year = int(self.year_dropdown.currentText())
            selected_month = self.month_dropdown.currentText()  # Ay adını al

            if selected_month == "Tüm Yıl":
                filtered_df = df[df['Yıl'] == selected_year]  # Tüm yıl için veri filtrele
            else:
                selected_month_index = self.month_dropdown.currentIndex()
                filtered_df = df[(df['Yıl'] == selected_year) & (df['Ay'] == selected_month_index)]  # Ayı filtrele

            return filtered_df

        def eFaturaAnalizi(self):
            try:
                filtered_data = self.filter_data(aylik_senaryolar)  # Aylık Senaryolar verisini filtrele

                # Veri yapısını kontrol etme
                print("eFaturaAnalizi - Filtered Data Columns:", filtered_data.columns)
                print("eFaturaAnalizi - Filtered Data Head:", filtered_data.head())

                # Mevcut canvas'ı tamamen kaldırıp yenisini oluşturuyoruz
                self.plot_layout.removeWidget(self.canvas)
                self.canvas.deleteLater()
                self.canvas = MplCanvas(self.plotArea, width=5, height=4, dpi=100)
                self.plot_layout.addWidget(self.canvas)

                self.canvas.axes.clear()

                if self.month_dropdown.currentText() == "Tüm Yıl":
                    # Yıl boyunca toplamları göstermek için:
                    filtered_data = filtered_data.groupby('Yıl').sum().reset_index()
                    filtered_data.plot(kind='bar', x='Yıl', ax=self.canvas.axes)

                    self.canvas.axes.set_title('E-Fatura Senaryoları - Tüm Yıl Toplamı')
                    self.canvas.axes.set_xlabel('Yıl')
                    self.canvas.axes.set_ylabel('Toplam Miktar')
                else:
                    # Belirli bir ay seçildiyse, her bir sütun için ayrı barlar çiz
                    filtered_data = filtered_data.drop(columns=['Yıl'], errors='ignore')  # Yıl sütununu kaldırıyoruz
                    filtered_data.set_index('Ay').plot(kind='bar', ax=self.canvas.axes)

                self.canvas.draw_idle()

                self.update_table(filtered_data)

                # Garbage collection ile bellek yönetimi
                gc.collect()

            except Exception as e:
                print(f"Hata oluştu: {e}")
                gc.collect()

        def faturaTuruAnalizi(self):
            try:
                filtered_data = self.filter_data(aylik_faturalar)  # Aylık Faturalar verisini filtrele

                # Veri yapısını kontrol etme
                print("faturaTuruAnalizi - Filtered Data Columns:", filtered_data.columns)
                print("faturaTuruAnalizi - Filtered Data Head:", filtered_data.head())

                # Mevcut canvas'ı tamamen kaldırıp yenisini oluşturuyoruz
                self.plot_layout.removeWidget(self.canvas)
                self.canvas.deleteLater()
                self.canvas = MplCanvas(self.plotArea, width=5, height=4, dpi=100)
                self.plot_layout.addWidget(self.canvas)

                self.canvas.axes.clear()

                if self.month_dropdown.currentText() == "Tüm Yıl":
                    # Eğer "Tüm Yıl" seçildiyse, Ay sütununa göre barları çiz
                    filtered_data = filtered_data.drop(columns=['Yıl'], errors='ignore')  # Yıl sütununu kaldırıyoruz
                    filtered_data.plot(kind='bar', x='Ay', stacked=True, ax=self.canvas.axes)
                else:
                    # Belirli bir ay seçildiyse, her bir sütun için ayrı barlar çiz
                    filtered_data = filtered_data.drop(columns=['Yıl'], errors='ignore')  # Yıl sütununu kaldırıyoruz
                    filtered_data.set_index('Ay').plot(kind='bar', ax=self.canvas.axes)

                self.canvas.axes.set_title('Fatura Türü Analizi')
                self.canvas.draw_idle()

                self.update_table(filtered_data)

                # Garbage collection ile bellek yönetimi
                gc.collect()

            except Exception as e:
                print(f"Hata oluştu: {e}")
                gc.collect()

        def AylikOzet(self):
            try:
                if self.month_dropdown.currentText() == "Tüm Yıl":
                    # Tüm Yıl seçildiğinde aylar_df'yi kullanıyoruz
                    filtered_data = self.filter_data(aylar_df)
                    print("AylikOzet - Filtered Data Columns:", filtered_data.columns)
                    print("AylikOzet - Filtered Data Head:", filtered_data.head())

                    # Mevcut canvas'ı tamamen kaldırıp yenisini oluşturuyoruz
                    self.plot_layout.removeWidget(self.canvas)
                    self.canvas.deleteLater()
                    self.canvas = MplCanvas(self.plotArea, width=5, height=4, dpi=100)
                    self.plot_layout.addWidget(self.canvas)

                    self.canvas.axes.clear()
                    filtered_data.plot(kind='bar', x='Ay', y=['Gelir', 'Gider'], stacked=True, ax=self.canvas.axes)
                    self.canvas.axes.set_title('Aylık Gelir/Gider Özeti')
                else:
                    # Belirli bir ay seçildiğinde gunler_df'yi kullanıyoruz
                    filtered_data = self.filter_data(gunler_df)
                    print("AylikOzet (Günlük) - Filtered Data Columns:", filtered_data.columns)
                    print("AylikOzet (Günlük) - Filtered Data Head:", filtered_data.head())

                    filtered_data = filtered_data[['Gün', 'Gelir', 'Gider']].melt(id_vars=['Gün'], var_name='Tür',
                                                                                  value_name='Miktar')
                    self.canvas.axes.clear()
                    sns.barplot(data=filtered_data, x='Gün', y='Miktar', hue='Tür', ax=self.canvas.axes)
                    self.canvas.axes.set_title('Günlük Gelir/Gider Özeti')

                self.canvas.draw_idle()

                self.update_table(filtered_data)

                # Garbage collection ile bellek yönetimi
                gc.collect()

            except Exception as e:
                print(f"Hata oluştu: {e}")
                gc.collect()

        def update_table(self, data):
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data.columns))
            self.table_widget.setHorizontalHeaderLabels(data.columns)

            for i, row in data.iterrows():
                for j, col in enumerate(data.columns):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(row[col])))


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

