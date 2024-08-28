from fastapi import Depends

from repository.user import UserRepo

from handlers.security import TokenHandler
from handlers.security import UserSession

from models.oauth import OauthRequest, AuthURL

from config import settings

from urllib.parse import urlencode

class OauthHandler:
    def __init__(
        self, 
        user_repo: UserRepo = Depends(UserRepo),
        token_handler: TokenHandler = Depends(TokenHandler),
        user_session: UserSession = Depends(UserSession),
    ) -> None:
        self._repo = user_repo
        self._token_handler = token_handler
        self._user_session = user_session

    def get_oauth(self, oauth_req: OauthRequest) -> AuthURL:
        if oauth_req.provider not in settings.PROVIDER:
            raise Exception("Invalid provider")
        oauth_config = settings.OAUTH.get(oauth_req.provider)
        auth_url = oauth_config["auth_url"]
        client_id = oauth_config["client_id"]
        scope = " ".join(oauth_config["scope"])
        redirect_uri = settings.REDIRECT_URI
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope
        }
        print(params)
        query_string = urlencode(params)
        authorization_url = f"{auth_url}?{query_string}"
        print(authorization_url)
        return AuthURL(url=authorization_url)