import os
import dotenv

dotenv.load_dotenv() # Load environment variables


def env(key: str, default_value = None):
    return os.environ.get(key, default_value)


is_production = env('ENV') == 'production'
