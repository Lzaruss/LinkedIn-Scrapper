from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional, Dict

class Person:
    # Constants for reusable class names or tags
    CONTACT_TYPE_CLASS = 'pv-contact-info__contact-type'

    def __init__(self, driver: Optional[WebDriver] = None):
        """
        Initializes a Person instance.
        :param driver: Selenium WebDriver instance for web scraping.
        """
        self.driver = driver
        self.name: str = ""
        self.profile: str = ""
        self.website: str = ""
        self.phone: str = ""
        self.email: str = ""
        self.birthday: str = ""
        self.title: str = ""
        self.location: str = ""
        self.address: str = ""
        self.photo: str = ""

    def _safe_find_element(self, by: By, value: str, attribute: Optional[str] = None) -> str:
        """
        Safely finds an element and optionally retrieves an attribute or text.
        :param by: By selector (e.g., By.ID, By.CLASS_NAME).
        :param value: Value for the selector.
        :param attribute: Attribute to retrieve; if None, retrieves text.
        :return: Text or attribute value of the element, or an empty string if not found.
        """
        try:
            element = self.driver.find_element(by, value)
            return element.get_attribute(attribute) if attribute else element.text.strip()
        except Exception:
            return ""

    def _get_section_value(self, class_name: str, h3_text: str, tag: str = 'span') -> str:
        """
        Searches for a specific section by class name and h3 text, returning the value of a tag within.
        :param class_name: Class name of the section.
        :param h3_text: Text of the <h3> tag to match.
        :param tag: Tag to retrieve content from.
        :return: Text content of the matched tag, or an empty string if not found.
        """
        try:
            sections = self.driver.find_elements(By.CLASS_NAME, class_name)
            for section in sections:
                h3 = section.find_element(By.TAG_NAME, 'h3')
                if h3.text.strip() == h3_text:
                    return section.find_element(By.TAG_NAME, tag).text.strip()
        except Exception:
            pass
        return ""

    def gather_name(self):
        self.name = self._safe_find_element(By.ID, 'pv-contact-info')

    def gather_profile(self):
        try:
            profile_element = self.driver.find_element(By.CLASS_NAME, 'pv-top-card--list')
            self.profile = profile_element.find_element(By.TAG_NAME, 'li').find_element(By.TAG_NAME, 'a').get_attribute('href')
        except Exception:
            self.profile = ""

    def set_profile(self, profile: str):
        self.profile = profile

    def gather_website(self):
        self.website = self._safe_find_element(By.CLASS_NAME, 'pv-contact-info__contact-link')

    def gather_phone(self):
        self.phone = self._get_section_value(self.CONTACT_TYPE_CLASS, 'Phone')

    def gather_email(self):
        self.email = self._get_section_value(self.CONTACT_TYPE_CLASS, 'Email', tag='a')

    def gather_birthday(self):
        self.birthday = self._get_section_value(self.CONTACT_TYPE_CLASS, 'Birthday')

    def gather_address(self):
        self.address = self._get_section_value(self.CONTACT_TYPE_CLASS, 'Address')

    def gather_title(self):
        self.title = self._safe_find_element(By.CLASS_NAME, 'text-body-medium.break-words')

    def gather_location(self):
        self.location = self._safe_find_element(By.CLASS_NAME, 'text-body-small.inline.t-black--light.break-words')

    def gather_photo(self):
        self.photo = self._safe_find_element(By.CLASS_NAME, 'pv-top-card-profile-picture__container', attribute='src')

    def gather_all_info(self, include_profile: bool = False) -> "Person":
        """
        Gathers all available information for the person.
        :param include_profile: Whether to gather profile URL.
        :return: The updated Person instance.
        """
        self.gather_name()
        if include_profile:
            self.gather_profile()
        self.gather_website()
        self.gather_phone()
        self.gather_email()
        self.gather_birthday()
        self.gather_title()
        self.gather_address()
        self.gather_location()
        self.gather_photo()
        return self

    def __str__(self) -> str:
        return (f"Name: {self.name}\nProfile: {self.profile}\nWebsite: {self.website}\nPhone: {self.phone}\n"
                f"Email: {self.email}\nBirthday: {self.birthday}\nTitle: {self.title}\n"
                f"Location: {self.location}\nAddress: {self.address}\nPhoto: {self.photo}\n")

    def to_dict(self) -> Dict[str, str]:
        return {
            "profile": self.profile,
            "name": self.name,
            "title": self.title,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "birthday": self.birthday,
            "location": self.location,
            "website": self.website,
            "photo": self.photo
        }
