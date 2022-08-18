from repositries import generics as gen
from models.ssp import Ad_Request
from models.users import Membership, MembershipMarks
from .utilites import probability_get, rand
from config.db import advertisement_collection, interactive_advertisement_collection, user_collection, served_ad_collection
from models.ssp import ApplyAd
from uuid import uuid4
from .utilites import get_weight_user_info, get_kw_mark
from fastapi import status, HTTPException
from config.general import HOST
from fastapi.templating import Jinja2Templates


cat_weight = 1
keyword_weight = 1


user_info_weight = 10
categories_weight = 40
keywords_weight = 50
ctr_weight = 0
pay_weight = 0
membership_weight = 0
times_served_weight = 0

def negotiate(request : Ad_Request, interactive = 0):

    ad_collection = advertisement_collection
    if interactive != 0:
        ad_collection = interactive_advertisement_collection
    adv_collection = user_collection
    query = {"$and": [{"marketing_info.max_cpc" : {"$gt" : request.min_cpc}}, {"ad_info.type" : request.type.value}]}
    all_ads = gen.get_many(ad_collection, query)
    all_ads_advertisers = []
    for ad in all_ads:
        all_ads_advertisers.append(gen.get_one(adv_collection, {"username" : ad["ad_info"]["advertiser_username"]}))

    for index in range(len(all_ads)):
        if all_ads_advertisers[index]["membership"] == Membership.NORMAL:
            all_ads[index]["membership"] = Membership.NORMAL.value
        elif all_ads_advertisers[index]["membership"] == Membership.PREMIUM:
            all_ads[index]["membership"] = Membership.PREMIUM.value
        else:
            all_ads[index]["membership"] = Membership.VIP.value

    if len(all_ads) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No Ads For U")
   

    final_ad_list = []
    


    mx_times_served = 0
    mx_raise_amount = 0
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
        final_ad_list.append([index, 0, actual_raise])
    
    for i in range(len(all_ads)):
        if i == 1:
            break
        all_weights = 0
        marks = 0
        ad = all_ads[i]
        user_info_res = get_weight_user_info(request.user_info, ad)
        if user_info_res != -1:
            all_weights += user_info_weight
            marks += user_info_res * user_info_weight
        cat_tot_marks = 0
        cat_gained_marks = 0
        if request.categories:
            for cat in request.categories:
                cat_tot_marks += cat_weight
                if cat in ad["categories"]:
                    cat_gained_marks += cat_weight

        if cat_tot_marks != 0:
            all_weights += categories_weight
            marks += (cat_gained_marks * 100 / cat_tot_marks) * categories_weight

        if request.keywords:
            res = get_kw_mark(request.keywords, ad["keywords"])
            all_weights += keywords_weight
            marks += res * keywords_weight

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
        # if ad["id"] == "17da25c1-738e-42e1-b531-3f3973d75209":
        #     print(final_weight, " " , "gaming")
        # if ad["id"] == "02fba90c-959e-459d-9966-7f2d24ad980d":
        #     print(final_weight, " ", "furn")
        final_ad_list[i] = [i, final_weight, final_ad_list[i][2] + request.min_cpc]

    final_ad_list.sort(key= lambda x : x[1], reverse= True)
    winner_ad = all_ads[final_ad_list[0][0]]
    #return {"cpc": final_ad_list[0][1], "ad_id": winner_ad["id"]}
    if final_ad_list[0][1] <50:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No Ads For U")
    # print(final_ad_list[0])
    # print(winner_ad)
    res = {"cpc": final_ad_list[0][2], "weight":final_ad_list[0][1],  "ad_id": winner_ad["id"]}
    print(res)
    return res
    


def request(ad_apply : ApplyAd, interactive = 0):
    ad_collection = advertisement_collection
    if interactive != 0:
        ad_collection = interactive_advertisement_collection
    ad = gen.get_one(ad_collection, {"id" : ad_apply.ad_id})
    if (not ad) or (ad_apply.cpc > ad["marketing_info"]["max_cpc"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Ad For U")
    id = str(uuid4())
    served_ad = {"id": id, "agreed_cpc": ad_apply.cpc, "impressions": 0, "clicks" : 0, "ad_id": ad["id"], "advertiser_username" : ad["ad_info"]["advertiser_username"], "payment_account": ad_apply.payment_account}
    served_ad_collection.insert_one(dict(served_ad))
    data = {
        "url" : HOST + 'serve_ad/impression/' + id,
        "text" : ad["ad_info"]["text"]
    }
    width = ad["ad_info"]["width"]
    height = ad["ad_info"]["height"]
    ratio = width / height
    if ad_apply.max_width != 0 and ad_apply.max_height == 0:
        width = min(width, ad_apply.max_width)
        height = int(width / ratio)
    elif ad_apply.max_width == 0 and ad_apply.max_height != 0:
        height = min(height, ad_apply.max_height)
        width = int(height * ratio)
    elif ad_apply.max_width != 0 and ad_apply.max_height != 0:
        max_width = int(min(ad_apply.max_height, height) * ratio)
        if max_width <= ad_apply.max_width:
            width = max_width
            height = int(width / ratio)
        else:
            height = int(min(ad_apply.max_width,width) / ratio)
            width = int(height * ratio)

    data["width"] = width
    data["height"] = height
    data["text_font_size"] =int((13/275) * (width+height)/2)
    data["text_margin_top"] = int((13/275) * (width+height)/2)
    if interactive != 0:
        data["redirect_url"] = HOST + 'serve_ad/click/' + id 
    return data


def html_request(req, ad_apply, interactive = 0):
    data = request(ad_apply=ad_apply, interactive=interactive)
    data["request"] = req
    templates = Jinja2Templates(directory="templates")
    if interactive:
        return templates.TemplateResponse("interactive_img_ad.html",data)
    return templates.TemplateResponse("img_ad.html",data)