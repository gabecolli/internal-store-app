from pymongo_get_database import get_database

#customer_info is going to be a dictionary
'''
with the following keys
paid, meas_taken, name, adrs, phnumber, email
'''

def enter_customer(customer_info):

    dbname = get_database()

    collection_name = dbname["customers"]

    customer_data = {
        "customer_name" : customer_info["cus_name"],
        "measurements_taken" : customer_info["meas_taken"],
        "address" : customer_info["adrs"],
        "phone_number" : customer_info["phnumber"],
        "email" : customer_info["email"]
    }


    collection_name.insert_one(customer_data)



def get_customers():
    dbname = get_database()
    collection_name = dbname["customers"]
    item_details = collection_name.find()
    
    cus_list = []
    for item in item_details:
        cus_list.append(item)
    return cus_list  #list of dictionaries

    
    

