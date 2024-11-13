import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time  # Thêm import cho thư viện time


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_log_out(driver):
    driver.get("http://127.0.0.1:8000")

    # Nhấp vào liên kết để chuyển đến trang đăng nhập
    driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()

    # Nhập thông tin đăng nhập
    driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("DVNaka1412")
    print("Password entered:", password_input.get_attribute("value"))

    # Nhấn nút đăng nhập
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)  # Chờ để trang tải xong

    # Nhấp vào nút hiển thị tên người dùng (Vũ Nghĩa)
    try:
        user_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Vũ Nghĩa')]")
        user_button.click()
        time.sleep(2)  # Chờ một chút sau khi nhấp
    except NoSuchElementException:
        print("User button not found.")

    # Thực hiện thao tác đăng xuất
    try:
        # Nhấp vào nút đăng xuất
        logout_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Log Out')]")
        logout_button.click()
        time.sleep(5)  # Chờ một chút để đảm bảo trang tải xong
    except NoSuchElementException:
        print("Logout button not found.")

    # Kiểm tra xem đã chuyển đến trang nào sau khi đăng xuất
    current_url = driver.current_url
    print("Current URL after logout:", current_url)  # In ra URL hiện tại

    # Kiểm tra xem URL có phải là trang chính không
    assert current_url == "http://127.0.0.1:8000/", \
        f"Expected URL to be 'http://127.0.0.1:8000/' but got '{current_url}'"



