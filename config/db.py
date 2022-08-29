
from pymongo import MongoClient
from repositries import generics as gen

from models.advertisement import Category
conn = MongoClient("mongodb://localhost:27017/AdServer")


advertisement_collection = conn.AdServer.advertisement
interactive_advertisement_collection = conn.AdServer.interactive_advertisement
user_collection = conn.AdServer.user
role_permission_collection = conn.AdServer.role_permission

served_ad_collection = conn.AdServer.served_ad



# gen.update_one(served_ad_collection,{"paid" :{"$gte" : 0.01255}}, {"$set": {"paid":0, "charges" : 0.05255}})

# print(gen.get_many(interactive_advertisement_collection, {"ad_info.type" : "gif"}))

# res = gen.get_many(advertisement_collection, {"adinfo.advertiser_username" : "testAdv"})
# print(res)




# advertisement_collection.delete_many({})
# interactive_advertisement_collection.delete_many({})
# served_ad_collection.delete_many({})


#gen.update_many(collection, {}, {"$set" : {"marketing_info.times_served" : 0} })


#print(all_ads[0]["marketing_info"]["max_cpc"])


# advertisement_collection.delete_many({})
# interactive_advertisement_collection.delete_many({})
# served_ad_collection.delete_many({})



# for cat in Category:
#     res = "{label: '" + cat.value.upper() + "', value: '" + cat.value + "', alias: '" + cat.value + "'},"
#     print(res)