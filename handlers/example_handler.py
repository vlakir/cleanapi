from cleanapi.server import BaseHandler

url_tail = '/example.json'


# noinspection PyAbstractClass
class Handler(BaseHandler):
    """
    Test API request handler
    """
    async def get(self):
        self.set_status(200)
        self.write({'status': 'working'})
