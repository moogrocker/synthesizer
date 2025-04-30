from time import sleep
import parameters
import os
import pandas as pd
from fpdf import FPDF
import urllib.parse

# Traditional scrapping
import requests
from bs4 import BeautifulSoup
import base64

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


link_name = 'moogrockersynthesizer@gmail.com'
link_password = 'Mr9jCq6NtttN?f8$'
job = "data scientist"
location = "london"



def search_people(job, location):

    base_url = "https://www.linkedin.com/search/results/people/"

    keywords = f"{job},{location}"

    encoded_keywords = urllib.parse.quote(keywords) # URL-encode the keywords
    params = f"keywords={encoded_keywords}&origin=GLOBAL_SEARCH_HEADER" # Construct the query parameters
    search_url = f"{base_url}?{params}"
    return search_url


def login(email, password):

    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    username = driver.find_element(By.NAME, "session_key")
    password = driver.find_element(By.NAME, "session_password")

    # Credentials
    username.send_keys(email)
    password.send_keys(password)
    password.send_keys(Keys.RETURN)

    # Wait for the welcome page to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-nav"))
        )
    except Exception as e:
        print("Error: Page did not load in time", e)
