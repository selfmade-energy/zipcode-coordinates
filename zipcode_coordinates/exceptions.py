class ZipCodeNotFound(Exception):
    def __init__(self, zipcode):
        super().__init__(f"Zip code {zipcode} not found")
