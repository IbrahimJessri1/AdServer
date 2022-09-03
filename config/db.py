
from pymongo import MongoClient
from repositories import generics as gen
from models.advertisement import Category
import time
conn = MongoClient("mongodb://localhost:27017/AdServer")


advertisement_collection = conn.AdServer.advertisement
interactive_advertisement_collection = conn.AdServer.interactive_advertisement
user_collection = conn.AdServer.user
role_permission_collection = conn.AdServer.role_permission

served_ad_collection = conn.AdServer.served_ad
