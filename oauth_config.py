import os
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.facebook import FacebookOAuth2
from httpx_oauth.clients.github import GitHubOAuth2

# OAuth configurations
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

# OAuth clients
google_oauth = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
facebook_oauth = FacebookOAuth2(FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET)
github_oauth = GitHubOAuth2(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET)

# Redirect URI (update this with your Replit app URL)
REDIRECT_URI = "https://your-replit-app-url.repl.co/callback"
