
from pymongo import MongoClient
from repositries import generics as gen


conn = MongoClient("mongodb://localhost:27017/AdServer")


advertisement_collection = conn.AdServer.advertisement
interactive_advertisement_collection = conn.AdServer.interactive_advertisement
user_collection = conn.AdServer.user
role_permission_collection = conn.AdServer.role_permission

served_ad_collection = conn.AdServer.served_ad



#gen.update_many(collection, {}, {"$set" : {"marketing_info.times_served" : 0} })


#print(all_ads[0]["marketing_info"]["max_cpc"])
