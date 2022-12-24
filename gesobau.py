import requests
from selenium import webdriver
from company import Company


class Gesobau(Company):
    def apply(self, driver: webdriver):
        print("gesobau")


if __name__ == '__main__':
    Gesobau().apply(None)