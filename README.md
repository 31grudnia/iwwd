## Technologies

* Python 3.10
* FastAPI
* Docker
* PostgreSQL
* Firebase

## Functionalities

* CRUD of tables
* Data validation 
* Password recovery via link sent to users email
* Hashing passwords
* JWT-based service authorization
* Data stored using PostgreSQL and Firebase

## How to run 

1. Building images and container

```bash
  docker-compose build
```
2. Starting Container:

```bash
  docker-compose up
```

3. Server data base (domyślnie [localhost:5050](localhost:5050))

4. Find "Servers". Click RMB and "Register->Server".

5. Fill: "Name: iwwd_db" 

6. Find "Connection" 

7. Fill: 
"Host name: db", 

"Maintance database: iwwd_db",

"Username: postgres",

"Password: password"

8. Migration:

```bash
  docker-compose run app alembic revision --autogenerate -m "New Migration"
```
9. Migration commit:

```bash
  docker-compose run app alembic upgrade head
```





    
