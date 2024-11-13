import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import time  # Thêm thư viện time để sử dụng hàm sleep
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_to_cart_but_out_of_stock(driver):
    # Truy cập trang chủ
    driver.get("http://127.0.0.1:8000")

    try:
        # Nhấn vào liên kết Menu
        menu_link = driver.find_element(By.CSS_SELECTOR, "a[href='/#menu']")
        menu_link.click()

        # Chờ phần tử menu tải
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card")))

        # Kiểm tra xem món "Blueberry Cake" có trong menu không
        blueberry_card = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@style, 'background-image: url( \"http://127.0.0.1:8000/assets/images/menu-item-04.jpg\" )')]")
        ))

        # Di chuyển đến card của Blueberry Cake (để đảm bảo trang có thể tương tác với phần tử)
        ActionChains(driver).move_to_element(blueberry_card).perform()

        # Kiểm tra trạng thái của nút "Add to Cart"
        add_to_cart_button = blueberry_card.find_element(By.CSS_SELECTOR,
                                                         "input[type='submit'][class='btn btn-success']")

        # Đảm bảo nút "Add to Cart" có thể nhấn
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(add_to_cart_button))

        if add_to_cart_button.is_enabled():
            # Nếu nút không bị vô hiệu hóa, nhấn nút
            add_to_cart_button.click()

            # Chờ một chút để đảm bảo hành động hoàn thành
            WebDriverWait(driver, 5).until(EC.alert_is_present())  # Giả sử sau khi click sẽ có thông báo

            # In ra thông báo thành công
            print("Sản phẩm 'Blueberry Cake' đã được thêm vào giỏ hàng!")
        else:
            print("Sản phẩm hiện tại không thể thêm vào giỏ hàng (Out of Stock).")

    except NoSuchElementException:
        print("Lỗi: Không tìm thấy phần tử cần thiết trên trang.")
    except TimeoutException:
        print("Lỗi: Thời gian tải trang hoặc phần tử đã hết.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

def test_add_to_cart(driver):
        # Truy cập trang chủ
        driver.get("http://127.0.0.1:8000")

        try:
            # Thực hiện đăng nhập
            driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
            driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
            password_input = driver.find_element(By.ID, "password")
            password_input.send_keys("DVNaka1412")
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            # Đợi trang chuyển hướng sau đăng nhập
            WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
            print("Đăng nhập thành công!")

            # Truy cập menu
            browse_all_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='/menu']//input[@type='submit'][@value='Browse All']"))
            )
            browse_all_button.click()

            # Chờ cho đến khi phần tử của sản phẩm "Chocolate Cake" xuất hiện
            chocolate_cake_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
                (By.XPATH, "//h2[text()='Chocolate Cake']/following-sibling::form//button[@class='btn btn-success']")
            ))

            # Nhấn trực tiếp vào nút "Add to Cart" cho Chocolate Cake
            ActionChains(driver).move_to_element(chocolate_cake_button).click().perform()

            # Chờ giỏ hàng được cập nhật
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, "lblCartCount"), "1")
            )

            # Kiểm tra số lượng trong giỏ hàng
            cart_count = driver.find_element(By.ID, "lblCartCount").text.strip()
            print(f"Sản phẩm 'Chocolate Cake' đã được thêm vào giỏ hàng. Cart count hiện tại: {cart_count}")

            # Giữ trình duyệt ở lại trang lâu hơn để có thể kiểm tra
            time.sleep(10)  # Dừng lại 10 giây trước khi đóng, điều chỉnh thời gian nếu cần

        except NoSuchElementException as e:
            print(f"Lỗi: Không tìm thấy phần tử cần thiết trên trang. {e}")
        except TimeoutException as e:
            print(f"Lỗi: Thời gian tải trang hoặc phần tử đã hết. {e}")
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")


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


def test_checkout_process(driver):
    driver.get("http://127.0.0.1:8000")

    try:
        # Step 1: Perform login
        driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
        driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
        driver.find_element(By.ID, "password").send_keys("DVNaka1412")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for redirect after successful login
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
        print("Login successful!")

        # Step 2: Open cart
        cart_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa.fa-shopping-cart"))
        )
        cart_icon.click()

        # Wait for cart page to load
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/cart"))
        print("Cart page opened.")

        # Step 3: Click Checkout button
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success"))
        )
        checkout_button.click()

        # Wait for checkout page to load
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/checkout/270"))
        print("Checkout page opened.")

        # Step 4: Select payment method (Cash on Delivery) using its id
        payment_method = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cod"))
        )
        payment_method.click()

        # Step 5: Click "Place Order" button
        place_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-success[type='submit']"))
        )
        place_order_button.click()

        # Wait for redirected page to load
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/mails/shipped/270"))
        print("Order placement page opened.")

        # Step 6: Fill in shipping information
        driver.find_element(By.ID, "address").send_keys("93 B, New Eskaton Road")
        driver.find_element(By.ID, "address2").send_keys("Apartment 10B")

        country_select = driver.find_element(By.ID, "country")
        country_select.click()
        country_option = driver.find_element(By.CSS_SELECTOR, "option[value='Bangladesh']")
        country_option.click()

        state_select = driver.find_element(By.ID, "state")
        state_select.click()
        state_option = driver.find_element(By.CSS_SELECTOR, "option[value='Dhaka']")
        state_option.click()

        driver.find_element(By.ID, "zip").send_keys("700000")

        # Step 7: Confirm the order
        confirm_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        confirm_order_button.click()

        # Final confirmation page
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/confirm_place_order/270"))
        print("Order confirmed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")











