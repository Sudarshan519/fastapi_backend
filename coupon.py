import itertools
import json
from apis.v1.coupon_management import route_coupon
# Create an iterator for generating unique IDs
id_counter = itertools.count()
from fastapi import APIRouter, FastAPI
# Create a dictionary to store coupon data
# Function to load coupons from the JSON file
def load_coupons_from_file():
    with open("coupons.json", "r") as file:
        coupons = json.load(file)
    return coupons
coupons=load_coupons_from_file()

def save_coupons_to_file():
    with open("coupons.json", "w") as file:
        json.dump(coupons, file)


        
app = FastAPI()
coupon_router=APIRouter()
app.include_router(route_coupon.router,prefix='/coupon',tags=['Coupon'])

@coupon_router.get('/')
def get_all_coupons():
    return coupons
# Create a function to save coupons to a JSON file




# Endpoint to create a coupon with attachments
@app.post("/r/coupons")
def create_coupon(coupon_data: dict):
    coupon_id = coupon_data.get("coupon_id")
    attachments = coupon_data.get("attachments")

    # Store the coupon data in the dictionary
    coupons.append({
        "coupon_id": coupon_id,
        "attachments": attachments,
        "usage": 0
    })

    # Save the coupons to the JSON file
    save_coupons_to_file()

    return {"message": "Coupon created successfully"}

# Endpoint to retrieve a coupon with attachments and usage
@app.get("/coupons/{coupon_id}")
def get_coupon(coupon_id: str):
    coupon = coupons.get(coupon_id)

    if coupon:
        attachments = coupon["attachments"]
        usage = coupon["usage"]
        return {"coupon_id": coupon_id, "attachments": attachments, "usage": usage}
    else:
        return {"message": "Coupon not found"}

# Endpoint to update attachments for a coupon
@app.put("/coupons/{coupon_id}")
def update_attachments(coupon_id: str, attachments: list):
    if coupon_id in coupons:
        coupons[coupon_id]["attachments"] = attachments
        save_coupons_to_file()  # Save the coupons to the JSON file after updating
        return {"message": "Attachments updated successfully"}
    else:
        return {"message": "Coupon not found"}

# Endpoint to delete a coupon
@app.delete("/coupons/{coupon_id}")
def delete_coupon(coupon_id: str):
    if coupon_id in coupons:
        del coupons[coupon_id]
        save_coupons_to_file()  # Save the coupons to the JSON file after deletion
        return {"message": "Coupon deleted successfully"}
    else:
        return {"message": "Coupon not found"}



#  Product


# Endpoint to buy a product with a coupon
@app.post("products/buy/{product_id}",tags=['Product'])
def buy_product(product_id: str, coupon_id: str):
    # Check if the coupon exists
    coupons = load_coupons_from_file()
    coupon_found = False
    for coupon in coupons:
        if coupon["coupon_id"] == coupon_id:
            coupon_found = True
            attachments = coupon["attachments"]
            usage = coupon["usage"]

            # Perform the purchase with the coupon
            # ... Your code to handle the purchase ...

            # Increment coupon usage and save
            coupon["usage"] -= 1
            save_coupons_to_file(coupons)
            return {"message": "Product purchased successfully with the coupon"}

    if not coupon_found:
        return {"message": "Coupon not found"}

    return {"message": "Product purchase failed"}
