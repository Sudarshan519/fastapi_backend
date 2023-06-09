# import json
# from fastapi import APIRouter, FastAPI

# router = APIRouter()

# # Create a dictionary to store coupon data
# coupons = {}


# # Create a function to save coupons to a JSON file
# def save_coupons_to_file():
#     with open("coupons.json", "w") as file:
#         json.dump(coupons, file)

# # Endpoint to create a coupon with attachments
# @router.post("/coupons")
# def create_coupon(coupon_data: dict):
#     coupon_id = coupon_data.get("coupon_id")
#     attachments = coupon_data.get("attachments")

#     # Store the coupon data in the dictionary
#     coupons[coupon_id] = attachments

#     return {"message": "Coupon created successfully"}

# # Endpoint to retrieve a coupon with attachments
# @router.get("/coupons/{coupon_id}")
# def get_coupon(coupon_id: str):
#     attachments = coupons.get(coupon_id)

#     if attachments:
#         return {"coupon_id": coupon_id, "attachments": attachments}
#     else:
#         return {"message": "Coupon not found"}

# # Endpoint to update attachments for a coupon
# @router.put("/coupons/{coupon_id}")
# def update_attachments(coupon_id: str, attachments: list):
#     if coupon_id in coupons:
#         coupons[coupon_id] = attachments
#         return {"message": "Attachments updated successfully"}
#     else:
#         return {"message": "Coupon not found"}

# # Endpoint to delete a coupon
# @router.delete("/coupons/{coupon_id}")
# def delete_coupon(coupon_id: str):
#     if coupon_id in coupons:
#         del coupons[coupon_id]
#         return {"message": "Coupon deleted successfully"}
#     else:
#         return {"message": "Coupon not found"}


from fastapi import APIRouter


router=APIRouter()


@router.get('/')
def get_all_coupons():
    return []
