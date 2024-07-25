from consul import Consul
import os
class ConsulClient:
    def __init__(self,host:str="127.0.0.1",port:int=8500):
        self.client = Consul(
            host=host,
            port=port,
        )
    def RegisterService(self,service_id:str,name:str,address:str,port:int,tags:any):
        services = self.client.agent.services()
        if service_id in services:
            return
        self.client.agent.service.register(
            service_id=service_id,
            name=name,
            address=address,
            port=port,
            tags=tags,
        )
    def DeregisterService(self,service_id:str):
        self.client.agent.service.deregister(service_id)
    def AddCheck(self, service_id: str, name: str, http: str, interval: str="10s", timeout: str = "1s"):
        self.client.agent.check.register(
            name=name,
            check={
                "http": http,
                "interval": interval,
                "timeout": timeout,
                "service_id": service_id,
            }
        )
consulClient = ConsulClient(os.getenv("CONSUL_HOST"))