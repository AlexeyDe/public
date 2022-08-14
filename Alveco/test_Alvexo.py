import time
from settings import valid_email, valid_password, valid_name, valid_phone


def test_alvexo1(web_browser):
    # Open base page:
    web_browser.get("https://trader.alvexo.com/login-area-new/sign-up")

    # click on the full name field
    field_full_name = web_browser.find_element_by_name("FirstName")
    field_full_name.clear()
    field_full_name.send_keys(valid_name)

    # add email
    field_email = web_browser.find_element_by_name("Email")
    field_email.clear()
    field_email.send_keys(valid_email)

    # add password
    field_pass = web_browser.find_element_by_name("Password")
    field_pass.clear()
    field_pass.send_keys(valid_password)

    # click checkbox
    checkbox = web_browser.find_element_by_name("Checkbox")
    checkbox.click()

    # click continue button
    continue_button = web_browser.find_element_by_xpath('//*[@id="sign_up_form"]/button')
    continue_button.click()

    # added time-sleep to give browser time to catch new url
    time.sleep(10)

    assert web_browser.current_url == "https://trader.alvexo.com/login-area-new/phone", "error step 1"


def test_alvexo2(web_browser):
    web_browser.get('https://trader.alvexo.com/login-area-new/phone')

    # click on the account type field
    field_account_type = web_browser.find_element_by_xpath('//*[@id="phone_form"]/div[2]/div/div/span/span[1]')
    field_account_type.click()
    field_account_type.click()

    # add phone number
    field_phone = web_browser.find_element_by_name("PhoneNumber")
    field_phone.clear()
    field_phone.send_keys(valid_phone)

    # click sign up button
    signup_button = web_browser.find_element_by_xpath('//*[@id="phone_form"]/button')
    signup_button.click()

    #added time-sleep to give browser time to catch new url
    time.sleep(10)

    assert web_browser.current_url == "https://trader.alvexo.com/dashboard?lang=en", "error step 2"

    if test_alvexo1(web_browser) is True and test_alvexo2(web_browser) is True:
        return 'success'



