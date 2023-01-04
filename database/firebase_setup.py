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

DEFAULT_USER_IMAGES = ["profile_picture_man.png", "profile_picture_woman.png"]
DEFAULT_BRAMD_IMAGES = ["https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/brand_images%2FRoyal_horse.png?alt=media&token=6d32439d-f6df-4df3-b66b-dd13d26fe1d6",
                        "https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/brand_images%2FCats_among_us.png?alt=media&token=f056bac3-4969-4874-866c-596b88c9bd17",
                        "https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/brand_images%2FSilence_of_the_dogs.png?alt=media&token=868524d5-52c2-414e-941b-579d503d46e8"]

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
