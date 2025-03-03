import aiohttp
from aiohttp import web

import asyncio
import aiofiles

import config
from create_bot import bot

from . import abstractions


class BitrixApi():
    def __init__(self, host: str, port: int, api_url: str, client_id: str, client_secret: str):
        self.host = host
        self.port = port

        self.client_id = client_id
        self.client_secret = client_secret

        self.api_url = api_url
        self.scope = 'crm,imopenlines,im'

        self.app = web.Application()
        self.app.add_routes([web.post('/message', self._on_message)])

    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()

        async with aiofiles.open('refresh_token', 'r') as file:
            self.refresh_token = await file.read()

        await self._update_token()

    async def send_message(self, message: abstractions.OutgoingMessage):
        data = {'CONNECTOR': config.connector_id, 'LINE': config.ol_id, 'MESSAGES': [message.data]}
        method = 'imconnector.send.messages'
        await self._post(method, data)

    async def add_lead(self, lead: abstractions.Lead):
        data = {'fields': lead.fields}
        method = 'crm.lead.add'
        await self._post(method, data)

    def configure(self):
        app = web.Application()
        app.add_routes([web.post('/install', self._get_first_token)])
        web.run_app(app, host=self.host, port=self.port)

    async def _get_first_token(self, request):
        data = await request.post()
        self.token = data['auth[access_token]']
        self.refresh_token = data['auth[refresh_token]']
        await self._write_refresh_token()
        await self._create_connector()
        await self._activate_connector()
        await self._bind_listener()
        print('App was configured succesful')
        quit()

    async def _bind_listener(self):
        data = {'event': 'OnImConnectorMessageAdd', 'handler': f'{config.host_url}/message'}
        method = 'event.bind'
        await self._post(method, data)

    async def _create_connector(self):
        data = {
            'ID': config.connector_id,
            'NAME': config.connector_name,
            'ICON': {'DATA_IMAGE': config.connector_pic, 'COLOR': '#a6ffa3', 'SIZE': '100%', 'POSITION': 'center'},
            'PLACEMENT_HANDLER': f'{config.host_url}:{config.port}'
        }

        method = 'imconnector.register'
        await self._post(method, data)

    async def _activate_connector(self):
        data = {'CONNECTOR': config.connector_id, 'LINE': config.ol_id, 'ACTIVE': 1}
        method = 'imconnector.activate'
        await self._post(method, data)

    async def _post(self, method: str, data: dict):
        params = {'auth': self.token, **data}
        url = f'{self.api_url}/{method}'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params) as response:
                response = await response.json()
                return response

    async def _on_message(self, request):
        data = await request.post()

        message = abstractions.IncomingMessage(data)

        if message.connector == config.connector_id:
            await bot.send_message(message.chat_id, text=message.text)
            await self._delievered(message)

    async def _delievered(self, message: abstractions.IncomingMessage):
        data = {'CONNECTOR': config.connector_id, 'LINE': config.ol_id, 'MESSAGES': [{'im': message.im}]}
        method = 'imconnector.send.status.delivery'
        await self._post(method, data)

    async def _write_refresh_token(self):
        async with aiofiles.open('refresh_token', 'w') as file:
            await file.write(self.refresh_token)

    async def _update_token(self):
        while True:

            data = {
                'grant_type': 'refresh_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': self.refresh_token,
                'scope': self.scope
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(config.token_update_url, params=data) as resp:
                    response = await resp.json()
                    self.token = response['access_token']
                    self.refresh_token = response['refresh_token']

            await self._write_refresh_token()

            await asyncio.sleep(config.token_update_time)


api = BitrixApi(config.host, config.port, config.api_url, config.client_id, config.client_secret)


if __name__ == '__main__':
    api.configure()
