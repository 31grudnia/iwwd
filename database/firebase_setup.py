import pyrebase

config = {
  "apiKey": "AIzaSyD7tmTTkKaPwOW8MHt42ruhar2dd-xmduo",
  "authDomain": "iwwd-77dbe.firebaseapp.com",
  "databaseURL": "https://iwwd-77dbe-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "iwwd-77dbe",
  "storageBucket": "iwwd-77dbe.appspot.com",
  "messagingSenderId": "344923570857",
  "appId": "1:344923570857:web:13e6de707a2f5e105fdfb8",
  "measurementId": "G-RQLTSRR24G"
}

DEFAULT_USER_IMAGES = ["https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/user_images%2Fprofile_picture_man.png?alt=media&token=03c86f39-2a32-4892-8e39-16a79c8cf45e",
                       "https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/user_images%2Fprofile_picture_woman.png?alt=media&token=fddd1936-8adb-40bf-ac97-74f2a1fbc2a2"]
DEFAULT_BRAMD_IMAGES = ["https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/brand_images%2FRoyal_horse.png?alt=media&token=6d32439d-f6df-4df3-b66b-dd13d26fe1d6",
                        "https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/brand_images%2FCats_among_us.png?alt=media&token=f056bac3-4969-4874-866c-596b88c9bd17",
                        "https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/brand_images%2FSilence_of_the_dogs.png?alt=media&token=868524d5-52c2-414e-941b-579d503d46e8"]
DEFAULT_ANIMAL_IMAGE = "https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/animal_images%2FAnimal_image_placeholder.png?alt=media&token=5a4eab80-9d91-4d30-83ec-eff187e3d629"
DEFAULT_PRODUCT_IMAGE = "https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/product_images%2FProduct_image_placeholder.png?alt=media&token=54f5ce20-ca8b-4779-8dd1-3dd6889049c6"
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
