import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


@pytest.fixture(scope="class")
def browser(request):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    request.cls.browser = browser
    yield browser
    browser.quit()

@pytest.fixture(scope="class")
def base_url():
    return os.environ.get('URL', "http://localhost/BadCRUD")

@pytest.mark.usefixtures("browser")
class TestContactManagement:
    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        self.url = base_url

    def login(self):
        self.browser.get(f"{self.url}/login.php")
        self.browser.find_element(By.ID, "inputUsername").send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_1_add_new_contact(self):
        self.login()
        self.browser.find_element(By.CSS_SELECTOR, '.btn.btn-primary.create-contact').click()
        self.browser.find_element(By.ID, 'name').send_keys("John Doe")
        self.browser.find_element(By.ID, 'email').send_keys("john.doe@example.com")
        self.browser.find_element(By.ID, 'phone').send_keys("123456789")
        self.browser.find_element(By.ID, 'title').send_keys("Developer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_2_delete_contact(self):
        self.login()
        self.browser.find_element(By.CSS_SELECTOR, '.btn.btn-sm.btn-outline.btn-danger').click()
        alert = self.browser.switch_to.alert
        alert.accept()
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_3_change_profile_picture(self):
        self.login()
        self.browser.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary[href="profil.php"]').click()
        file_path = os.path.join(os.getcwd(), 'tests','image_test.jpg')
        self.browser.find_element(By.ID, 'formFile').send_keys(file_path)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        assert self.browser.current_url == f"{self.url}/profil.php"

    def test_4_update_contact(self):
        self.login()
        elements = self.browser.find_elements(By.CSS_SELECTOR, 'a.btn-outline.btn-success')
        if elements:
            elements[-1].click()
        self.browser.find_element(By.ID, 'name').clear()
        self.browser.find_element(By.ID, 'name').send_keys("Jane Doe")
        self.browser.find_element(By.ID, 'email').clear()
        self.browser.find_element(By.ID, 'email').send_keys("jane.doe@example.com")
        self.browser.find_element(By.ID, 'phone').clear()
        self.browser.find_element(By.ID, 'phone').send_keys("987654321")
        self.browser.find_element(By.ID, 'title').clear()
        self.browser.find_element(By.ID, 'title').send_keys("Designer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        assert self.browser.current_url == f"{self.url}/index.php"

    def test_5_test_xss_security(self):
        self.login()
        self.browser.find_element(By.CSS_SELECTOR, 'a.btn.btn-warning[href="xss.php"]').click()
        self.browser.find_element(By.NAME, 'thing').send_keys("<script>alert(1)</script>")
        self.browser.find_element(By.NAME, 'submit').click()
        
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
            pytest.fail("XSS vulnerability detected!")
        except:
            raise pytest.fail.Exception("XSS vulnerability detected!")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
