class Development:
    # database name://user:password:localhost:port/dbname e.g postgresql://postgres:12121994@127.0.0.1.5432/PetManagementSystem
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12121994@127.0.0.1:5432/Techome'
    # DEBUG = True  # since we are in development mode
    # SECRET_KEY = "12121994"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    Pass


class Production:
    SQLALCHEMY_DATABASE_URI = 'postgres://blufcyfuephvbf:f6bb9cce21036c899c21ea893eb19ef5568e2ef2c22316547c6ee5f3f149206a@ec2-176-34-184-174.eu-west-1.compute.amazonaws.com:5432/d36lve8t356t1v'
    DEBUG = False
    #pass



