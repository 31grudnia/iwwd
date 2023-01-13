# import fastapi
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from database.db_setup import get_db
# from dotenv import load_dotenv
#
# # from helpers.paymentMethodCategoryHelpers import add_payment_method_category, get_payment_method_categories
#
# from schemas.PaymentMethodCategorySchema import PaymentMethodCategory as PaymentMethodCategorySchema
#
#
# load_dotenv(".env")
# router = fastapi.APIRouter()
#
#
# """
#     PAYMENT METHOD CATEGORY ENDPOINTS
# """
#
#
# @router.post("/payment_method_category/add", tags=['payment_method_category'], status_code=201)
# async def payment_method_category_add(pmcategory: PaymentMethodCategorySchema, db: Session = Depends(get_db)):
#     return {"Added Payment Method Category": add_payment_method_category(db=db, pmcategory=pmcategory)}
#
#
# @router.get("/payment_method_categories", tags=['payment_method_category'], status_code=201)
# async def payment_method_categories_get(db: Session = Depends(get_db)):
#     return {"Payment Method Categories": get_payment_method_categories(db=db)}