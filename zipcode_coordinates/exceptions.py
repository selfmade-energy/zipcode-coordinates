class ZipCodeNotFound(Exception):
    def __init__(self, zipcode):
        super().__init__(f"Zip code {zipcode} not found")


class CountryCodeNotFound(Exception):
    def __init__(self, country_code):
        super().__init__(f"Country code {country_code} not found")
