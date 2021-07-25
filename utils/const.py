JWT_SECRET_KEY = "b8b8eb7d1254a5fca3f4dbbb935402fa20a791cd83d5acfd673d9ff134758f68"  # $openssl rand -h 32
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5  # 5 days

TOKEN_DESCRIPTION = "It checks username and password, and returns JWT Token if authentication succeeds."
TOKEN_SUMMARY = "It returns JWT Token."

ISBN_DESCRIPTION = "It is unique identifier for books"