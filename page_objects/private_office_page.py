import allure

from helpers import Helpers
from page_objects.base_page import BasePage
from locators.private_office_locators import PrivateOffice as office_locators

class PrivateOfficePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Перейти в личный кабинет")
    def go_to_personal_account(self, password_recovery):
        password_recovery.go_to_personal_account()

    @allure.step("Ввести email")
    def enter_email(self, email):
        self.send_keys(office_locators.EMAIL_INPUT, email)

    @allure.step("Ввести пароль")
    def enter_password(self, password):
        self.send_keys(office_locators.PASSWORD_INPUT, password)

    @allure.step("Нажать на кнопку входа")
    def click_login_button(self):
        self.click_on_element(office_locators.LOGIN_BUTTON)

    @allure.step("Дождаться видимости кнопки создания заказа")
    def wait_for_create_order_button(self):
        self.wait_element_visibility_of_element_located(office_locators.CREATE_ORDER_BUTTON)

    @allure.step("Авторизоваться уникальным пользователем")
    def login(self, create_user, password_recovery):
        self.go_to_personal_account(password_recovery)
        user_date, resp = create_user
        self.enter_email(user_date['email'])
        self.enter_password(user_date['password'])
        self.click_login_button()
        self.wait_for_create_order_button()
        return user_date['email'], user_date['password']

    @allure.step("Авторизоваться")
    def authorization(self, create_user, password_recovery):
        self.go_to_personal_account(password_recovery)
        self.login(create_user, password_recovery)

    @allure.step("Создать заказ")
    def create_order(self, resp):
        helpers = Helpers()
        number = helpers.created_orders(resp)
        number = str(number.json()['order']['number'])
        return number

    @allure.step("Авторизоваться и сделать заказы")
    def auth_and_change_order(self, create_user, password_recovery):
        user_date, resp = create_user
        self.authorization(create_user, password_recovery)
        number = self.create_order(resp)
        return user_date['email'], user_date['password'], number

    @allure.step("Дождаться видимости кнопки истории заказов")
    def wait_for_history_order_button(self):
        self.wait_element_visibility_of_element_located(office_locators.HISTORY_ORDER)

    @allure.step("Нажать на кнопку истории заказов")
    def click_history_order_button(self):
        self.click_on_element(office_locators.HISTORY_ORDER)

    @allure.step("Открыть личный кабинет и тапнуть по истории заказов")
    def open_history_orders(self, password_recovery):
        self.go_to_personal_account(password_recovery)
        self.wait_for_history_order_button()
        self.click_history_order_button()
        self.wait_for_history_order_button()
        return self.get_current_url()

    @allure.step("Дождаться видимости кнопки выхода")
    def wait_for_logout_button(self):
        self.wait_element_visibility_of_element_located(office_locators.LOGOUT_BUTTON)

    @allure.step("Нажать на кнопку выхода")
    def click_logout_button(self):
        self.click_on_element(office_locators.LOGOUT_BUTTON)

    @allure.step("Дождаться видимости кнопки входа")
    def wait_for_login_button(self):
        self.wait_element_visibility_of_element_located(office_locators.LOGIN_BUTTON)

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.wait_for_logout_button()
        self.click_logout_button()
        self.wait_for_login_button()
        return self.get_current_url()
