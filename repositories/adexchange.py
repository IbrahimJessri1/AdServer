from repositories import generics as gen
from models.ssp import Ad_Request
from models.users import Membership, MembershipMarks
from .utilites import orientor, rand
from config.db import advertisement_collection, interactive_advertisement_collection, user_collection, served_ad_collection
from models.ssp import ApplyAd
from uuid import uuid4
from .utilites import get_weight_user_info, get_kw_mark, orientor, get_dict, message_formatter
from fastapi import status, HTTPException
from config.general import HOST
from fastapi.templating import Jinja2Templates
import datetime
from .logger import my_logger

cat_weight = 1
keyword_weight = 1

user_info_weight = 12
categories_weight = 40
keywords_weight = 47
ctr_weight = 7
pay_weight = 7
membership_weight = 7
times_served_weight = 7




def negotiate(request : Ad_Request, interactive = 0):
    my_logger.error(message_formatter('request recieved for negotiation', str(get_dict(request))))
    ad_collection = advertisement_collection
    if interactive != 0:
        ad_collection = interactive_advertisement_collection
    adv_collection = user_collection
    query = {"$and": [{"$and": [{"marketing_info.max_cpc" : {"$gt" : request.min_cpc}}, {"ad_info.type" : request.type.value}, {"enabled" : 1}]}, {"ad_info.shape" : request.shape.value}]}
    all_ads = gen.get_many(ad_collection, query)
    if len(all_ads) == 0:
        my_logger.error(message_formatter('Pass, No Ads Found'))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No Ads For U")
    adv_usernames = []
    for ad in all_ads:
        adv_usernames.append(ad['ad_info']['advertiser_username'])
    adv_usernames = set(adv_usernames)
    constraints = []
    for un in adv_usernames:
        if {"username" : un} not in constraints:
            constraints.append({"username" : un})
    constraints = {"$or" : constraints}
    all_ads_advertisers = gen.get_many(collection=adv_collection, constraints=constraints)
    mem = {}
    for adv in all_ads_advertisers:
        mem[adv['username']] = adv['membership']
    for index in range(len(all_ads)):
        membership = mem[all_ads[index]['ad_info']['advertiser_username']]
        if membership == Membership.NORMAL:
            all_ads[index]["membership"] = Membership.NORMAL.value
        elif membership == Membership.PREMIUM:
            all_ads[index]["membership"] = Membership.PREMIUM.value
        else:
            all_ads[index]["membership"] = Membership.VIP.value

    
    my_logger.error(message_formatter('ads remainning after filtering ' + str(len(all_ads))))

    final_ad_list = []
    


    mx_times_served = 0
    mx_raise_amount = 0
    mx_kw_mark = 0
    mx_cat_matched = 0

    mx_ctr = 0
    for index in range(len(all_ads)):
        ad = all_ads[index]
        mx_times_served = max(ad["marketing_info"]["impressions"], mx_times_served)
        raise_percentage = rand(ad["marketing_info"]["raise_percentage"] / 2, ad["marketing_info"]["raise_percentage"], 3)
        diff = (ad["marketing_info"]["max_cpc"] - request.min_cpc)
        actual_raise = max(min(ad["marketing_info"]["max_cpc"] - request.min_cpc, request.min_cpc * raise_percentage), rand(diff * 0.2, diff * 0.3, 3))
        mx_raise_amount = max(actual_raise, mx_raise_amount)
        if interactive and ad["marketing_info"]["impressions"] != 0:
            mx_ctr = max(mx_ctr, ad["marketing_info"]["clicks"] / ad["marketing_info"]["impressions"])
        
        if request.categories:
            cat_matched = 0
            for cat in request.categories:
                if cat in ad["categories"]:
                    cat_matched+= 1
            mx_cat_matched = max(mx_cat_matched, cat_matched)

        if request.keywords:
            res = get_kw_mark(request.keywords, ad["keywords"])
            mx_kw_mark = max(mx_kw_mark, res)


        final_ad_list.append([index, 0, actual_raise])
    for i in range(len(all_ads)):
        all_weights = 0
        marks = 0
        ad = all_ads[i]
        user_info_res = get_weight_user_info(request.user_info, ad)
        if user_info_res != -1:
            all_weights += user_info_weight
            marks += user_info_res * user_info_weight
        if request.categories:
            if mx_cat_matched != 0:
                cat_matched = 0
                for cat in request.categories:
                    if cat in ad["categories"]:
                        cat_matched += 1
                if mx_cat_matched != 0:
                    all_weights += categories_weight
                    marks += (cat_matched * 100 / mx_cat_matched) * categories_weight

        if request.keywords:
            if mx_kw_mark != 0:
                res = get_kw_mark(request.keywords, ad["keywords"])
                all_weights += keywords_weight
                marks += (res * 100 / mx_kw_mark) * keywords_weight

        if mx_times_served != 0:
            all_weights += times_served_weight
            marks += ((mx_times_served - ad["marketing_info"]["impressions"]) * 100 / mx_times_served) * times_served_weight

        all_weights += pay_weight
        marks += (final_ad_list[i][2] * 100 / mx_raise_amount) * pay_weight

        membership_gained_marks = 0
        if ad["membership"] == Membership.NORMAL:
            membership_gained_marks = MembershipMarks.NORMAL.value
        elif ad["membership"] == Membership.PREMIUM:
            membership_gained_marks = MembershipMarks.PREMIUM.value
        elif ad["membership"] == Membership.VIP:
            membership_gained_marks = MembershipMarks.VIP.value

        all_weights += membership_weight
        marks += int(membership_gained_marks) * membership_weight

        if interactive != 0:
            all_weights += ctr_weight
            if ad["marketing_info"]["impressions"] != 0:
                ctr = ad["marketing_info"]["clicks"]  / ad["marketing_info"]["impressions"]
                if mx_ctr != 0:
                    ctr = ctr * 100 / mx_ctr
                marks += ctr * ctr_weight
        final_weight = 0
        if all_weights != 0:
            final_weight = marks / all_weights
        final_ad_list[i] = [i, final_weight, final_ad_list[i][2] + request.min_cpc]
    final_ad_list.sort(key= lambda x : x[1], reverse= True)
    winner_ad = all_ads[final_ad_list[0][0]]
    res = {"cpc": final_ad_list[0][2], "weight":final_ad_list[0][1],  "ad_id": winner_ad["id"]}
    # if res['weight'] < 60:
    #     my_logger.error(message_formatter('Pass, No Ads Found'))
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Good Ad For You')
    my_logger.error(message_formatter('best choice: AD-ID: ' + res['ad_id'] + ' - cpc: ' + str(res['cpc']) + ' - score: ' + str(res['weight'])))
    return res
    


def request(ad_apply : ApplyAd, interactive = 0):
    ad_collection = advertisement_collection
    if interactive != 0:
        ad_collection = interactive_advertisement_collection
    ad = gen.get_one(ad_collection, {"id" : ad_apply.ad_id})
    if (not ad) or (ad_apply.cpc > ad["marketing_info"]["max_cpc"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Ad For U")
    id = str(uuid4())
    clicks = 0
    if interactive == 0:
        clicks = -1
    served_ad = {"id": id, "agreed_cpc": ad_apply.cpc, "impressions": 0, "clicks" : clicks, "ad_id": ad["id"], "advertiser_username" : ad["ad_info"]["advertiser_username"], "payment_account": ad_apply.payment_account, "create_date": str(datetime.datetime.now()), "charges": 0, "paid":0}
    served_ad_collection.insert_one(dict(served_ad))
    data = {
        "url" : HOST + 'serve_ad/impression/' + id,
        "text" : ad["ad_info"]["text"],
        "type": ad["ad_info"]["type"]
    }
    width = ad["ad_info"]["width"]
    height = ad["ad_info"]["height"]
    ratio = width / height
    if ad_apply.max_width != 0 and ad_apply.max_height == 0:
        width = ad_apply.max_width
        height = int(width / ratio)
    elif ad_apply.max_width == 0 and ad_apply.max_height != 0:
        height = ad_apply.max_height
        width = int(height * ratio)
    elif ad_apply.max_width != 0 and ad_apply.max_height != 0:
        max_width = int(ad_apply.max_height * ratio)
        if max_width <= ad_apply.max_width:
            width = max_width
            height = int(width / ratio)
        else:
            height = int(ad_apply.max_width / ratio)
            width = int(height * ratio)

    data["width"] = width
    data["height"] = height
    font_size = 0
    margin_top = 0
    if ad["ad_info"]["text"] != "":
        font_size = 13#int((13/275) * (width+height)/2)
        margin_top = 13#int((13/275) * (width+height)/2)
    data["text_font_size"] = font_size
    data["text_margin_top"] = margin_top
    if interactive != 0:
        data["redirect_url"] = HOST + 'serve_ad/click/' + id 
    return data


def html_request(req, ad_apply, interactive = 0):
    data = request(ad_apply=ad_apply, interactive=interactive)
    data["request"] = req
    path = orientor(data["type"], interactive)
    templates = Jinja2Templates(directory="templates")
    my_logger.error(message_formatter('serve ad request ID: ' + str(ad_apply.ad_id) + ' sending details..'))
    return templates.TemplateResponse(path,data)


