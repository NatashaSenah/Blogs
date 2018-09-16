import os
class Config:
    SECRET_KEY = os.environ.get('1234')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://student:learn@localhost/blog'



class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True
config_options = {
'development':DevConfig,
'production':ProdConfig
}