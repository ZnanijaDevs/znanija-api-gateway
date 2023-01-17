# Znanija API Gateway

A service to communicate with Brainly legacy API and Brainly GraphQL API.

### How to run

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
ROLLBAR_ACCESS_TOKEN="<token>" // used in production
```