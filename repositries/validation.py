
from models.advertisement import AdvertisementInput



class Validator:
    def validate(ad_input : AdvertisementInput):
        if  ad_input.max_cpc <= 0:
            return False
        if ad_input.raise_percentage < 0 or ad_input.raise_percentage > 1:
            return False
        return True
