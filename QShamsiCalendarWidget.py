from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
import convert_numbers
import jdatetime


class DayLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.selected = False
        self.current_date_style = False
        self.isfriday = False
        self.default_style()        
        
    
    def default_style(self):
        if self.isfriday:
            if self.current_date_style and self.selected:
                self.setStyleSheet("background-color: yellow; border: 1px solid red; color: red")
            elif self.current_date_style:
                self.setStyleSheet("background-color: yellow; border: 1px solid white; color: red")
            elif self.selected:
                self.setStyleSheet("background-color: cyan; border: 1px solid red; color: red")
            else:
                self.setStyleSheet("background-color: cyan; border: 1px solid white; color: red")
        else:
            if self.current_date_style and self.selected:
                self.setStyleSheet("background-color: yellow; border: 1px solid red; color: black")
            elif self.current_date_style:
                self.setStyleSheet("background-color: yellow; border: 1px solid white; color: black")
            elif self.selected:
                self.setStyleSheet("background-color: cyan; border: 1px solid red; color: black")
            else:
                self.setStyleSheet("background-color: cyan; border: 1px solid white; color: black")

    
    def setDayText(self, text):
        self.dayText = text
        if text == -1:
            self.setText(' ')
        else:
            self.setText(convert_numbers.english_to_persian(str(text)))


    def enterEvent(self, event):
        if self.isfriday:
            if self.current_date_style:
                self.setStyleSheet("background-color: yellow; border: 1px solid black; color: red") 
            else:
                self.setStyleSheet("background-color: cyan; border: 1px solid black; color: red")
        else:
            if self.current_date_style:
                self.setStyleSheet("background-color: yellow; border: 1px solid black; color: black") 
            else:
                self.setStyleSheet("background-color: cyan; border: 1px solid black; color: black")


    def leaveEvent(self, event):
        self.default_style()


    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


class QShamsiCalendarWidget(QWidget):
    sel_date_changed = pyqtSignal()

    def __init__(self, first_year, last_year):
        super().__init__()
        self.first_year = first_year
        self.last_year = last_year
        self.current_date = jdatetime.date.today()
        self.selected_date = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        head_layout = QHBoxLayout()
        grid = QGridLayout()
        headers = ['جمعه', 'پنجشنبه', 'چهارشنبه', 'سه‌شنبه', 'دوشنبه', 'یکشنبه', 'شنبه']
        header_positions = [(0, i) for i in range(7)]
        for pos, name in zip(header_positions, headers):
            label = QLabel(self)
            label.setStyleSheet("background-color: white; border: 1px solid white")
            label.setText(name)
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, *pos)

        self.weeks = []
        for i in range(1, 7):
            temp_week = list()
            for j in list(range(7))[::-1]:
                pos = (i, j)
                label = DayLabel(self)
                label.setDayText(-1)
                label.setAlignment(Qt.AlignCenter)
                label.clicked.connect(self.day_label_clicked)
                grid.addWidget(label, *pos)
                temp_week.append(label)
            self.weeks.append(temp_week)

        self.next_month_btn = QPushButton(self)    
        self.next_month_btn.setText('ماه بعدی')
        self.next_month_btn.clicked.connect(self.next_month_btn_clicked)
        head_layout.addWidget(self.next_month_btn)

        self.month_combo = QComboBox(self)
        self.month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        for month_name in self.month_names:
            self.month_combo.addItem(month_name)
        self.month_combo.setCurrentIndex(jdatetime.date.today().month - 1)
        self.month_combo.currentIndexChanged.connect(self.month_combo_changed)
        head_layout.addWidget(self.month_combo)

        self.year_combo = QComboBox(self)
        self.years = list(range(self.first_year, self.last_year + 1))
        for year in self.years:
            self.year_combo.addItem(convert_numbers.english_to_persian(str(year)))
        self.year_combo.setCurrentIndex(self.years.index(jdatetime.date.today().year))
        self.year_combo.currentIndexChanged.connect(self.year_combo_changed)
        head_layout.addWidget(self.year_combo)

        self.last_month_btn = QPushButton(self)    
        self.last_month_btn.setText('ماه قبلی')
        self.last_month_btn.clicked.connect(self.last_month_btn_clicked)
        head_layout.addWidget(self.last_month_btn)

        main_layout.addLayout(head_layout)
        main_layout.addLayout(grid)
        self.fix_days()
        self.setLayout(main_layout)
    
    def fix_days(self):
        for i in range(6):
            for j in list(range(7)):
                self.weeks[i][j].setDayText(-1)
                self.weeks[i][j].selected = False
                self.weeks[i][j].current_date_style = False
                self.weeks[i][j].isfriday = False
                self.weeks[i][j].default_style()       
        year = self.years[self.year_combo.currentIndex()]
        month = self.month_combo.currentIndex() + 1
        first_day = jdatetime.date(year, month, 1)
        day_thr = -1
        if first_day.isleap():
            if 7 <= month <= 12:
                day_thr = 30
            else:
                day_thr = 31
        else:
            if month == 12:
                day_thr = 29
            elif 7 <= month <= 11:
                day_thr = 30
            else:
                day_thr = 31
        first_day_week_id = first_day.weekday()
        day_co = 0
        for i in range(6):
            if day_co == day_thr:
                break
            if i == 0:
                for j in list(range(first_day_week_id, 7)):
                    self.weeks[i][j].setDayText(day_co + 1)
                    if self.current_date == jdatetime.date(year, month, day_co + 1):
                        self.weeks[i][j].current_date_style = True
                    if self.selected_date == jdatetime.date(year, month, day_co + 1):
                        self.weeks[i][j].selected = True
                    if jdatetime.date(year, month, day_co + 1).weekday() == 6:
                        self.weeks[i][j].isfriday = True
                    self.weeks[i][j].default_style()
                    day_co += 1
            else:
                for j in list(range(7)):
                    self.weeks[i][j].setDayText(day_co + 1)
                    if self.current_date == jdatetime.date(year, month, day_co + 1):
                        self.weeks[i][j].current_date_style = True
                    if self.selected_date == jdatetime.date(year, month, day_co + 1):
                        self.weeks[i][j].selected = True
                    if jdatetime.date(year, month, day_co + 1).weekday() == 6:
                        self.weeks[i][j].isfriday = True
                    self.weeks[i][j].default_style()
                    day_co += 1
                    if day_co == day_thr:
                        break                
    
    def day_label_clicked(self):
        label = self.sender()
        day_selected = label.dayText
        if day_selected != -1:
            year = self.years[self.year_combo.currentIndex()]
            month = self.month_combo.currentIndex() + 1
            current_selected_date = jdatetime.date(year, month, day_selected)
            for i in range(6):
                for j in list(range(7)):
                    if self.weeks[i][j].dayText == day_selected:
                        self.weeks[i][j].selected = not self.weeks[i][j].selected
                    else:
                        self.weeks[i][j].selected = False
                    self.weeks[i][j].default_style()
            if self.selected_date == current_selected_date:
                self.selected_date = None
            else:
                self.selected_date = current_selected_date
                self.sel_date_changed.emit()    
    
    def next_month_btn_clicked(self, event):
        month_index = self.month_combo.currentIndex()
        month_index += 1
        if month_index == len(self.month_names):
            year_index = self.year_combo.currentIndex()
            year_index += 1
            year_index %= len(self.years)
            self.year_combo.setCurrentIndex(year_index)
        month_index %= len(self.month_names)
        self.month_combo.setCurrentIndex(month_index)
        self.fix_days()    
    
    def month_combo_changed(self, ind):
        self.fix_days()    

    def year_combo_changed(self, ind):
        self.fix_days()
    
    def last_month_btn_clicked(self, event):
        month_index = self.month_combo.currentIndex()
        month_index -= 1
        if month_index == -1:
            year_index = self.year_combo.currentIndex()
            year_index -= 1
            year_index %= len(self.years)
            self.year_combo.setCurrentIndex(year_index)
        month_index %= len(self.month_names)
        self.month_combo.setCurrentIndex(month_index)
        self.fix_days()
    
    def enterEvent(self, event):
        if self.current_date != jdatetime.date.today():
            self.current_date = jdatetime.date.today()
            year = self.years[self.year_combo.currentIndex()]
            month = self.month_combo.currentIndex() + 1
            if self.current_date.year == year and self.current_date.month == month:
                self.fix_days()



    def leaveEvent(self, event):
        if self.current_date != jdatetime.date.today():
            self.current_date = jdatetime.date.today()
            year = self.years[self.year_combo.currentIndex()]
            month = self.month_combo.currentIndex() + 1
            if self.current_date.year == year and self.current_date.month == month:
                self.fix_days()