from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json

WAITTIME = 1.5


def setupSelenium():
    driver_path = './driver/chromedriver'
    options = Options()
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get("https://npm.cpami.gov.tw/apply_1.aspx")  # 前往這個網址

    ele = driver.find_element_by_css_selector('div.content div.row a[title="玉山國家公園"]')
    ele.click()
    return driver


def check_rule(driver):
    driver.find_element_by_id('chk[]15').click()
    driver.find_element_by_id('chk[]').click()
    driver.find_element_by_id('ContentPlaceHolder1_btnagree').click()


def setup_schedule(driver, data):
    selector = 'input[placeholder="請輸入隊名"]'
    driver.find_element_by_css_selector(selector).send_keys(data['name'])

    select_option(driver, 'ContentPlaceHolder1_climblinemain', data['main_path'])
    select_option(driver, 'ContentPlaceHolder1_climbline', data['sub_path'])
    select_option(driver, 'ContentPlaceHolder1_sumday', data['day'])
    select_option(driver, 'ContentPlaceHolder1_applystart', data['date'])

    select_path(driver, data['paths'])
    select_option(driver, 'ContentPlaceHolder1_teams_count', data['people'])
    driver.find_element_by_id('ContentPlaceHolder1_cbRouteSel').click()


def setup_applicant(driver, applicant):
    driver.find_element_by_id('menuhref1').click()
    sleep(WAITTIME)

    driver.find_element_by_id('ContentPlaceHolder1_applycheck').click()
    sleep(WAITTIME)

    fillin_data(driver, 'ContentPlaceHolder1_apply_name', applicant['name'])
    fillin_data(driver, 'ContentPlaceHolder1_apply_tel', applicant['tel'])

    select_option(driver, 'ContentPlaceHolder1_ddlapply_country', applicant['city'])
    select_option(driver, 'ContentPlaceHolder1_ddlapply_city', applicant['district'])
    fillin_data(driver, 'ContentPlaceHolder1_apply_addr', applicant['address'])

    fillin_data(driver, 'ContentPlaceHolder1_apply_mobile', applicant['mobile'])
    fillin_data(driver, 'ContentPlaceHolder1_apply_email', applicant['mail'])

    select_option(driver, 'ContentPlaceHolder1_apply_nation', '中華民國')
    fillin_data(driver, 'ContentPlaceHolder1_apply_sid', applicant['id'])
    select_option(driver, 'ContentPlaceHolder1_apply_sex', applicant['gender'])

    ele = driver.find_element_by_id('ContentPlaceHolder1_apply_birthday')
    script = 'arguments[0].value="{}"'.format(applicant['birthday'])
    driver.execute_script(script, ele)


def setup_leader(driver, applicant):
    driver.find_element_by_id('menuhref2').click()
    sleep(WAITTIME)

    driver.find_element_by_id('ContentPlaceHolder1_copyapply').click()
    sleep(WAITTIME)

    fillin_data(driver, 'ContentPlaceHolder1_leader_contactname', applicant['urgent_contact']['name'])
    fillin_data(driver, 'ContentPlaceHolder1_leader_contacttel', applicant['urgent_contact']['tel'])


def setup_members(driver, members):
    driver.find_element_by_id('menuhref3').click()
    sleep(WAITTIME)

    driver.find_element_by_id('ContentPlaceHolder1_member_keytype').click()
    sleep(WAITTIME)

    driver.switch_to_alert().accept()
    sleep(WAITTIME)

    for (idx, member) in enumerate(members):
        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_name_' + str(idx), member['name'])
        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_tel_' + str(idx), member['tel'])

        select_option(driver, 'ContentPlaceHolder1_lisMem_ddlmember_country_' + str(idx), member['city'])
        select_option(driver, 'ContentPlaceHolder1_lisMem_ddlmember_city_' + str(idx), member['district'])
        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_addr_' + str(idx), member['address'])

        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_mobile_' + str(idx), member['mobile'])
        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_email_' + str(idx), member['mail'])

        select_option(driver, 'ContentPlaceHolder1_lisMem_member_nation_' + str(idx), '中華民國')
        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_sid_' + str(idx), member['id'])
        select_option(driver, 'ContentPlaceHolder1_lisMem_member_sex_' + str(idx), member['gender'])

        ele = driver.find_element_by_id('ContentPlaceHolder1_lisMem_member_birthday_' + str(idx))
        script = 'arguments[0].value="{}"'.format(member['birthday'])
        driver.execute_script(script, ele)

        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_contactname_' + str(idx), member['urgent_contact']['name'])
        fillin_data(driver, 'ContentPlaceHolder1_lisMem_member_contacttel_' + str(idx), member['urgent_contact']['tel'])


def setup_stay(driver, stay):
    driver.find_element_by_id('menuhref4').click()
    sleep(WAITTIME)

    fillin_data(driver, 'ContentPlaceHolder1_stay_name', stay['name'])
    fillin_data(driver, 'ContentPlaceHolder1_stay_mobile', stay['tel'])


def select_option(driver, selectID, target):
    selector = "#{} option".format(selectID)
    select = driver.find_element_by_id(selectID)
    script = "showDropdown = function (element) {var event; event = document.createEvent('MouseEvents'); event.initMouseEvent('mousedown', true, true, window); element.dispatchEvent(event); }; showDropdown(arguments[0]);"
    driver.execute_script(script, select)

    options = driver.find_elements_by_css_selector(selector)
    for option in options:
        if target in option.text:
            option.click()
            break
    sleep(WAITTIME)


def select_path(driver, paths):
    for path in paths:
        selector = '#ContentPlaceHolder1_rblNode input'
        eles = driver.find_elements_by_css_selector(selector)
        for ele in eles:
            id = ele.get_attribute('id')
            label = driver.find_element_by_css_selector('label[for="{}"]'.format(id))
            if path in label.text:
                ele.click()
                sleep(WAITTIME)
                break
    finish = driver.find_element_by_css_selector('input[value="完成今日路線"]')
    finish.click()
    sleep(WAITTIME)


def fillin_data(driver, element_id, data):
    driver.find_element_by_id(element_id).send_keys(data)


if __name__ == '__main__':
    driver = setupSelenium()
    check_rule(driver)
    member_count = 0
    with open('schdule.json', 'r') as f:
        data = json.load(f)
        setup_schedule(driver, data)
        member_count = int(data['people'])

    with open('member.json', 'r') as f:
        members = json.load(f)
        if len(members) != member_count:
            print('少人了啦')

        setup_applicant(driver, members[0])
        setup_leader(driver, members[0])
        setup_members(driver, members[1:])

    with open('stay.json', 'r') as f:
        stay = json.load(f)
        setup_stay(driver, stay)
