"""The central configuration file."""

from typing import Optional

from pydantic import BaseSettings, Field


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # These variables will be loaded from the .env file. However, if
    # there is a shell environment variable having the same name,
    # that will take precedence.

    # the class Field is necessary to while defining global variables
    ENV_STATE: Optional[str] = Field(..., env="ENV_STATE")
    API_USERNAME: Optional[str] = Field(..., env="API_USERNAME")
    API_PASSWORD: Optional[str] = Field(..., env="API_PASSWORD")
    REDIS_PASSWORD: Optional[str] = Field(..., env="REDIS_PASSWORD")

    # env specific configs will be pulled from .env with specific prefixes
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[str] = None

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


config = FactoryConfig(GlobalConfig().ENV_STATE)()
# print(config.__repr__())
