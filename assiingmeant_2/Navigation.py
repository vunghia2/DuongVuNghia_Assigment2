import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_see_chef_information_on_social_networking_sites(driver):
    driver.get("http://127.0.0.1:8000")

    try:
        # Kiểm tra nút đăng xuất để xác định trạng thái đăng nhập
        driver.find_element(By.CSS_SELECTOR, ".logout-button")
    except NoSuchElementException:
        # Nếu chưa đăng nhập, thực hiện đăng nhập
        print("Đang tiến hành đăng nhập...")
        driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()

        # Thêm thời gian chờ để làm chậm quá trình (ví dụ: 1 giây trước khi nhập thông tin đăng nhập)
        time.sleep(1)  # Chờ 1 giây

        driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
        driver.find_element(By.ID, "password").send_keys("DVNaka1412")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Chờ trang đăng nhập hoàn tất và chuyển đến trang đầu bếp
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
        driver.find_element(By.CSS_SELECTOR, "#chefs").click()

    # Thêm thời gian chờ giữa các bước sau khi nhấn nút
    time.sleep(1)  # Đợi 1 giây trước khi tìm và nhấn vào biểu tượng Facebook

    # Tìm và nhấn vào biểu tượng Facebook
    try:
        # Dùng WebDriverWait để đợi nút Facebook trở nên có thể nhấn
        facebook_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='https://www.facebook.com/']"))
        )

        # Nhấn nút Facebook
        facebook_icon.click()

        # Đợi cho đến khi số cửa sổ là 2 (một cửa sổ mới mở)
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # Lấy số lượng cửa sổ hiện có và chuyển đến cửa sổ mới
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[-1])  # Chuyển sang cửa sổ mới nhất

        current_url = driver.current_url

        # Kiểm tra URL để đảm bảo chúng ta đã đến trang Facebook
        assert "facebook.com" in current_url, f"Expected Facebook URL, but got {current_url}"

        print("Kiểm tra thành công: Trang Facebook đã được mở.")

        # Dừng lại trên trang Facebook trong 20 giây để đảm bảo trang đã tải hoàn toàn
        time.sleep(20)  # Đợi 20 giây

        # Quay lại cửa sổ chính
        driver.close()  # Đóng cửa sổ Facebook nếu muốn
        driver.switch_to.window(all_windows[0])  # Quay lại cửa sổ gốc

    except NoSuchElementException:
        print("Không tìm thấy biểu tượng Facebook trên trang.")
    except TimeoutException:
        print("Không thể chuyển đến trang Facebook.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")


def test_error_printing_page_logo(driver):
    # Truy cập trang chính
    driver.get("http://127.0.0.1:8000")

    try:
        # Tìm logo và click vào logo
        logo = driver.find_element("class name", "logo")
        logo.click()

        # Chờ một chút sau khi nhấp vào logo để trang có đủ thời gian tải
        time.sleep(5)  # Chờ thêm 5 giây

        # Kiểm tra URL hiện tại - đặt URL sai để kiểm tra lỗi
        expected_url = "http://127.0.0.1:8000/wrong-url"  # URL sai để gây lỗi
        assert driver.current_url == expected_url, f"Không điều hướng đến đúng URL, URL hiện tại là: {driver.current_url}"

        # Chờ phần tử xuất hiện để đảm bảo trang đã tải
        wait = WebDriverWait(driver, 10)  # Chờ tối đa 10 giây
        header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert header is not None, "Trang không tải đúng"

    except NoSuchElementException:
        print("Lỗi: Không tìm thấy phần tử logo hoặc trang không tải đúng")
    except AssertionError as e:
        print("Lỗi: Điều hướng không đúng URL hoặc trang bị lỗi")
        print(e)
    except TimeoutException:
        print("Lỗi: Trang không tải kịp thời")

def test_click_facebook_icon(driver):
    # Truy cập trang chính
    # Truy cập trang chính
    driver.get("http://127.0.0.1:8000")

    try:
        # Thực hiện đăng nhập
        driver.find_element(By.CSS_SELECTOR, ".text-sm.text-gray-700.underline").click()
        time.sleep(1)  # Chờ 1 giây để trang đăng nhập tải

        driver.find_element(By.ID, "email").send_keys("vdnghia2@gmail.com")
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("DVNaka1412")
        print("Password entered:", password_input.get_attribute("value"))

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Chờ cho đến khi trang chuyển hướng sau khi đăng nhập hoàn tất
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:8000/redirects"))
        print("Đăng nhập thành công!")

        # Quay lại trang chính để kiểm tra biểu tượng Facebook
        driver.get("http://127.0.0.1:8000")

        # Cuộn xuống cuối trang
        ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME, "left-text-content")).perform()

        # Chờ cho phần tử icon Facebook xuất hiện
        wait = WebDriverWait(driver, 10)  # Chờ tối đa 10 giây
        facebook_icon = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='https://web.facebook.com/rahathosenmanik/']"))
        )

        # Nhấn vào biểu tượng Facebook
        facebook_icon.click()

        # Chuyển sang tab mới
        driver.switch_to.window(driver.window_handles[-1])

        # Kiểm tra URL hiện tại để xác nhận điều hướng đến trang Facebook
        expected_url = "https://web.facebook.com/rahathosenmanik/"
        assert driver.current_url == expected_url, f"Không điều hướng đến đúng URL Facebook, URL hiện tại là: {driver.current_url}"

        print("Đã điều hướng đến trang Facebook thành công!")

        # Dừng lại 10 giây để giữ lại trang Facebook
        time.sleep(10)

    except NoSuchElementException:
        print("Lỗi: Không tìm thấy phần tử hoặc biểu tượng Facebook.")
    except AssertionError as e:
        print("Lỗi: Điều hướng không đúng URL.")
        print(e)
    except TimeoutException:
        print("Lỗi: Trang không tải kịp thời hoặc không tìm thấy biểu tượng Facebook.")


def test_click_youtube_play_button(driver):
    driver.get("http://127.0.0.1:8000")

    try:
        # Nhấp vào liên kết "About"
        about_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/#about']"))
        )
        about_link.click()

        # Chờ để đảm bảo nội dung trong mục "About" đã tải
        time.sleep(2)  # Có thể thay thế bằng một điều kiện chờ khác nếu có thể

        # Cuộn đến phần chứa nút Play
        thumb_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.thumb"))
        )
        ActionChains(driver).move_to_element(thumb_element).perform()

        # Chờ nút Play xuất hiện và có thể nhấp vào
        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href='https://www.youtube.com/embed/eMF9tfxigGw'] i.fa-play"))
        )

        # Nhấp vào nút Play
        play_button.click()

        # Đợi cho đến khi tab mới mở ra
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # Chuyển sang tab mới nhất
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[-1])

        # Kiểm tra URL để đảm bảo là YouTube
        current_url = driver.current_url
        expected_url = "https://www.youtube.com/embed/eMF9tfxigGw"
        assert expected_url in current_url, f"Expected URL {expected_url}, but got {current_url}"

        print("Đã mở video YouTube thành công!")

        # Giữ tab YouTube mở thêm thời gian (nếu muốn)
        time.sleep(10)

        # Quay lại tab gốc
        driver.close()
        driver.switch_to.window(all_windows[0])

    except NoSuchElementException:
        print("Không tìm thấy nút Play.")
    except TimeoutException:
        print("Không thể mở video YouTube.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")


