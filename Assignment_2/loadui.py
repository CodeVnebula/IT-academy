from PyQt5.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QWidget, 
    QStackedWidget, 
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QComboBox,
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import sys
import requests
from pympler import asizeof
import os

USERNAME = "admin"
PASSWORD = "admin"

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        
        img_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "icons/favicon.png"
        )
        self.setWindowIcon(QIcon(img_path))

        ui_file = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "app.ui"
        )
        uic.loadUi(ui_file, self)
        
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        
        self.login_page = self.findChild(QWidget, "login_page")
        self.currency_converter_page = self.findChild(QWidget, 
                                                      "currency_converter",
                                                      )
        
        self.stackedWidget.setCurrentWidget(self.login_page)
        
        self.username_entry = self.findChild(QLineEdit, "username_input_line")
        self.password_entry = self.findChild(QLineEdit, "password_input_line")
        self.authorize_button = self.findChild(QPushButton, 
                                               "authorisation_btn",
                                               )
        
        self.authorize_button.clicked.connect(self.authorisation)
        
        self.show()
        
    def authorisation(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
            
        if username == USERNAME and password == PASSWORD:
            self.stackedWidget.setCurrentWidget(self.currency_converter_page)
            
            self.currency_converter = CurrencyConverter(self)
            
        else:
            self.wrong_cretentials_label = self.findChild(
                QLabel, "wrong_credentials_label",
            )
            
            wrong_credentials_message = (
                "არასწორი სახელი ან პაროლი! სცადეთ ხელახლა."
            )
            self.wrong_credentials_label.setText(wrong_credentials_message)
            self.wrong_cretentials_label.setStyleSheet("color: red;")
            
            self.username_entry.clear()
            self.password_entry.clear()
    
    
class CurrencyConverter:
    __ALL_CURRENCIES_ADDRESS = (
        "https://cdn.jsdelivr.net/npm/"
        "@fawazahmed0/currency-api@latest/v1/currencies.json"
    )
    __EACH_CURRENCY_ADDRESS = __ALL_CURRENCIES_ADDRESS.replace(
        '.json', ''
    ) + '/{currency_code}.json'
    __DEFAULT_FROM_CURRENCY = "USD"
    __DEFAULT_TO_CURRENCY = "GEL"
    __DEFAULT_FROM_CRYPTO = "BTC"
    __DEFAULT_TO_CRYPTO = "ETH"
    __MAX_AMOUNT = 1_000_000_000
    
    # This list contains ISO 4217 currency codes for various countries, 
    # including both current and former codes.

    country_currency_codes = {
        "aed", "afn", "all", "amd", "ang", "aoa", "ars", "ats", "aud", "awg",
        "bam", "bbd", "bdt", "bef", "bgn", "bhd", "bif", "bmd", "bnd", "bob",
        "brl", "bsd", "bsv", "btn", "bwp", "byn", "byr", "bzd", "cad", "cake",
        "cdf", "celo", "chf", "clp", "cnh", "cny", "cop", "crc", "cuc", "cup",
        "cve", "cyp", "czk", "dai", "dash", "dcr", "djf", "dkk", "doge", "dop",
        "dot", "dydx", "dzd", "egp", "ern", "esp", "etb", "eur", "fjd", "fkp",
        "gel", "ghs", "gip", "gmd", "gnf", "grd", "gtq", "gyd", "hkd", "hnl",
        "htg", "huf", "idr", "iep", "ils", "imp", "inr", "iqd", "irr", "isk",
        "jep", "jmd", "jod", "jpy", "kes", "kgs", "khr", "kmf", "kpw", "krw",
        "kwd", "kyd", "kzt", "lak", "lbp", "lkr", "lrd", "lsl", "ltc", "mad",
        "mdl", "mga", "mgf", "mkd", "mkr", "mmk", "mnt", "mop", "mro", "mru",
        "mtl", "mur", "mvr", "mwk", "mxn", "myr", "mzm", "nad", "ngn", "nio",
        "nok", "npr", "nzd", "omr", "pab", "pen", "pgk", "php", "pkr", "pln",
        "pte", "pyg", "qar", "ron", "rsd", "rub", "sbd", "scr", "sdg", "sek",
        "sgd", "shp", "skk", "sll", "sos", "srd", "stn", "svc", "syp", "szl",
        "thb", "tjs", "tmt", "tnd", "top", "trl", "try", "ttd", "tvd", "twd",
        "tzs", "uah", "ugx", "usd", "uyu", "uzs", "vnd", "vuv", "wst", "xaf",
        "xag", "xau", "xcd", "xof", "xpf", "xpt", "yer", "zar", "zmk", "zmw",
        "zwd", "zwl", "azm", "azn", "dem", "eek", "fim", "frf", "gbp", "ggp",
        "ghc", "hrk", "itl", "ltl", "luf", "lvl", "lyd", "mzn", "nlg", "rol",
        "rwf", "sar", "sdd", "sit", "spl", "srg", "std", "sle", "tmm", "val",
        "veb", "vef", "ves",
    }

    
    def __init__(self, login_instance):
        self.cached_currencies_data = None
        self.last_request_time = None
        self.login_instance = login_instance
        self.setup_ui()
    
    def setup_ui(self):
        self.currency_type_combobox = self.login_instance.findChild(
            QComboBox, "currency_type_combobox"
        )
        self.from_currency_combobox = self.login_instance.findChild(
            QComboBox, "from_currency_combobox"
        )
        self.to_currency_combobox = self.login_instance.findChild(
            QComboBox, "to_currency_combobox"
        )
        
        self.amount_input_line = self.login_instance.findChild(
            QLineEdit, "amount_input_line"
        )
        self.result_amount = self.login_instance.findChild(
            QLabel, "result_amount"
        )
        self.cache_size = self.login_instance.findChild(QLabel, "cache_size")
        self.date_label = self.login_instance.findChild(QLabel, "date_label")
        
        self.convert_button = self.login_instance.findChild(
            QPushButton, "convert_button"
        )
        self.clear_button = self.login_instance.findChild(
            QPushButton, "clear_button"
        )
        self.defaults_button = self.login_instance.findChild(
            QPushButton, "defaults_button"
        )
        self.logout_button = self.login_instance.findChild(
            QPushButton, "logout_button"
        )
        
        self.cache_size.setText('0.0 MB')
        self.cache_size.setStyleSheet('color: green;')
        
        self.data = self.get_all_currencies()
       
        self.fill_currency_comboboxes_with_currencies(data = self.data)
        self.currency_type_combobox.currentIndexChanged.connect(
            self.fill_currency_comboboxes
        )  
          
        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_entries)
        self.defaults_button.clicked.connect(self.set_defaults)
        self.logout_button.clicked.connect(self.logout)
        
        
        
    def get_all_currencies(self):
        response = requests.get(self.__ALL_CURRENCIES_ADDRESS)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def fill_currency_comboboxes(self):
        if self.currency_type_combobox.currentIndex() == 0:
            self.fill_currency_comboboxes_with_currencies()
            print("Currency comboboxes filled with all currencies values!")
        elif self.currency_type_combobox.currentIndex() == 1:
            data = {code: name for code, name in self.data.items() 
                    if code in self.country_currency_codes}
            self.fill_currency_comboboxes_with_currencies(data)
            print("Currency comboboxes filled with countries currencies only!")
        else:
            data = {code: name for code, name in self.data.items() 
                    if code not in self.country_currency_codes and name}
            self.fill_currency_comboboxes_with_currencies(
                data, self.__DEFAULT_FROM_CRYPTO, self.__DEFAULT_TO_CRYPTO
            )
            print("Currency comboboces filled with cryptocurencies only!")
            
    def fill_currency_comboboxes_with_currencies(self, data=None, 
                                                 def_from_currency=None, 
                                                 def_to_currency=None):
        if data is None:
            data = self.data
        if def_from_currency is None:
            def_from_currency = self.__DEFAULT_FROM_CURRENCY
        if def_to_currency is None:
            def_to_currency = self.__DEFAULT_TO_CURRENCY

        self.from_currency_combobox.clear()
        self.to_currency_combobox.clear()
        
        self.currency_codes = [key.upper() for key in data.keys()]
        self.currency_names = list(data.values())
        items = [f'{code} - {name}' for code, name in zip(self.currency_codes, 
                                                          self.currency_names)]
        self.from_currency_combobox.addItems(items)
        self.to_currency_combobox.addItems(items)
            
        self.from_index = self.currency_codes.index(def_from_currency)
        self.from_currency_combobox.setCurrentIndex(self.from_index)
            
        self.to_index = self.currency_codes.index(def_to_currency)
        self.to_currency_combobox.setCurrentIndex(self.to_index) 

    def convert_currency(self):
        to_currency_code = self.to_currency_combobox.currentText()
        to_currency_code = to_currency_code.split('-')[0].strip()
        from_currency_code = self.from_currency_combobox.currentText()
        from_currency_code = from_currency_code.split('-')[0].strip()
        
        print("Converting function called!")
        print(f"   From currency code - {from_currency_code}")
        print(f"   To currency code - {to_currency_code}")
        
        inputted_amount_text = self.amount_input_line.text()
        
        try:
            inputted_amount_text = float(inputted_amount_text)
            self.result_amount.clear()
        except ValueError:
            self.result_amount.setText('შეიყვანეთ რიცხვი!')
            self.result_amount.setStyleSheet('color: red;')
            return None
        
        if inputted_amount_text <= 0 or inputted_amount_text > self.__MAX_AMOUNT:
            self.result_amount.setText("თანხა დიაპაზონის გარეთაა!")
            self.result_amount.setStyleSheet('color: red;')
        elif from_currency_code == to_currency_code:
            self.result_amount.setText(
                f'{str(inputted_amount_text)} {to_currency_code}'
            )
            self.result_amount.setStyleSheet('color: green;')
        else:
            from_currency_code_lower = from_currency_code.lower()
            to_currency_code_lower = to_currency_code.lower()
            
            from_currency_address = self.__EACH_CURRENCY_ADDRESS.format(
                currency_code = from_currency_code_lower
            )
            to_currency_address = self.__EACH_CURRENCY_ADDRESS.format(
                currency_code = to_currency_code_lower
            )
            
            if not self.cached_currencies_data:
                self.cached_currencies_data = {}
                
            if from_currency_code_lower not in self.cached_currencies_data:
                response_from_currency = requests.get(from_currency_address)
                if response_from_currency.status_code == 200:
                    from_currency_data = response_from_currency.json()
                    self.cached_currencies_data[from_currency_code_lower] = (
                        from_currency_data
                    )
                    print("Request sent for 'From' currency! Data added to cache.")
                else:
                    return None
            
            if to_currency_code_lower not in self.cached_currencies_data:
                response_to_currency = requests.get(to_currency_address)
                if response_to_currency.status_code == 200:
                    to_currency_data = response_to_currency.json()
                    self.cached_currencies_data[to_currency_code_lower] = (
                        to_currency_data
                    )
                    print("Request sent for 'To' currency! Data added to cache.")
                else:
                    return None
            
            result = (
                self.cached_currencies_data[from_currency_code_lower]
                [from_currency_code_lower][to_currency_code_lower]
                * inputted_amount_text
            )
            result = f"{result:.4f}"
        
            self.result_amount.setText(f'{str(result)} {to_currency_code}')
            self.result_amount.setStyleSheet('color: green;')
            
            date = self.cached_currencies_data[from_currency_code_lower]['date']
            self.date_label.setText(f"{date}-ის შედეგი")
            self.date_label.setStyleSheet('color: green;')

        size_in_megabytes = (
            asizeof.asizeof(self.cached_currencies_data)
            / (1024 ** 2)
        )

        self.cache_size.setText(f"{size_in_megabytes:.6f} MB")
        self.cache_size.setStyleSheet('color: red;')
            
        print("Currency converted successfully")
    
    def clear_entries(self):
        self.amount_input_line.clear()
        self.result_amount.clear()
        self.date_label.clear()
        print("Entries cleared")
    
    def set_defaults(self):
        self.clear_entries()
        self.currency_type_combobox.setCurrentIndex(0)
        self.from_currency_combobox.setCurrentIndex(self.from_index)
        self.to_currency_combobox.setCurrentIndex(self.to_index)
        self.cached_currencies_data = {}
        self.cache_size.setText('0.0 MB')
        self.cache_size.setStyleSheet('color: green;')
        print("Settings set to defaults")
        
        
    def logout(self):
        self.set_defaults()
        self.login_instance.stackedWidget.setCurrentWidget(
            self.login_instance.login_page
        )
        self.login_instance.username_entry.clear()
        self.login_instance.password_entry.clear()
        self.login_instance.wrong_credentials_label.clear()
    
    
app = QApplication(sys.argv)
UIWindow = Login()
app.exec_()
