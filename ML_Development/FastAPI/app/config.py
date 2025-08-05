from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #Here we can just provide a list of all the environment variables that we need set
    
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    model_config = SettingsConfigDict(env_file= ".env")
    
settings = Settings()   #Creating am instance of the Settings class

