import json
import asyncio
import aiohttp


class Wirecard(object):

    def __init__(self, environment, key, token):
        self.environment = environment
        self.key = key
        self.token = token
        if environment == 'production':
            self.base_url = 'https://api.moip.com.br'
        elif environment == 'sandbox':
            self.base_url = 'https://sandbox.moip.com.br'

    async def get(self, url, parameters=None):
        auth = aiohttp.BasicAuth(self.token, self.key, 'utf-8')
        async with aiohttp.ClientSession() as client:
            async with client.get('{0}/{1}'.format(self.base_url, url),
                                  params=parameters,
                                  auth=auth) as response:
                assert response.status == 200
                return await response.text()

    async def post(self, url, status=200, parameters=None):
        headers = {
            'Content-type': 'application/json; charset="UTF-8"',
        }
        async with aiohttp.ClientSession() as client:
            auth = aiohttp.BasicAuth(self.token, self.key, 'utf-8')
            async with client.post('{0}/{1}'.format(self.base_url, url),
                                   data=json.dumps(parameters),
                                   headers=headers,
                                   auth=auth) as response:
                assert response.status == status
                return await response.text()

    async def post_customer(self, parameters):
        try:
            response = await self.post('v2/customers', status=201, parameters=parameters)
            return response
        except Exception as error:
            print(json.dumps({"status": "error", "message": str(error)}))

    async def get_customer(self, customer_id):
        try:
            response = await self.get('v2/customers/{0}'.format(customer_id))
            return response
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def post_creditcard(self, customer_id, parameters):
        try:
            response = await self.post(
                'v2/customers/{0}/fundinginstruments'.format(customer_id),
                status=201,
                parameters=parameters
            )
            data = json.loads(response)
            return data['creditCard']['id']
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def delete_creditcard(self, creditcard_id):
        try:
            async with aiohttp.ClientSession() as client:
                async with client.delete(
                        '{0}/v2/fundinginstruments/{1}'.format(self.base_url,
                                                               creditcard_id),
                        auth=(self.token, self.key)) as response:
                    return response.status
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def post_order(self, parameters):
        try:
            response = await self.post('v2/orders', status=201, parameters=parameters)
            return response
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def get_order(self, order_id):
        try:
            response = await self.get('v2/orders/{0}'.format(order_id))
            return response
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def post_payment(self, order_id, parameters):
        try:
            response = await self.post('v2/orders/{0}/payments'.format(order_id),
                                       parameters)
            return response.text()
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def get_payment(self, payment_id):
        try:
            response = await self.get('v2/payments/{0}'.format(payment_id))
            return response
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def capture_payment(self, payment_id):
        try:
            response = await self.post('v2/payments/{0}/capture'.format(payment_id))
            return response.text()
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def void_payment(self, payment_id):
        try:
            response = await self.post('v2/payments/{0}/void'.format(payment_id))
            return response.text()
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))

    async def account_exists(self, account_id):
        try:
            return await self.get('v2/accounts/{0}'.format(account_id)).status == 200
        except Exception as error:
            print(json.dumps({"status": "error", "message": error}))
