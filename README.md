# cd FASTAPI
# uvicorn app.main:app --reload >>in cmd
# pip install -r requirements.txt


You need postgres installed and a database created for this project to work.
This is a simple posts app, created using Fastapi which has jwt token authoriation for user login and all the CRUD operations tested.


#models.Base.metadata.create_all(bind=engine) # this thing creates TABLES in postgres,
#no longer needed as using alembic


# alembic revision --autogenerate >>>>Then>>>  alembic upgrade head
# alembic revision --help, 
# , or +2 or +1 or downgrade etc


# uvicorn app.main:app --reload >>in cmd
    # its better to create new venv when project moves location, all module versions are saved in requirements.txt
    #( it runs a uvicorn server terminal unlike flask)
    #cd to FASTAPI if ASGI app error
    # >venv\Scripts\activate    
