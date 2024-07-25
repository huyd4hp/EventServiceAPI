import hvac
class VaultClient:
    def __init__(self,VAULT_HOST,VAULT_TOKEN,VAULT_PORT=8200):
        self.client = hvac.Client(
            url= f"http://{VAULT_HOST}:{VAULT_PORT}",
            token=VAULT_TOKEN,
        )
        self.client.is_authenticated()
    def readSecret(self,path):
        return self.client.read(path)


