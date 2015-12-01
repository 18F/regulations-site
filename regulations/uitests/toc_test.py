import unittest
from base_test import BaseTest
from selenium.webdriver.support.ui import WebDriverWait


class TOCTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'TOC test'

    def test_toc(self):
        self.driver.set_window_size(1024, 600)
        self.driver.get(self.test_url + '/1005')
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))

        drawer_toggle = self.driver.find_element_by_id('panel-link')
        drawer_toggle.click()

        # toggle arrow should switch
        self.assertTrue(drawer_toggle.get_attribute('class').find('open'))

        toc_link_1005_1 = self.driver.find_element_by_xpath(
            '//*[@id="toc"]/ol/li[1]/a')
        # toc link should have the proper section id attr
        self.assertEqual(toc_link_1005_1.get_attribute('data-section-id'),
                         '1005-1')
        toc_link_1005_1.click()

        # reg section should load in content area
        self.assertTrue(
            'catharine and myriads'
            in self.driver.find_element_by_class_name('section-title').text)

        # toc link should be highlighted
        self.assertTrue('current' in toc_link_1005_1.get_attribute('class'))

        WebDriverWait(self.driver, 90)

        # test another section
        toc_link_1005_3 = self.driver.find_element_by_xpath(
            '//*[@id="toc"]/ol/li[3]/a')
        self.assertEquals(toc_link_1005_3.get_attribute('data-section-id'),
                          '1005-3')

        toc_link_1005_3.click()
        # toc link should be highlighted
        self.assertTrue('current' in toc_link_1005_3.get_attribute('class'))

        self.assertTrue(
            'clicked'
            in self.driver.find_element_by_class_name('section-title').text)
        self.assertTrue('current' in toc_link_1005_3.get_attribute('class'))

        # make sure that the current class has been removed from the prev
        # section
        self.assertFalse('current' in toc_link_1005_1.get_attribute('class'))

if __name__ == '__main__':
    unittest.main()
