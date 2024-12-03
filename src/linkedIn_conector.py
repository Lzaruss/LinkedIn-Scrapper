from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.person import Person
from src.fileManager import FileManager
from src.utils import scroll_to_end, printyellow

class LinkedInConector:

    def __init__(self, connection_links_file: str, driver=None):
        self.driver = driver
        self.fm = FileManager(connection_links_file)

    def start(self):
        self.goToMyConnections()
        printyellow('Gathering connections...')
        connection_links = self.get_connections_links()
        self.fm.add_connections(connection_links)
        self.gather_all_contact_info(self.fm.get_connections())

    def goToMyConnections(self):
        self.driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
        self._wait_for_page_load()
        self._scroll_to_end()

    def gather_contact_info(self, connection_link: str, show_terminal: bool = True) -> Person:
        contact_info_link = self._connection_link_contact_info(connection_link)
        self._go_to(contact_info_link)
        person = Person(self.driver)
        person.gather_all_info()
        person.set_profile(connection_link)
        
        if show_terminal:
            printyellow(person)

        return person

    def gather_all_contact_info(self, connection_links: list[str]):
        for link in connection_links:
            person = self.gather_contact_info(link)
            self.fm.add_person(person.to_dict())
            self.fm.remove_connection(link)

    def get_connections_links(self) -> list[str]:
        links = []
        connections_list = self.driver.find_elements(By.CLASS_NAME, "mn-connection-card__details")
        for connection in connections_list:
            link = connection.find_element(By.TAG_NAME, "a").get_attribute("href")
            links.append(link)
        return links

    def _go_to(self, url: str):
        self.driver.get(url)
        self._wait_for_page_load()

    def _connection_link_contact_info(self, connection_link: str) -> str:
        return f"{connection_link}overlay/contact-info/"

    def _wait_for_page_load(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def _scroll_to_end(self, times: int = 20):
        for _ in range(times):
            scroll_to_end(self.driver, times=times)
            try:
                self.driver.find_element(By.CSS_SELECTOR, "div.p5").click()
            except NoSuchElementException:
                pass