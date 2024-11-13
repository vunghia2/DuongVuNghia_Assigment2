
import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import time
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
def test_registter(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".ml-4.text-sm.text-gray-700.underline").click()
    driver.find_element(By.ID, "name").send_keys("aka")
    driver.find_element(By.ID, "email").send_keys("duongvunghia7a1@gmail.com")
    driver.find_element(By.XPATH, '//input[@name="phone"]').send_keys("0919159845")

    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.ID, "password_confirmation").send_keys("123456789")
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(10)
    assert driver.current_url == "http://127.0.0.1:8000/login"

def test_missing_required_fields(driver):
    driver.get("http://127.0.0.1:8000")

    # Nhấp vào liên kết để chuyển đến trang đăng ký
    driver.find_element(By.CSS_SELECTOR, ".ml-4.text-sm.text-gray-700.underline").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Điền các trường không đầy đủ (bỏ trống 'name' và 'password_confirmation')
    driver.find_element(By.ID, "email")
    driver.find_element(By.XPATH, '//input[@name="phone"]').send_keys("0919159845")
    driver.find_element(By.ID, "password").send_keys("123456789")

    time.sleep(2)  # Chờ một chút để kiểm tra trước khi gửi form

    # Nhấn nút "submit" mà không điền đủ các trường bắt buộc
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)

    # Kiểm tra nếu người dùng vẫn ở trang đăng ký do lỗi không nhập đầy đủ thông tin
    current_url = driver.current_url
    assert current_url == "http://127.0.0.1:8000/register", f"URL has changed unexpectedly to {current_url}"

    # Kiểm tra xem có thông báo lỗi cụ thể nào hiển thị không (tùy chọn)
    try:
        # Giả định rằng có thông báo lỗi hiển thị với selector là `.error-message-selector`
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-selector")  # Thay `.error-message-selector` bằng CSS selector thực tế
        assert "Please fill out this field" in error_message.text
        print("Error message displayed as expected.")
    except NoSuchElementException:
        print("No specific error message displayed for missing required fields.")

    # Kiểm tra validity của trường `name` và `password_confirmation`
    try:
        name_input = driver.find_element(By.ID, "name")
        if not name_input.get_property("validity")["valid"]:
            print("Error: 'Please fill out this field' displayed for name field.")
    except NoSuchElementException:
        print("Name field validation not found.")

    try:
        password_confirmation_input = driver.find_element(By.ID, "password_confirmation")
        if not password_confirmation_input.get_property("validity")["valid"]:
            print("Error: 'Please fill out this field' displayed for password confirmation field.")
    except NoSuchElementException:
        print("Password confirmation field validation not found.")


def test_duplicate_email_register(driver):
    driver.get("http://127.0.0.1:8000")

    # Nhấp vào liên kết để chuyển đến trang đăng ký
    driver.find_element(By.CSS_SELECTOR, ".ml-4.text-sm.text-gray-700.underline").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Nhập thông tin người dùng
    driver.find_element(By.ID, "name").send_keys("aka")
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")  # Đảm bảo email này đã được đăng ký trước
    driver.find_element(By.XPATH, '//input[@name="phone"]').send_keys("0919159845")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.ID, "password_confirmation").send_keys("123456789")

    time.sleep(2)  # Chờ một chút trước khi nhấn nút gửi
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)  # Chờ để thông báo lỗi xuất hiện

    # Kiểm tra xem có thông báo lỗi hiển thị không
    try:
        error_message = driver.find_element(By.CSS_SELECTOR, ".alert")  # Chọn selector cho thông báo lỗi
        assert "Email already registered" in error_message.text, "Error message not displayed as expected."
        print("Error message displayed as expected:", error_message.text)
    except NoSuchElementException:
        print("No specific error message displayed for duplicate email.")
def test_duplicate_phone_register(driver):
    driver.get("http://127.0.0.1:8000")

    # Nhấp vào liên kết để chuyển đến trang đăng ký
    driver.find_element(By.CSS_SELECTOR, ".ml-4.text-sm.text-gray-700.underline").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Nhập thông tin người dùng
    driver.find_element(By.ID, "name").send_keys("aka")
    driver.find_element(By.ID, "email").send_keys("duongvunghia7a1@gmail.com")  # Đảm bảo email này đã được đăng ký trước
    driver.find_element(By.XPATH, '//input[@name="phone"]').send_keys("0919159843")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.ID, "password_confirmation").send_keys("123456789")

    time.sleep(2)  # Chờ một chút trước khi nhấn nút gửi
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)  # Chờ để thông báo lỗi xuất hiện

    # Kiểm tra xem có thông báo lỗi hiển thị không
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert")))
        error_message = driver.find_element(By.CSS_SELECTOR, ".alert")
        assert "Phone already registered !" in error_message.text, "Error message not displayed as expected."
        print("Error message displayed as expected:", error_message.text)
    except NoSuchElementException:
        print("No specific error message displayed for duplicate phone.")


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
import time


def test_register_password_too_short_duplicate(driver):
    driver.get("http://127.0.0.1:8000")

    # Nhấp vào liên kết để chuyển đến trang đăng ký
    try:
        driver.find_element(By.CSS_SELECTOR, ".ml-4.text-sm.text-gray-700.underline").click()
    except ElementClickInterceptedException:
        print("Không thể nhấp vào phần tử đăng ký, phần tử khác che khuất.")

    # Chờ để chắc chắn trang đăng ký đã tải
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Nhập thông tin người dùng
    driver.find_element(By.ID, "name").send_keys("aka")
    driver.find_element(By.ID, "email").send_keys(
        "duongvunghia7a1@gmail.com")  # Đảm bảo email này đã được đăng ký trước
    driver.find_element(By.XPATH, '//input[@name="phone"]').send_keys("0919159845")
    driver.find_element(By.ID, "password").send_keys("1234")  # Mật khẩu quá ngắn
    driver.find_element(By.ID, "password_confirmation").send_keys("1234")  # Mật khẩu xác nhận

    time.sleep(2)  # Chờ một chút trước khi nhấn nút gửi

    # Nhấn nút "Đăng ký"
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Chờ để đảm bảo preloader đã biến mất (nếu có)
    try:
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "preloader")))
    except TimeoutException:
        print("Preloader không biến mất kịp thời. Kiểm tra lại.")

    # Kiểm tra thông báo lỗi nếu mật khẩu quá ngắn
    try:
        # Đợi phần tử lỗi xuất hiện
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='text-red-500 text-xs mt-2']"))
        ).text
        print(f"Lỗi: {error_message}")  # In ra lỗi nếu có
    except NoSuchElementException as e:
        print(f"Không tìm thấy thông báo lỗi: {e}")

    time.sleep(5)  # Chờ để thông báo lỗi xuất hiện

    # Kiểm tra lại nếu có cần nhấp lại vào phần tử đăng ký
    try:
        driver.find_element(By.CSS_SELECTOR, ".ml-4.text-sm.text-gray-700.underline").click()
    except ElementClickInterceptedException:
        print("Không thể nhấp lại vào phần tử đăng ký, thử lại.")
    except NoSuchElementException:
        print("Không thể tìm thấy phần tử đăng ký, vui lòng kiểm tra lại cấu trúc HTML.")

