# Znanija Tools Server

**Purpose**: communicating with Brainly legacy API and Brainly GraphQL API

## Endpoints
### Tasks [`/brainly/task/`]
* `GET /{id}` - get Brainly question by ID
* `GET /log/{id}` - get Brainly question log by question ID
* `POST /deleted_tasks {"ids": int[]}` - check whether specified Brainly questions are deleted

### Users [`/brainly/users/`]
* `POST / {"ids": int[]}` - get Brainly users by IDs
* `POST /send_message` - send message to Brainly user. *You can send only 1 message per 1 request.*
  ```py
  {
    "user_id": int,
    "text": str
  }
  ```
* `POST /{id}/ban` - ban a user.
  ```py
  {
    "ban_type": int
  }
  ```
* `POST /{id}/cancel_ban` - cancels a ban for a user.

### Rankings [`/brainly/ranking/`]
* `GET /active_users` - get active users from Brainly rankings

### Feed [`/brainly/feed/`]
* `GET /` - get the Brainly feed

## Run

*You must have `.env.debug` for debugging this app.*
```env
AUTH_USER = "admin"
AUTH_PASSWORD = "password (Basic auth)"
BRAINLY_LEGACY_API_HOST = "https://znanija.com"
BRAINLY_GRAPHQL_API_URL = "https://znanija.com/graphql/ru"
BRAINLY_AUTH_TOKEN = "<auth-token>"
BRAINLY_PROXY_HOST_URL="https://znanija.com" # CloudFlare must not protect this host
BRAINLY_PROXY_AUTH_PASS="<base64-pass-to-proxy>"
```
Also please create `secret_constants.py` with **1 variable** - `AUTH_HEADER` in `test` to make tests work.