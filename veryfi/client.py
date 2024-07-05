from veryfi.documents import Documents
from veryfi.w9s import W9s
from veryfi.client_base import Client as ClientBase


class Client(ClientBase, Documents, W9s):
    def __init__(
        self,
        client_id,
        client_secret,
        username,
        api_key,
        base_url=ClientBase.BASE_URL,
        api_version=ClientBase.API_VERSION,
        timeout=ClientBase.API_TIMEOUT,
    ):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            timeout=timeout,
        )
        Documents.__init__(self, super())
        W9s.__init__(self, super())
