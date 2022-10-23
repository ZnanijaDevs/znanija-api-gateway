# Znanija Tools Server

**Purpose**: communicating with Brainly legacy API and Brainly GraphQL API

__Swagger API is available on `https://tools.br-helper.com/documentation`__

## Run

You must have:
* `.env.debug` to run this app in debug mode
* `.env` to run this app in production mode
```env
AUTH_USER = "admin"
AUTH_PASSWORD = "password (Basic auth)"
BRAINLY_LEGACY_API_HOST = "https://znanija.com"
BRAINLY_GRAPHQL_API_URL = "https://znanija.com/graphql/ru"
BRAINLY_AUTH_TOKEN = "<auth-token>"
BRAINLY_PROXY_HOST_URL="https://znanija.com" # CloudFlare must not protect this host
BRAINLY_PROXY_AUTH_PASS="<base64-pass-to-proxy>"
APP_VERSION="1.0.0"
APP_NAME="Znanija Tools"
ROLLBAR_ACCESS_TOKEN="<token>" // used in production
```
Also please create `secret_constants.py` with **1 variable** - `AUTH_HEADER` in `test` to make tests work.