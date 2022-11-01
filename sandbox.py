from intuitlib.client import AuthClient
from intuitlib.migration import migrate
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError

REALM_ID = "4620816365251923790"


auth_client = AuthClient(
    client_id="*******",
    client_secret="********",
    environment="sandbox",
    redirect_uri="http://localhost:80",
)

url = auth_client.get_authorization_url([Scopes.ACCOUNTING])

# auth_client.get_bearer_token(auth_code, realm_id=realm_id)


