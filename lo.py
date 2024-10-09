<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Veri Analiz Arayüzü</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QSplitter" name="splitter" orientation="Qt::Horizontal">
      <property name="orientation">
       <enum>Qt::Horizontal</enum>
      </property>
      <widget class="QWidget" name="left_panel">
       <layout class="QVBoxLayout" name="left_layout">
        <item>
         <widget class="QComboBox" name="year_dropdown">
          <property name="currentText">
           <string>Yıl Seçimi</string>
          </property>
          <item>
           <property name="text">
            <string>2020</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>2021</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>2022</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>2023</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>2024</string>
           </property>
          </item>
         </widget>
        </item>
        <item>
         <widget class="QComboBox" name="month_dropdown">
          <property name="currentText">
           <string>Ay Seçimi</string>
          </property>
          <item>
           <property name="text">
            <string>Ocak</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Şubat</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Mart</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Nisan</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Mayıs</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Haziran</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Temmuz</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Ağustos</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Eylül</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Ekim</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Kasım</string>
           </property>
          </item>
          <item>
           <property name="text">
            <string>Aralık</string>
           </property>
          </item>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="upload_button">
          <property name="text">
           <string>Dosya Yükle</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="analyze_button">
          <property name="text">
           <string>Analiz Et</string>
          </property>
         </widget>
        </item>
       </layout>
      </widget>
      <widget class="QWidget" name="right_panel">
       <layout class="QVBoxLayout" name="right_layout">
        <item>
         <widget class="QWidget" name="plotArea">
          <property name="minimumSize">
           <size>
            <width>0</width>
            <height>400</height>
           </size>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QScrollArea" name="scrollArea">
          <property name="widgetResizable">
           <bool>true</bool>
          </property>
          <widget class="QWidget" name="scrollAreaWidgetContents">
           <layout class="QVBoxLayout" name="verticalLayout_2">
            <item>
             <widget class="QTableWidget" name="table_widget">
              <property name="minimumSize">
               <size>
                <width>0</width>
                <height>100</height>
               </size>
              </property>
             </widget>
            </item>
           </layout>
          </widget>
         </widget>
        </item>
       </layout>
      </widget>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
