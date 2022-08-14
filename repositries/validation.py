
from models.advertisement import AdvertisementInput
from models.users import Advertiser, AdvertiserUpdate



class Validator:
    def validate_ad_input(ad_input : AdvertisementInput):
        if ad_input.max_cpc <= 0:
            return "max_cpc must be positive"
        if ad_input.raise_percentage < 0 or ad_input.raise_percentage > 1:
            return "raise percentage must between 0 and 1"
        return False
    def validate_advertiser(advertiser: Advertiser):
        if len(advertiser.username) < 4:
            return "username must have at least 4 characters"
        if len(advertiser.password) < 8:
            return "password must have at least 9 characters"
        return False
    
    def validate_advertiser_update(advertiser_update : AdvertiserUpdate):
        if len(advertiser_update.password) < 8:
            return "password must have at least 8 characters"
        return False