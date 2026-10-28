import asyncio, json, logging, os
from pydantic import TypeAdapter, ValidationError
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from .audit import AuditStore
from .auth import AuthenticationError, authenticate
from .intake import evaluate
from .schemas import ApproveAsset, DeployMission, Envelope, GetState, IncomingMessage, SubmitAsset

logging.basicConfig(level=logging.INFO, format="[J-ROC AI FACTORY] %(asctime)s %(levelname)s %(message)s")
ADAPTER=TypeAdapter(IncomingMessage)

class Factory:
    def __init__(self):
        self.clients=set(); self.missions={}; self.store=AuditStore(os.getenv("JROC_DB","jroc_factory.db"))
    async def send(self, ws, event, request_id=None, data=None):
        await ws.send(Envelope(event=event,request_id=request_id,data=data or {}).model_dump_json())
    async def broadcast(self,event,data):
        if not self.clients: return
        payload=Envelope(event=event,data=data).model_dump_json()
        results=await asyncio.gather(*(c.send(payload) for c in tuple(self.clients)),return_exceptions=True)
        for c,r in zip(tuple(self.clients),results):
            if isinstance(r,Exception): self.clients.discard(c)
    async def handler(self,ws):
        try:
            await authenticate(ws)
        except AuthenticationError:
            await ws.close(code=4401,reason="Unauthorized"); return
        self.clients.add(ws); await self.send(ws,"AUTHENTICATED",data={"service":"J-ROC AI Factory"})
        try:
            async for raw in ws:
                try: msg=ADAPTER.validate_json(raw)
                except ValidationError as exc:
                    await self.send(ws,"VALIDATION_ERROR",data={"errors":exc.errors(include_url=False)}); continue
                await self.dispatch(ws,msg)
        except ConnectionClosed: pass
        finally: self.clients.discard(ws)
    async def dispatch(self,ws,msg):
        if isinstance(msg,SubmitAsset):
            decision=evaluate(msg.asset); payload=msg.asset.model_dump(mode="json")
            self.store.put_asset(msg.asset.asset_id,decision.state,payload); digest=self.store.append("ASSET_INTAKE",{"asset_id":msg.asset.asset_id,"decision":decision.__dict__})
            await self.send(ws,"ASSET_INTAKE_DECISION",msg.request_id,{**decision.__dict__,"asset_id":msg.asset.asset_id,"audit_hash":digest})
        elif isinstance(msg,ApproveAsset):
            asset=self.store.get_asset(msg.asset_id)
            if not asset or asset["state"]!="PENDING_APPROVAL": await self.send(ws,"REQUEST_REJECTED",msg.request_id,{"reason":"Asset is not awaiting approval."}); return
            self.store.put_asset(msg.asset_id,"APPROVED",asset["payload"]); digest=self.store.append("ASSET_APPROVED",msg.model_dump())
            await self.send(ws,"ASSET_APPROVED",msg.request_id,{"asset_id":msg.asset_id,"audit_hash":digest})
        elif isinstance(msg,DeployMission):
            asset=self.store.get_asset(msg.asset_id)
            if not asset or asset["state"]!="APPROVED": await self.send(ws,"REQUEST_REJECTED",msg.request_id,{"reason":"Only approved assets may be deployed."}); return
            if msg.mission_id in self.missions: await self.send(ws,"REQUEST_REJECTED",msg.request_id,{"reason":"Mission identifier already exists."}); return
            self.missions[msg.mission_id]={"status":"QUEUED","progress":0,"asset_id":msg.asset_id,"target_component":msg.target_component}
            asyncio.create_task(self.run_mission(msg.mission_id)); await self.send(ws,"MISSION_ACCEPTED",msg.request_id,{"mission_id":msg.mission_id})
        elif isinstance(msg,GetState):
            await self.send(ws,"FACTORY_STATE",msg.request_id,{"assets":self.store.list_assets(),"missions":self.missions})
    async def run_mission(self,mission_id):
        phases=[("SCOUTING",20),("COMPLIANCE_REVIEW",40),("TRIAGING",60),("INTEGRATION_TESTING",85),("COMPLETE",100)]
        for status,progress in phases:
            self.missions[mission_id].update(status=status,progress=progress); digest=self.store.append("MISSION_UPDATE",{"mission_id":mission_id,**self.missions[mission_id]})
            await self.broadcast("MISSION_UPDATE",{"mission_id":mission_id,**self.missions[mission_id],"audit_hash":digest})
            if progress<100: await asyncio.sleep(0.5)

async def main():
    factory=Factory(); host=os.getenv("JROC_HOST","127.0.0.1"); port=int(os.getenv("JROC_PORT","8765"))
    async with serve(factory.handler,host,port,max_size=64*1024,ping_interval=20,ping_timeout=20) as server:
        logging.info("Listening on ws://%s:%s",host,port); await server.serve_forever()
if __name__=="__main__": asyncio.run(main())
