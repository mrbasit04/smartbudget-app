# Smart Budget Manager - Full Multi-Screen KivyMD App
# Filename: SmartBudgetManager_app.py
# Purpose: Offline Android personal budget manager with monthly records, savings, charts
# Requirements: Python 3.10+, kivy, kivymd, matplotlib, sqlite3
# Run locally for testing: python SmartBudgetManager_app.py
# Buildozer for APK: see README-build.md

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import OneLineListItem, MDList, OneLineAvatarListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox

import sqlite3, os, datetime, io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

# For desktop testing window size (remove on Android)
Window.size = (360, 720)

KV = '''
MDScreenManager:

    DashboardScreen:
    IncomeScreen:
    ExpenseScreen:
    SummaryScreen:
    SavingsScreen:
    RecordsScreen:
    BalanceScreen:

<PanelButton@MDCard>:
    size_hint: None, None
    size: dp(160), dp(100)
    radius: [12,]
    padding: dp(8)
    elevation: 6
    ripple_behavior: True
    md_bg_color: root.theme_cls.primary_light

<DashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Smart Budget Manager'
            md_bg_color: app.theme_cls.primary_color
            elevation: 10

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(12)

            MDGridLayout:
                cols: 2
                adaptive_height: True
                spacing: dp(12)

                PanelButton:
                    on_release: app.change_screen('income')
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDIconButton:
                            icon: 'cash'
                            user_font_size: '32sp'
                            pos_hint: {'center_x':0.5}
                        MDLabel:
                            text: 'Income'
                            halign: 'center'

                PanelButton:
                    on_release: app.change_screen('expense')
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDIconButton:
                            icon: 'tray-full'
                            user_font_size: '32sp'
                            pos_hint: {'center_x':0.5}
                        MDLabel:
                            text: 'Expense'
                            halign: 'center'

                PanelButton:
                    on_release: app.change_screen('balance')
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDIconButton:
                            icon: 'finance'
                            user_font_size: '32sp'
                            pos_hint: {'center_x':0.5}
                        MDLabel:
                            text: 'Balance'
                            halign: 'center'

                PanelButton:
                    on_release: app.change_screen('summary')
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDIconButton:
                            icon: 'chart-box'
                            user_font_size: '32sp'
                            pos_hint: {'center_x':0.5}
                        MDLabel:
                            text: 'Summary'
                            halign: 'center'

                PanelButton:
                    on_release: app.change_screen('savings')
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDIconButton:
                            icon: 'piggy-bank'
                            user_font_size: '32sp'
                            pos_hint: {'center_x':0.5}
                        MDLabel:
                            text: 'Savings'
                            halign: 'center'

                PanelButton:
                    on_release: app.change_screen('records')
                    MDBoxLayout:
                        orientation: 'vertical'
                        MDIconButton:
                            icon: 'calendar-multiple'
                            user_font_size: '32sp'
                            pos_hint: {'center_x':0.5}
                        MDLabel:
                            text: 'Records'
                            halign: 'center'

            MDCard:
                size_hint_y: None
                height: dp(140)
                padding: dp(12)
                radius: [12,]
                elevation: 4

                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(6)

                    MDLabel:
                        id: lbl_income
                        text: 'Income: PKR 0.00'
                        font_style: 'H6'

                    MDLabel:
                        id: lbl_expense
                        text: 'Total Expense: PKR 0.00'
                        font_style: 'H6'

                    MDLabel:
                        id: lbl_balance
                        text: 'Balance: PKR 0.00'
                        font_style: 'H6'

                    MDLabel:
                        id: lbl_savings
                        text: 'Savings: PKR 0.00'
                        font_style: 'H6'

            MDLabel:
                text: 'Category breakdown (this month)'
                halign: 'left'

            Image:
                id: chart_image
                size_hint_y: None
                height: dp(220)
                allow_stretch: True
                keep_ratio: True

<IncomeScreen>:
    name: 'income'
    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Add Income'
            left_action_items: [['arrow-left', lambda x: app.change_screen('dashboard')]]
            md_bg_color: app.theme_cls.primary_color

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(12)

            MDTextField:
                id: income_amount
                hint_text: 'Amount (PKR)'
                input_filter: 'float'

            MDTextField:
                id: income_note
                hint_text: 'Note (Salary, Bonus, etc.)'

            MDRaisedButton:
                text: 'Save Income for Current Month'
                on_release: app.save_income()

<ExpenseScreen>:
    name: 'expense'
    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Add Expense'
            left_action_items: [['arrow-left', lambda x: app.change_screen('dashboard')]]
            md_bg_color: app.theme_cls.primary_color

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(10)

            MDTextField:
                id: exp_name
                hint_text: 'Expense name (e.g., Groceries)'

            MDTextField:
                id: exp_amount
                hint_text: 'Amount (PKR)'
                input_filter: 'float'

            MDBoxLayout:
                size_hint_y: None
                height: dp(40)
                spacing: dp(8)

                MDTextField:
                    id: cat_input
                    hint_text: 'Type new category (optional)'

                MDDropdownMenu:
                    id: cat_menu

            MDRaisedButton:
                text: 'Pick Date (default: today)'
                on_release: app.show_date_picker()

            MDRaisedButton:
                text: 'Save Expense'
                on_release: app.save_expense()

<SummaryScreen>:
    name: 'summary'
    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Monthly Summary'
            left_action_items: [['arrow-left', lambda x: app.change_screen('dashboard')]]
            md_bg_color: app.theme_cls.primary_color

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(8)

            MDLabel:
                id: sum_month
                text: 'Month: -'
                halign: 'left'

            MDLabel:
                id: sum_income
                text: 'Total Income: PKR 0.00'
                halign: 'left'

            MDLabel:
                id: sum_expense
                text: 'Total Expenses: PKR 0.00'
                halign: 'left'

            MDLabel:
                id: sum_savings
                text: 'Savings: PKR 0.00'
                halign: 'left'

            MDLabel:
                text: 'Expenses list:'
                halign: 'left'

            ScrollView:
                MDList:
                    id: expense_list

<SavingsScreen>:
    name: 'savings'
    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Savings'
            left_action_items: [['arrow-left', lambda x: app.change_screen('dashboard')]]
            md_bg_color: app.theme_cls.primary_color

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(8)

            MDLabel:
                id: sav_month
                text: 'Month: -'
                halign: 'left'

            MDLabel:
                id: sav_value
                text: 'This month savings: PKR 0.00'
                halign: 'left'

            MDLabel:
                text: 'Previous months savings:'
                halign: 'left'

            ScrollView:
                MDList:
                    id: savings_list

<RecordsScreen>:
    name: 'records'
    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Previous Records'
            left_action_items: [['arrow-left', lambda x: app.change_screen('dashboard')]]
            md_bg_color: app.theme_cls.primary_color

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(8)

            ScrollView:
                MDList:
                    id: months_list

<BalanceScreen>:
    name: 'balance'
    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Balance & Graphs'
            left_action_items: [['arrow-left', lambda x: app.change_screen('dashboard')]]
            md_bg_color: app.theme_cls.primary_color

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(12)
            spacing: dp(8)

            MDLabel:
                id: bal_label
                text: 'Current month balance: PKR 0.00'
                halign: 'left'

            Image:
                id: bal_chart
                size_hint_y: None
                height: dp(300)
                allow_stretch: True
                keep_ratio: True
'''

# -----------------------
# Database and helper functions
# -----------------------
DB_FILE = 'budget.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # months table keeps per-month totals including savings
    c.execute('''
        CREATE TABLE IF NOT EXISTS months (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            month INTEGER,
            income REAL DEFAULT 0,
            savings REAL DEFAULT 0,
            UNIQUE(year, month)
        )
    ''')
    # categories table
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    # expense table
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            name TEXT,
            category TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def ensure_month(year, month):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id FROM months WHERE year=? AND month=?', (year, month))
    row = c.fetchone()
    if not row:
        c.execute('INSERT INTO months(year, month, income, savings) VALUES(?,?,0,0)', (year, month))
        conn.commit()
    conn.close()

def set_income_for_month(year, month, amount):
    ensure_month(year, month)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE months SET income=? WHERE year=? AND month=?', (amount, year, month))
    conn.commit()
    conn.close()
    recalc_savings(year, month)

def add_expense_record(year, month, day, name, category, amount):
    ensure_month(year, month)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO expenses(year,month,day,name,category,amount) VALUES(?,?,?,?,?,?)', (year,month,day,name,category,amount))
    # add category if not exists
    try:
        c.execute('INSERT INTO categories(name) VALUES(?)', (category,))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()
    recalc_savings(year, month)

def recalc_savings(year, month):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT income FROM months WHERE year=? AND month=?', (year, month))
    row = c.fetchone()
    income = row[0] if row else 0
    c.execute('SELECT SUM(amount) FROM expenses WHERE year=? AND month=?', (year, month))
    s = c.fetchone()[0]
    total_expenses = s if s else 0
    savings = round(income - total_expenses, 2)
    c.execute('UPDATE months SET savings=? WHERE year=? AND month=?', (savings, year, month))
    conn.commit()
    conn.close()

def get_months_list():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT year,month,income,savings FROM months ORDER BY year DESC, month DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_categories():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT name FROM categories ORDER BY name')
    rows = [r[0] for r in c.fetchall()]
    conn.close()
    return rows

def get_expenses_for_month(year, month):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT year,month,day,name,category,amount FROM expenses WHERE year=? AND month=? ORDER BY year DESC, month DESC, day DESC', (year, month))
    rows = c.fetchall()
    conn.close()
    return rows

def get_totals_for_month(year, month):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT income, savings FROM months WHERE year=? AND month=?', (year, month))
    row = c.fetchone()
    income = row[0] if row else 0
    savings = row[1] if row else 0
    c.execute('SELECT SUM(amount) FROM expenses WHERE year=? AND month=?', (year, month))
    s = c.fetchone()[0]
    expense = s if s else 0
    conn.close()
    return income, expense, savings

# -----------------------
# App Class
# -----------------------
class DashboardScreen(MDScreen):
    pass
class IncomeScreen(MDScreen):
    pass
class ExpenseScreen(MDScreen):
    pass
class SummaryScreen(MDScreen):
    pass
class SavingsScreen(MDScreen):
    pass
class RecordsScreen(MDScreen):
    pass
class BalanceScreen(MDScreen):
    pass

class SmartBudgetApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Light'
        init_db()
        root = Builder.load_string(KV)
        Clock.schedule_once(lambda dt: self.post_build(), 0.2)
        return root

    def post_build(self):
        # initialize to current month
        self.current_date = datetime.date.today()
        self.refresh_dashboard()
        self.populate_categories_menu()
        self.populate_months_list()

    def change_screen(self, name):
        self.root.current = name
        if name == 'dashboard':
            self.refresh_dashboard()
        elif name == 'summary':
            self.show_summary()
        elif name == 'records':
            self.populate_months_list()
        elif name == 'savings':
            self.show_savings()
        elif name == 'balance':
            self.show_balance()

    # ----------------------
    # Income
    # ----------------------
    def save_income(self):
        val = self.root.get_screen('income').ids.income_amount.text.strip()
        note = self.root.get_screen('income').ids.income_note.text.strip()
        try:
            amount = float(val)
        except:
            self.show_message('Please enter a valid income amount')
            return
        year = self.current_date.year
        month = self.current_date.month
        set_income_for_month(year, month, amount)
        self.show_message('Income saved for current month')
        # clear fields
        self.root.get_screen('income').ids.income_amount.text = ''
        self.root.get_screen('income').ids.income_note.text = ''
        self.refresh_dashboard()

    # ----------------------
    # Expense
    # ----------------------
    def show_date_picker(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_save)
        date_picker.open()

    def on_date_save(self, instance, value, date_range):
        # value is datetime.date
        self._selected_date = value
        self.show_message(f'Date set to {value.isoformat()}')

    def populate_categories_menu(self):
        # simple approach: categories in dropdown are not complex MDDropdownMenu widgets here
        cats = get_categories()
        # store in app for UI access
        self.categories = cats

    def save_expense(self):
        scr = self.root.get_screen('expense')
        name = scr.ids.exp_name.text.strip()
        amt_text = scr.ids.exp_amount.text.strip()
        new_cat = scr.ids.cat_input.text.strip()
        # choose date
        sel_date = getattr(self, '_selected_date', None)
        if not sel_date:
            sel_date = datetime.date.today()
        try:
            amount = float(amt_text)
        except:
            self.show_message('Please enter a valid expense amount')
            return
        if not name:
            self.show_message('Please enter expense name')
            return
        if new_cat:
            category = new_cat
        else:
            # choose first category saved or default 'Other'
            cats = get_categories()
            category = cats[0] if cats else 'Other'
        add_expense_record(sel_date.year, sel_date.month, sel_date.day, name, category, amount)
        # clear fields
        scr.ids.exp_name.text = ''
        scr.ids.exp_amount.text = ''
        scr.ids.cat_input.text = ''
        self._selected_date = None
        self.show_message('Expense saved')
        self.refresh_dashboard()

    # ----------------------
    # Dashboard & UI refresh
    # ----------------------
    def refresh_dashboard(self):
        y = self.current_date.year
        m = self.current_date.month
        income, expense, savings = get_totals_for_month(y, m)
        balance = income - expense
        # update labels
        dash = self.root.get_screen('dashboard')
        dash.ids.lbl_income.text = f'Income: PKR {income:,.2f}'
        dash.ids.lbl_expense.text = f'Total Expense: PKR {expense:,.2f}'
        dash.ids.lbl_balance.text = f'Balance: PKR {balance:,.2f}'
        dash.ids.lbl_savings.text = f'Savings: PKR {savings:,.2f}'
        # draw category chart
        self.draw_category_chart(y, m)

    def draw_category_chart(self, year, month):
        rows = get_expenses_for_month(year, month)
        if not rows:
            # blank image
            fig = plt.figure(figsize=(4,2.3))
            fig.text(0.5,0.5,'No data for this month',ha='center',va='center')
        else:
            # aggregate per category
            agg = {}
            for r in rows:
                cat = r[4]
                amt = r[5]
                agg[cat] = agg.get(cat, 0) + amt
            labels = list(agg.keys())
            sizes = list(agg.values())
            fig = plt.figure(figsize=(4,2.3))
            ax = fig.add_subplot(111)
            ax.pie(sizes, labels=labels, autopct='%1.0f', startangle=90)
            ax.axis('equal')
        buf = io.BytesIO()
        fig.tight_layout()
        FigureCanvasAgg(fig).print_png(buf)
        buf.seek(0)
        data = buf.read()
        buf.close()
        plt.close(fig)
        # convert png bytes to Kivy texture
        image = self.root.get_screen('dashboard').ids.chart_image
        tex = Texture.create(size=(1,1))
        try:
            tex.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        except Exception:
            # fallback: save to file and set source
            with open('chart_tmp.png','wb') as f:
                f.write(data)
            image.source = 'chart_tmp.png'
            image.reload()
            return
        # If blit_buffer works (may not for raw png bytes), fallback to file
        with open('chart_tmp.png','wb') as f:
            f.write(data)
        image.source = 'chart_tmp.png'
        image.reload()

    # ----------------------
    # Summary
    # ----------------------
    def show_summary(self):
        y = self.current_date.year
        m = self.current_date.month
        income, expense, savings = get_totals_for_month(y, m)
        scr = self.root.get_screen('summary')
        scr.ids.sum_month.text = f'Month: {m}/{y}'
        scr.ids.sum_income.text = f'Total Income: PKR {income:,.2f}'
        scr.ids.sum_expense.text = f'Total Expenses: PKR {expense:,.2f}'
        scr.ids.sum_savings.text = f'Savings: PKR {savings:,.2f}'
        # fill expense list
        scr.ids.expense_list.clear_widgets()
        rows = get_expenses_for_month(y, m)
        total = 0
        for r in rows:
            yyyy,mm,dd,name,cat,amt = r
            total += amt
            item = OneLineListItem(text=f'{yyyy}-{mm:02d}-{dd:02d}  {name}  [{cat}]  PKR {amt:,.2f}')
            scr.ids.expense_list.add_widget(item)
        # add total label
        item = OneLineListItem(text=f'TOTAL EXPENSE: PKR {total:,.2f}')
        scr.ids.expense_list.add_widget(item)

    # ----------------------
    # Savings
    # ----------------------
    def show_savings(self):
        scr = self.root.get_screen('savings')
        y = self.current_date.year
        m = self.current_date.month
        income, expense, savings = get_totals_for_month(y, m)
        scr.ids.sav_month.text = f'Month: {m}/{y}'
        scr.ids.sav_value.text = f'This month savings: PKR {savings:,.2f}'
        scr.ids.savings_list.clear_widgets()
        months = get_months_list()
        for (yy,mm,inc,sav) in months:
            item = OneLineListItem(text=f'{mm}/{yy}  Income: PKR {inc:,.2f}  Savings: PKR {sav:,.2f}')
            scr.ids.savings_list.add_widget(item)

    # ----------------------
    # Records (months)
    # ----------------------
    def populate_months_list(self):
        scr = self.root.get_screen('records')
        scr.ids.months_list.clear_widgets()
        months = get_months_list()
        for (yy,mm,inc,sav) in months:
            btn = OneLineListItem(text=f'{mm}/{yy}  Income: PKR {inc:,.2f}  Savings: PKR {sav:,.2f}')
            # when tapped, show that month's summary
            btn.bind(on_release=lambda inst, yy=yy, mm=mm: self.show_month_detail(yy, mm))
            scr.ids.months_list.add_widget(btn)

    def show_month_detail(self, year, month):
        # set current_date to that month and show summary screen
        self.current_date = datetime.date(year, month, 1)
        self.change_screen('summary')

    # ----------------------
    # Balance screen
    # ----------------------
    def show_balance(self):
        y = self.current_date.year
        m = self.current_date.month
        income, expense, savings = get_totals_for_month(y, m)
        scr = self.root.get_screen('balance')
        balance = income - expense
        scr.ids.bal_label.text = f'Current month balance: PKR {balance:,.2f}'
        # create simple bar chart of category expenses
        rows = get_expenses_for_month(y, m)
        if not rows:
            fig = plt.figure(figsize=(4,3))
            fig.text(0.5,0.5,'No expense data',ha='center')
        else:
            agg = {}
            for r in rows:
                cat = r[4]
                amt = r[5]
                agg[cat] = agg.get(cat,0) + amt
            cats = list(agg.keys())
            vals = list(agg.values())
            fig = plt.figure(figsize=(4,3))
            ax = fig.add_subplot(111)
            ax.bar(range(len(cats)), vals)
            ax.set_xticks(range(len(cats)))
            ax.set_xticklabels(cats, rotation=45, ha='right')
            fig.tight_layout()
        buf = io.BytesIO()
        FigureCanvasAgg(fig).print_png(buf)
        buf.seek(0)
        data = buf.read()
        buf.close()
        with open('bal_chart.png','wb') as f:
            f.write(data)
        scr.ids.bal_chart.source = 'bal_chart.png'
        scr.ids.bal_chart.reload()
        plt.close(fig)

    # ----------------------
    # Utility
    # ----------------------
    def show_message(self, msg):
        MDDialog(title='Info', text=msg, size_hint=(0.8, None), height=dp(150), buttons=[MDFlatButton(text='OK', on_release=lambda x: x.parent.parent.dismiss())]).open()


if __name__ == '__main__':
    SmartBudgetApp().run()
