import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
def test_view_cart(driver):
    driver.get("http://127.0.0.1:8000")

    try:
        # Thực hiện đăng nhập
        driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
        driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("DVNaka1412")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Đợi đến khi đăng nhập thành công và trang chuyển hướng
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
        print("Đăng nhập thành công!")

        # Nhấn vào biểu tượng giỏ hàng
        cart_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa.fa-shopping-cart"))
        )
        cart_icon.click()

        # Đợi trang giỏ hàng chuyển hướng đến URL đúng và tải đầy đủ
        WebDriverWait(driver, 60).until(EC.url_to_be("http://127.0.0.1:8000/cart"))

        # Kiểm tra xem có phần tử đặc trưng của trang giỏ hàng (Ví dụ: giỏ hàng trống) để xác nhận trang đã tải xong
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-items"))  # Thay bằng phần tử đặc trưng của giỏ hàng
        )

        print("Giỏ hàng đã được mở tại: http://127.0.0.1:8000/cart")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")