from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime, timedelta
from kivy.core.window import Window

# Pencere boyutunu mobil cihaz simülasyonu için ayarla
Window.size = (360, 640)


class CalendarDay(Button):
    def __init__(self, day_number, month, year, is_weekend_week, is_current_month=True, is_today=False, **kwargs):
        super().__init__(**kwargs)
        self.day_number = day_number
        self.month = month
        self.year = year
        self.is_weekend_week = is_weekend_week
        self.is_current_month = is_current_month
        self.is_today = is_today
        
        # Günü ayarla
        if day_number:
            self.text = str(day_number)
        else:
            self.text = ""
        
        # Stil ayarları
        self.font_size = dp(16) if is_today else dp(14)
        self.font_name = 'Roboto'
        self.bold = True if (is_current_month and day_number) or is_today else False
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        
        # Renkleri ayarla
        self.update_colors()
    
    def update_colors(self):
        if not self.day_number:
            self.color = (0.5, 0.5, 0.5, 0.3)
            return
        
        # Bugünün tarihi beyaz renkte olacak
        if self.is_today:
            self.color = (1, 1, 1, 1)
        elif self.is_current_month:
            self.color = (0.2, 0.2, 0.2, 1)
        else:
            self.color = (0.6, 0.6, 0.6, 0.6)
    
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.day_number:
                # Bugünün tarihi için özel işaretleme
                if self.is_today:
                    # Koyu mavi arka plan
                    Color(0.2, 0.4, 0.8, 1)
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
                elif self.is_current_month:
                    if self.is_weekend_week:
                        # Hafif kırmızı ton
                        Color(1, 0.85, 0.85, 1)
                    else:
                        # Hafif yeşil ton
                        Color(0.85, 1, 0.85, 1)
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
                else:
                    Color(1, 1, 1, 0)
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])


class ModernCalendar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(16)
        self.spacing = dp(12)
        
        # Bugünkü tarihle başla
        self.today = datetime.now()
        self.current_date = datetime.now()
        self.reference_date = datetime(2026, 3, 2)  # 2 Mart 2026 Pazartesi
        
        self.build_calendar()
    
    def build_calendar(self):
        self.clear_widgets()
        
        # Başlık bölümü
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        header.padding = [0, dp(8), 0, dp(8)]
        
        # Önceki ay butonu
        prev_btn = Button(
            text='<',
            size_hint_x=0.2,
            font_size=dp(24),
            background_color=(0.3, 0.6, 0.9, 1),
            background_normal='',
            bold=True
        )
        prev_btn.bind(on_press=self.previous_month)
        
        # Ay ve yıl etiketi
        month_year_label = Label(
            text=self.get_month_year_text(),
            size_hint_x=0.6,
            font_size=dp(20),
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        
        # Sonraki ay butonu
        next_btn = Button(
            text='>',
            size_hint_x=0.2,
            font_size=dp(24),
            background_color=(0.3, 0.6, 0.9, 1),
            background_normal='',
            bold=True
        )
        next_btn.bind(on_press=self.next_month)
        
        header.add_widget(prev_btn)
        header.add_widget(month_year_label)
        header.add_widget(next_btn)
        
        self.add_widget(header)
        
        # Gün başlıkları (Pazartesi'den başlayacak)
        days_header = GridLayout(cols=7, size_hint_y=None, height=dp(40), spacing=dp(4))
        day_names = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
        
        for day_name in day_names:
            label = Label(
                text=day_name,
                font_size=dp(12),
                bold=True,
                color=(0.4, 0.4, 0.4, 1)
            )
            days_header.add_widget(label)
        
        self.add_widget(days_header)
        
        # Takvim günleri
        calendar_grid = GridLayout(cols=7, spacing=dp(4))
        
        # Ayın ilk gününü ve gün sayısını hesapla
        first_day = datetime(self.current_date.year, self.current_date.month, 1)
        
        # Pazartesi'den başlamak için (0 = Pazartesi, 6 = Pazar)
        weekday = (first_day.weekday()) % 7
        
        # Bir sonraki ayın ilk gününü bul
        if self.current_date.month == 12:
            next_month = datetime(self.current_date.year + 1, 1, 1)
        else:
            next_month = datetime(self.current_date.year, self.current_date.month + 1, 1)
        
        days_in_month = (next_month - first_day).days
        
        # Önceki ayın son günlerini ekle
        prev_month_date = first_day - timedelta(days=1)
        prev_month_days = (next_month - timedelta(days=1)).replace(day=1)
        days_in_prev_month = (first_day - prev_month_days).days
        
        for i in range(weekday):
            day = days_in_prev_month - weekday + i + 1
            date_to_check = datetime(prev_month_date.year, prev_month_date.month, day)
            is_weekend_week = self.is_weekend_week(date_to_check)
            is_today = (date_to_check.date() == self.today.date())
            
            btn = CalendarDay(day, prev_month_date.month, prev_month_date.year, 
                            is_weekend_week, is_current_month=False, is_today=is_today)
            calendar_grid.add_widget(btn)
        
        # Bu ayın günlerini ekle
        for day in range(1, days_in_month + 1):
            date_to_check = datetime(self.current_date.year, self.current_date.month, day)
            is_weekend_week = self.is_weekend_week(date_to_check)
            is_today = (date_to_check.date() == self.today.date())
            
            btn = CalendarDay(day, self.current_date.month, self.current_date.year, 
                            is_weekend_week, is_current_month=True, is_today=is_today)
            calendar_grid.add_widget(btn)
        
        # Sonraki ayın ilk günlerini ekle (grid'i tamamlamak için)
        remaining_cells = 42 - (weekday + days_in_month)  # 6 satır x 7 gün
        for day in range(1, remaining_cells + 1):
            if self.current_date.month == 12:
                next_month_date = datetime(self.current_date.year + 1, 1, day)
            else:
                next_month_date = datetime(self.current_date.year, self.current_date.month + 1, day)
            
            is_weekend_week = self.is_weekend_week(next_month_date)
            is_today = (next_month_date.date() == self.today.date())
            
            btn = CalendarDay(day, next_month_date.month, next_month_date.year, 
                            is_weekend_week, is_current_month=False, is_today=is_today)
            calendar_grid.add_widget(btn)
        
        self.add_widget(calendar_grid)
        
        # Açıklama
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), padding=[0, dp(16), 0, 0])
        info_layout.spacing = dp(16)
        
        # Kırmızı hafta örneği
        red_week_box = BoxLayout(orientation='horizontal', spacing=dp(8))
        red_indicator = Label(size_hint_x=None, width=dp(30))
        with red_indicator.canvas:
            Color(1, 0.85, 0.85, 1)
            RoundedRectangle(pos=red_indicator.pos, size=(dp(30), dp(30)), radius=[dp(4)])
        red_week_box.add_widget(red_indicator)
        red_week_box.add_widget(Label(text='Hafta Aşırı\n(Kırmızı)', font_size=dp(11), color=(0.3, 0.3, 0.3, 1)))
        
        # Yeşil hafta örneği
        green_week_box = BoxLayout(orientation='horizontal', spacing=dp(8))
        green_indicator = Label(size_hint_x=None, width=dp(30))
        with green_indicator.canvas:
            Color(0.85, 1, 0.85, 1)
            RoundedRectangle(pos=green_indicator.pos, size=(dp(30), dp(30)), radius=[dp(4)])
        green_week_box.add_widget(green_indicator)
        green_week_box.add_widget(Label(text='Normal Hafta\n(Yeşil)', font_size=dp(11), color=(0.3, 0.3, 0.3, 1)))
        
        info_layout.add_widget(red_week_box)
        info_layout.add_widget(green_week_box)
        
        self.add_widget(info_layout)
    
    def is_weekend_week(self, date):
        """
        2 Mart 2026 Pazartesi'den başlayarak haftaları belirle.
        İlk hafta (2 Mart başlangıç) kırmızı, sonraki yeşil, sonraki kırmızı...
        """
        if date < self.reference_date:
            # Referans tarihinden önceki tarihler için geri sayım
            days_diff = (self.reference_date - date).days
            week_number = (days_diff // 7) + 1
            # Ters çevir çünkü geriye gidiyoruz
            return week_number % 2 == 1
        else:
            # Referans tarihinden itibaren
            days_diff = (date - self.reference_date).days
            week_number = days_diff // 7
            # İlk hafta (week_number = 0) kırmızı olacak
            return week_number % 2 == 0
    
    def get_month_year_text(self):
        months_tr = [
            'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
            'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
        ]
        return f"{months_tr[self.current_date.month - 1]} {self.current_date.year}"
    
    def previous_month(self, instance):
        if self.current_date.month == 1:
            self.current_date = datetime(self.current_date.year - 1, 12, 1)
        else:
            self.current_date = datetime(self.current_date.year, self.current_date.month - 1, 1)
        self.build_calendar()
    
    def next_month(self, instance):
        if self.current_date.year <= 2030:  # 2030 yılına kadar
            if self.current_date.month == 12:
                self.current_date = datetime(self.current_date.year + 1, 1, 1)
            else:
                self.current_date = datetime(self.current_date.year, self.current_date.month + 1, 1)
            self.build_calendar()


class CalendarApp(App):
    def build(self):
        self.title = 'Modern Takvim'
        
        # Ana layout
        root = BoxLayout(orientation='vertical')
        
        # Arka plan rengi için canvas
        with root.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            self.rect = RoundedRectangle(size=root.size, pos=root.pos)
        
        root.bind(size=self._update_rect, pos=self._update_rect)
        
        # Takvimi ekle
        calendar = ModernCalendar()
        root.add_widget(calendar)
        
        return root
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    CalendarApp().run()
