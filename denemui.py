from PyQt5 import QtCore, QtGui, QtWidgets


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
            "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
        ])
        self.left_layout.addWidget(self.month_dropdown)

        self.upload_button = QtWidgets.QPushButton(self.left_panel)
        self.upload_button.setObjectName("upload_button")
        self.upload_button.setText("Dosya Yükle")
        self.left_layout.addWidget(self.upload_button)

        self.analyze_button = QtWidgets.QPushButton(self.left_panel)
        self.analyze_button.setObjectName("analyze_button")
        self.analyze_button.setText("Analiz Et")
        self.left_layout.addWidget(self.analyze_button)

        self.right_panel = QtWidgets.QWidget(self.splitter)
        self.right_panel.setObjectName("right_panel")
        self.right_layout = QtWidgets.QVBoxLayout(self.right_panel)
        self.right_layout.setObjectName("right_layout")

        self.plotArea = QtWidgets.QWidget(self.right_panel)
        self.plotArea.setMinimumSize(QtCore.QSize(0, 600))
        self.plotArea.setObjectName("plotArea")
        self.right_layout.addWidget(self.plotArea)

        self.scrollArea = QtWidgets.QScrollArea(self.right_panel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 280, 500))
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

