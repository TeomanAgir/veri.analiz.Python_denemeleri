import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QComboBox, QPushButton, QLabel, QHBoxLayout, QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import webpy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 1200, 800)

        self.current_graph_col = None
        self.current_graph_title = None

        main_layout = QVBoxLayout()

        # Dataframe table
        self.table_widget = QTableWidget()
        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.table_widget.setMaximumHeight(200)
        main_layout.addWidget(self.table_widget)

        # Graph area
        self.canvas = FigureCanvas(Figure())
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.canvas)

        # Dropdown menus and buttons
        control_layout = QVBoxLayout()

        self.year_combo = QComboBox()
        self.year_combo.currentIndexChanged.connect(self.update_data)
        control_layout.addWidget(self.year_combo)

        self.month_combo = QComboBox()
        self.month_combo.addItems(["Tüm Yıl"] + [str(i) for i in range(1, 13)])
        self.month_combo.currentIndexChanged.connect(self.update_data)
        control_layout.addWidget(self.month_combo)

        button_layout = QHBoxLayout()

        fatura_turu_btn = QPushButton("Fatura Türleri")
        fatura_turu_btn.clicked.connect(self.plot_fatura_turu)
        button_layout.addWidget(fatura_turu_btn)

        fatura_senaryo_btn = QPushButton("Fatura Senaryoları")
        fatura_senaryo_btn.clicked.connect(self.plot_fatura_senaryo)
        button_layout.addWidget(fatura_senaryo_btn)

        gelir_gider_btn = QPushButton("Gelir/Gider")
        gelir_gider_btn.clicked.connect(self.plot_gelir_gider)
        button_layout.addWidget(gelir_gider_btn)

        button_layout.addStretch()
        control_layout.addLayout(button_layout)

        main_layout.addLayout(control_layout)

        # Best day details
        self.best_day_label = QLabel()
        main_layout.addWidget(self.best_day_label)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.load_data()

    def load_data(self):
        # Verileri webpy.py dosyasından yükleme
        (self.temiz_df, self.gunler_df, self.gunluk_fatura_turleri, self.haftalar_df,
         self.haftalik_fatura_turleri, self.aylar_df, self.aylik_fatura_turleri) = webpy.the_all_mighty()

        # Yılları combobox'a ekleme
        years = self.temiz_df['Yıl'].unique()
        self.year_combo.addItems(map(str, years))

        # İlk tablo gösterimi
        self.update_data()

    def update_data(self):
        year = int(self.year_combo.currentText())
        month = self.month_combo.currentText()

        df = self.temiz_df[self.temiz_df['Yıl'] == year]

        if month != "Tüm Yıl":
            df = df[df['Ay'] == int(month)]

        self.update_table(df)
        self.update_graph()

    def update_table(self, df):
        self.table_widget.setRowCount(len(df.index))
        self.table_widget.setColumnCount(len(df.columns))
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        print("Table updated successfully")

    def update_graph(self):
        if self.current_graph_col and self.current_graph_title:
            self.plot_graph(self.current_graph_col, self.current_graph_title)

    def plot_graph(self, column, title):
        self.current_graph_col = column
        self.current_graph_title = title

        year = int(self.year_combo.currentText())
        month = self.month_combo.currentText()

        df = self.temiz_df[self.temiz_df['Yıl'] == year]

        if month != "Tüm Yıl":
            df = df[df['Ay'] == int(month)]

        if column in df.columns:
            data = df[column].value_counts()
        else:
            data = df.groupby(column).size()

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.bar(data.index.astype(str), data.values)
        ax.set_title(title)
        ax.set_xticks(range(len(data.index)))
        ax.set_xticklabels(data.index.astype(str), rotation=45, ha='right')
        self.canvas.draw()

        self.update_best_day(df)

        print("Graph plotted successfully")

    def plot_fatura_turu(self):
        self.plot_graph('FATURA_TURU', 'Fatura Türleri Grafiği')

    def plot_fatura_senaryo(self):
        self.plot_graph('eFaturaSenaryo', 'Fatura Senaryoları Grafiği')

    def plot_gelir_gider(self):
        self.current_graph_col = None
        self.current_graph_title = None

        year = int(self.year_combo.currentText())
        month = self.month_combo.currentText()

        df = self.temiz_df[self.temiz_df['Yıl'] == year]

        if month != "Tüm Yıl":
            df = df[df['Ay'] == int(month)]

        gelir = df[df['FATURA_TURU'] == 8]['TOPLAM'].sum()
        gider = df[df['FATURA_TURU'] == 3]['TOPLAM'].sum()

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.bar(['Gelir', 'Gider'], [gelir, gider], color=['blue', 'purple'])
        ax.set_title("Gelir ve Gider Grafiği")
        self.canvas.draw()

        self.update_best_day(df)

        print("Gelir/Gider Graph plotted successfully")

    def update_best_day(self, df):
        if 'Gelir' in df.columns and len(df) > 0:
            best_day = df.loc[df['Gelir'].idxmax()]
            details = f"En İyi Gün: {best_day['Yıl']}-{best_day['Ay']}-{best_day['Gün']}\n"
            details += f"Gelir: {best_day['Gelir']}\n"
            details += f"Gider: {best_day['Gider']}\n"
            details += f"Fatura Türü: {best_day['FATURA_TURU']}\n"
            details += f"Senaryo: {best_day['eFaturaSenaryo']}\n"
            self.best_day_label.setText(details)
        else:
            self.best_day_label.setText("No data for that period")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())