
#collection = conn.AdServer.role_permission
from config.db import role_permission_collection
from repositries import generics as gen

admin_permission = ["get_tot_payment", "get_served_ad", "self_update_user", "update_advertisement", "delete_advertisement", "get_advertisement","delete_user","self_delete_user", "self_get_user", "get_user"]

#collection.insert_one(
{
    "role" : "admin",
    "permissions" :admin_permission
}
#)


advertiser_permission = ["self_get_ad_payment", "self_get_tot_payment", "self_get_served_ad", "self_update_user", "self_delete_user", "self_get_user","create_interactive_ad",  "create_ad", "self_delete_ad", "self_update_ad", "self_get_ad", "self_update_account_adv", "self_get_adv"]

#collection.insert_one(
{
    "role" : "advertiser",
    "permissions" :advertiser_permission
}


gen.update_one(role_permission_collection, {"role" : "advertiser"}, {"$set" : {"permissions" : advertiser_permission}})
gen.update_one(role_permission_collection, {"role" : "admin"}, {"$set" : {"permissions" : admin_permission}})


#)



###add admin
# admin = User(username='admin1', password=hashing.Hash.bcrypt('123'), role='admin', create_date=str(datetime.datetime.now()))
# conn.AdServer.user.delete_many({"role" : 'admin'})
# conn.AdServer.user.insert_one(dict(admin))


