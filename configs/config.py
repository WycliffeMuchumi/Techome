# class Development:
#   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12121994@127.0.0.1:5432/Techome'
#   DEBUG = True  # since we are in development mode
#   SECRET_KEY = "12121994"
#   SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Pass


class Production:
    SQLALCHEMY_DATABASE_URI = 'postgres://vegyyixqcaeopk:558ba3166ccfc3fbb08244a69f9c10289840ece23e12199106abee3e9a5f50d2@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/dep8r0o8d5cdmg'
    DEBUG = False
    #pass



