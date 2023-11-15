
from app.config import database

from .repository.repository import OrderRepository

# class Config(BaseSettings):
# HERE_API_KEY: str


class Service:
    def __init__(self):
        # config = Config()        
        self.repository = OrderRepository(database)
        # self.s3_service = S3Service()
        # self.here_service = HereService(config.HERE_API_KEY)


def get_service():
    svc = Service()
    return svc
