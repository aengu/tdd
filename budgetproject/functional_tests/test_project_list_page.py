from selenium import webdriver
from selenium.webdriver.common.by import By
from budget.models import Project
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.test import LiveServerTestCase
from django.urls import reverse
import time

"""
selenium같은 브라우저 기반 테스트할 때 사용하는 testCase class
- LiveServerTestCase: 정적파일 서빙 x
- StaticLiveServerTestCase: 정적파일 서빙 o
오 요즘 셀레니움은 웹드라이버 파일 필요 없다..
"""

class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
    
    def tearDown(self):
        self.browser.close()
    
    def test_no_projects_alert_is_displayed(self):
        self.browser.get(self.live_server_url)

        # the user requests the page for the first time
        alert = self.browser.find_element(By.CLASS_NAME, 'noproject-wrapper')
        self.assertEquals(
            alert.find_element(By.TAG_NAME,'h3').text,
            'Sorry, you don\'t have any projects, yet.'
        )
    
    def test_no_projects_alert_button_redirects_to_add_page(self):
        self.browser.get(self.live_server_url)

        # the user requests the page for the first time
        add_url = self.live_server_url + reverse('add')
        self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEquals(
            self.browser.current_url,
            add_url
        )
    
    def test_user_sees_project_list(self):
        project1 = Project.objects.create(
            name = 'project1',
            budget = 10000
        )
        self.browser.get(self.live_server_url)

        # the user sees the project on the screen
        self.assertEquals(
            self.browser.find_element(By.TAG_NAME, 'h5').text,
            'project1'
        )
    
    def test_user_is_redirected_to_project_detail(self):
        project1 = Project.objects.create(
            name = 'project1',
            budget = 10000
        )
        self.browser.get(self.live_server_url)

        # the user sees the project on the screen. he clicks the 'VISIT' link
        # and is redirected to the detail page
        detail_url = self.live_server_url + reverse('detail', args=[project1.slug])
        self.browser.find_element(By.LINK_TEXT, 'VISIT').click()
        self.assertEquals(
            self.browser.current_url,
            detail_url
        )
