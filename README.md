
## How to run for Szamil

1. Zbudowanie obrazów i kontenerów od zera:

```bash
  docker-compose build
```
2. Uruchomienie Kontera:

```bash
  docker-compose up
```

3. Następnie przechodzimy do bazy danych (domyślnie [localhost:5050](localhost:5050))

4. Po lewej stronie widzymy jedną zakładkę "Servers". Klikamy na nią PRAWYM przyciskiem myszki i wybieramy opcję "Register->Server".

5. Uzupełniamy: "Name: iwwd_db" 

6. Wybieramy zakładkę "Connection" (Ponad polem, które właśnie wypełniliśmy)

7. Uzupełniamy: 
"Host name: db", 

"Maintance database: iwwd_db",

"Username: postgres",

"Password: password"

8. Stworzenie migracji :

```bash
  docker-compose run app alembic revision --autogenerate -m "New Migration"
```
9. Popchnięcie migracji:

```bash
  docker-compose run app alembic upgrade head
```

# For Mikołaj only 
pip3 freeze > requirements.txt




    