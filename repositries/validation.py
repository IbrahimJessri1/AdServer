
from models.advertisement import AdvertisementInput
from models.users import Advertiser, AdvertiserUpdate, UserUpdate



class Validator:
    def validate_ad_input(ad_input : AdvertisementInput):
        msg = []
        if ad_input.max_cpc <= 0:
            msg.append("max_cpc must be positive")
        if ad_input.raise_percentage < 0 or ad_input.raise_percentage > 1:
            msg.append("raise percentage must between 0 and 1")
        if len(ad_input.text) == 0:
            msg.append("text should not be empty")
        ad_input["categories"] = list(set(ad_input["categories"]))
        if ad_input["keywords"]:
            ad_input["keywords"] = list(set(ad_input["keywords"]))
        if msg:
            return msg
        return False

    def validate_advertiser(advertiser: Advertiser):
        msg = []
        if len(advertiser.username) < 4:
            msg.append("username must have at least 4 characters")
        if len(advertiser.password) < 8:
            msg.append("password must have at least 9 characters")
        if msg:
            return msg
        return False
    
    def validate_advertiser_update(advertiser_update : AdvertiserUpdate):
        msg = []
        if len(advertiser_update.password) < 8:
            msg.append("password must have at least 8 characters")
        if msg:
            return msg
        return False

    def validate_user_update(user_update: UserUpdate):
        msg = []
        if len(user_update.password) < 8:
            msg.append("password must have at least 8 characters")
        if msg:
            return msg
        return False