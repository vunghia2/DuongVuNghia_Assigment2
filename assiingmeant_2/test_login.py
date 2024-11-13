import time
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
import time  # Thêm import cho thư viện time



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Test log in
def test_valid_login(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("DVNaka1412")
    print("Password entered:", password_input.get_attribute("value"))
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(10)
    # Sử dụng WebDriverWait thay vì time.sleep()
    #WebDriverWait(driver, 30).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))

    # Kiểm tra URL
    assert driver.current_url == "http://127.0.0.1:8000/redirects"


def test_invalid_login(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("DVNaka")  # Mật khẩu sai
    print("Password entered:", password_input.get_attribute("value"))

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Chờ thông báo lỗi xuất hiện
    try:
        # Chờ cho thông báo lỗi hiển thị
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".font-medium.text-red-600")))  # Thay đổi selector nếu cần

        # Lấy thông báo lỗi và in ra
        error_message_header = driver.find_element(By.CSS_SELECTOR, ".font-medium.text-red-600").text
        error_message_detail = driver.find_element(By.CSS_SELECTOR,
                                                   "ul.mt-3.list-disc.list-inside.text-sm.text-red-600").text

        print("Error message header:", error_message_header)
        print("Error message detail:", error_message_detail)

        # Kiểm tra xem thông báo lỗi có chính xác không
        assert error_message_header == "Whoops! Something went wrong."
        assert "These credentials do not match our records." in error_message_detail
        print("Test passed: Error messages are correct.")
    except Exception as e:
        print("Error message not found or test failed:", e)
        print("Current URL:", driver.current_url)
        print("Page Source:", driver.page_source)  # In ra toàn bộ mã HTML của trang
        assert False  # Đánh dấu bài kiểm thử là thất bại nếu không tìm thấy thông báo lỗi
def test_invalid_login_name(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Nhập địa chỉ email
    driver.find_element(By.ID, "email").send_keys("vdnghia2gmail.com")

    # Nhập mật khẩu
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("DVNaka1412")
    print("Password entered:", password_input.get_attribute("value"))

    # Nhấn nút đăng nhập
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Sử dụng WebDriverWait để chờ cho URL thay đổi
    try:
        WebDriverWait(driver, 5).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))

        # Kiểm tra URL sau khi đăng nhập
        assert driver.current_url == "http://127.0.0.1:8000/redirects"
        print("Login successful, redirected to:", driver.current_url)

    except Exception as e:
        print("Login failed or URL did not change:", e)

        # Xử lý alert nếu có
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert  # Chuyển đổi điều khiển sang alert
            print("Alert text:", alert.text)  # In ra nội dung alert
            alert.accept()  # Chấp nhận alert
            print("Alert accepted successfully.")
        except NoAlertPresentException:
            print("No alert was present.")
        except UnexpectedAlertPresentException:
            print("Unexpected alert is present.")
        except Exception as alert_exception:
            print("An error occurred while handling the alert:", alert_exception)

# Gọi hàm test_valid_login ở nơi thích hợp trong mã kiểm thử của bạn
def test_for_missing_password(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Chỉ nhập email mà không nhập mật khẩu
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("vdnghia2@gmail.com")
    print("Email entered:", email_input.get_attribute("value"))

    # Nhấn nút đăng nhập mà không nhập mật khẩu
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Chờ một chút trước khi kiểm tra trường mật khẩu
    time.sleep(2)  # Chờ 2 giây (hoặc thời gian bạn muốn)

    # Kiểm tra validity của trường mật khẩu
    password_input = driver.find_element(By.ID, "password")
    if not password_input.get_property("validity")["valid"]:
        print("Error: 'Please fill out this field' displayed for password field.")
    else:
        print("Password field is valid.")

    # Xác minh rằng URL vẫn là /login nếu có lỗi
    current_url = driver.current_url
    assert current_url == "http://127.0.0.1:8000/login", f"URL has changed unexpectedly to {current_url}"

    # Kiểm tra xem có thông báo lỗi cụ thể nào hiển thị không (tùy chọn)
    try:
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-selector")  # Thay `.error-message-selector` bằng CSS selector thực tế của thông báo lỗi nếu có
        assert "Please fill out this field" in error_message.text
        print("Error message displayed as expected.")
    except NoSuchElementException:
        print("No specific error message displayed for missing password.")


