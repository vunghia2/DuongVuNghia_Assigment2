import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
import time
from selenium.common.exceptions import NoAlertPresentException
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def close_datepicker_if_visible(driver):
    try:
        # Kiểm tra nếu datepicker đang hiển thị và nhấp ra ngoài để đóng nó
        datepicker = driver.find_element(By.CSS_SELECTOR, ".datepicker-days")
        if datepicker.is_displayed():
            ActionChains(driver).move_by_offset(10, 10).click().perform()
    except NoSuchElementException:
        pass  # Nếu không tìm thấy datepicker, không làm gì cả


def test_submit_contact_form_with_us(driver):
    driver.get("http://127.0.0.1:8000")

    # Kiểm tra xem đã đăng nhập chưa
    try:
        # Kiểm tra nút đăng xuất để xác định trạng thái đăng nhập
        driver.find_element(By.CSS_SELECTOR, ".logout-button")
    except NoSuchElementException:
        # Nếu chưa đăng nhập, thực hiện đăng nhập
        print("Đang tiến hành đăng nhập...")
        driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
        driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
        driver.find_element(By.ID, "password").send_keys("DVNaka1412")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Chờ trang đăng nhập hoàn tất
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))

    # Mở form đặt chỗ
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#reservation"))).click()

    # Điền thông tin vào form
    driver.find_element(By.ID, "name").send_keys("Vũ Nghĩa")
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    driver.find_element(By.ID, 'phone').send_keys("0919159843")

    # Chọn số lượng khách là "5"
    select_guests = Select(driver.find_element(By.ID, "number-guests"))
    select_guests.select_by_value("5")

    driver.find_element(By.ID, "date").send_keys("4/1/2025")

    # Chọn "Dinner" từ menu thời gian
    select_time = Select(driver.find_element(By.ID, "time"))
    select_time.select_by_value("Dinner")

    driver.find_element(By.ID, "message").send_keys("top table")

    # Đảm bảo datepicker không cản trở việc nhấp vào nút
    close_datepicker_if_visible(driver)

    # Nhấp vào nút gửi form
    driver.find_element(By.ID, "form-submit").click()

    # Chờ URL thay đổi đến trang xác nhận đặt chỗ
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/reserve/confirm"))
    assert driver.current_url == "http://127.0.0.1:8000/reserve/confirm"
    print("Form đã được gửi thành công và chuyển đến trang xác nhận.")


def test_submit_contact_form_with_missing_fields(driver):
    driver.get("http://127.0.0.1:8000")

    # Kiểm tra xem đã đăng nhập chưa
    try:
        driver.find_element(By.CSS_SELECTOR, ".logout-button")
    except NoSuchElementException:
        print("Đang tiến hành đăng nhập...")
        driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
        driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
        driver.find_element(By.ID, "password").send_keys("DVNaka1412")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))

    # Mở form đặt chỗ
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#reservation"))).click()

    # Điền một số trường, bỏ qua tên và số điện thoại
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    select_guests = Select(driver.find_element(By.ID, "number-guests"))
    select_guests.select_by_value("5")
    driver.find_element(By.ID, "date").send_keys("4/1/2025")
    select_time = Select(driver.find_element(By.ID, "time"))
    select_time.select_by_value("Dinner")
    driver.find_element(By.ID, "message").send_keys("top table")

    # Đảm bảo datepicker không cản trở việc nhấp vào nút
    close_datepicker_if_visible(driver)

    # Nhấp vào nút gửi form
    driver.find_element(By.ID, "form-submit").click()

    # Kiểm tra sự xuất hiện của thông báo lỗi cho các trường bắt buộc
    try:
        error_message_name = driver.find_element(By.ID, "error-name").text
        error_message_phone = driver.find_element(By.ID, "error-phone").text
        assert "Vui lòng nhập tên" in error_message_name
        assert "Vui lòng nhập số điện thoại" in error_message_phone
        print("Thông báo lỗi xuất hiện khi không điền đủ thông tin bắt buộc.")
    except NoSuchElementException:
        print("Không tìm thấy thông báo lỗi cho các trường bắt buộc.")

    # Kiểm tra xem có alert nào xuất hiện không và đóng alert nếu có
    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        print("Alert xuất hiện yêu cầu nhập lại thông tin bắt buộc.")
        alert.accept()  # Chấp nhận alert nếu có
    except TimeoutException:
        print("Không có alert yêu cầu nhập lại thông tin bắt buộc.")

def test_wrong_email_form_contact_us(driver):
    driver.get("http://127.0.0.1:8000")

    # Kiểm tra xem đã đăng nhập chưa
    try:
        driver.find_element(By.CSS_SELECTOR, ".logout-button")
    except NoSuchElementException:
        print("Đang tiến hành đăng nhập...")
        driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
        driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
        driver.find_element(By.ID, "password").send_keys("DVNaka1412")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))

    # Mở form đặt chỗ
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#reservation"))).click()

    # Điền thông tin vào form
    driver.find_element(By.ID, "name").send_keys("Vũ Nghĩa")
    driver.find_element(By.ID, "email").send_keys("aAAAAAAA")  # Email không hợp lệ
    driver.find_element(By.ID, 'phone').send_keys("0919159843")

    select_guests = Select(driver.find_element(By.ID, "number-guests"))
    select_guests.select_by_value("5")

    driver.find_element(By.ID, "date").send_keys("2025-01-04")
    select_time = Select(driver.find_element(By.ID, "time"))
    select_time.select_by_value("Dinner")

    driver.find_element(By.ID, "message").send_keys("top table")

    close_datepicker_if_visible(driver)

    # Nhấp vào nút gửi form
    driver.find_element(By.ID, "form-submit").click()

    try:
        # Kiểm tra thông báo lỗi dạng inline nếu email không hợp lệ
        error_message = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message"))
        )
        print("Email không hợp lệ:", error_message.text)
    except TimeoutException:
        print("Không có thông báo lỗi inline, kiểm tra alert...")
        try:
            alert = driver.switch_to.alert
            print("Alert message:", alert.text)
        except NoAlertPresentException:
            print("Không có alert nào.")


