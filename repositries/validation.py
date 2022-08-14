
from models.advertisement import AdvertisementInput
from models.ssp import Ad_Request, ApplyAd
from models.users import Advertiser, AdvertiserUpdate, UserUpdate


MAX_KEYWORDS = 20


class Validator:
    def validate_ad_input(ad_input : AdvertisementInput):
        msg = []
        if ad_input.max_cpc <= 0:
            msg.append("max_cpc must be positive")
        if ad_input.raise_percentage < 0 or ad_input.raise_percentage > 1:
            msg.append("raise percentage must between 0 and 1")
        if len(ad_input.text) == 0:
            msg.append("text should not be empty")
        ad_input.categories = list(set(ad_input.categories))
        if ad_input.keywords:
            ad_input.keywords= list(set(ad_input.keywords))
            if len(ad_input.keywords) > MAX_KEYWORDS:
                msg.append("too many keywords")
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


    def validate_ad_request(ad_request :Ad_Request):
        msg = []
        if ad_request.min_cpc < 0:
            msg.append("min_cpc must be positive")
        if ad_request.categories:
            ad_request.categories = list(set(ad_request.categories))
        if ad_request.keywords:
            ad_request.keywords = list(set(ad_request.keywords))
            if len(ad_request.keywords) > MAX_KEYWORDS:
                msg.append("too many keywords")
        if msg:
            return msg
        return False

    def validate_ad_apply(apply_ad : ApplyAd):
        msg = []
        if apply_ad.cpc < 0:
            msg.append("cpc must be positive")
        if msg:
            return msg
        return False

                