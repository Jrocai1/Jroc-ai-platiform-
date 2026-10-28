import asyncio, os, uuid
from websockets.asyncio.client import connect

async def main():
    token=os.environ["JROC_AUTH_TOKEN"]
    async with connect(os.getenv("JROC_URL","ws://127.0.0.1:8765")) as ws:
        await ws.send(__import__("json").dumps({"action":"AUTH","token":token})); print(await ws.recv())
        rid=uuid.uuid4().hex
        await ws.send(__import__("json").dumps({"action":"SUBMIT_ASSET","request_id":rid,"asset":{"asset_id":"sample-mit","name":"Authorized sample component","source_url":"https://example.com/repository","legal_basis":"open_source","license_spdx":"MIT","intended_use":"Security-reviewed reusable component","preserves_attribution":True}})); print(await ws.recv())
if __name__=="__main__": asyncio.run(main())
