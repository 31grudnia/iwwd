# from sqlalchemy.orm import Session
# from fastapi import HTTPException
#
# # from database.models.PaymentMethodCategoryModel import PaymentMethodCategory as PaymentMethodCategoryModel
#
# from schemas import PaymentMethodCategorySchema


# def get_payment_method_category_by_id(db: Session, index: int):
#     return db.query(PaymentMethodCategoryModel).filter(PaymentMethodCategoryModel.id == index).first()
#
#
# def get_payment_method_category_by_name(db: Session, name: str):
#     return db.query(PaymentMethodCategoryModel).filter(PaymentMethodCategoryModel.name == name.title()).first()
#
#
# def get_payment_method_categories(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(PaymentMethodCategoryModel).offset(skip).limit(limit).all()
#
#
# def add_payment_method_category(db: Session, pmcategory: PaymentMethodCategorySchema):
#     pmcategory_check = get_payment_method_category_by_name(db=db, name=pmcategory.name.title())
#     if pmcategory_check:
#         raise HTTPException(status_code=410, detail="Payment Method Category already exists!")
#
#     db_pmcategory = PaymentMethodCategoryModel(name=pmcategory.name.title())
#     db.add(db_pmcategory)
#     db.commit()
#     db.refresh(db_pmcategory)
#     return db_pmcategory