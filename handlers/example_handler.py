from cleanapi import BaseHandler


# noinspection PyAbstractClass
class Handler(BaseHandler):
    """
    Хендлер тестового API-запроса
    """
    url_tail = '/example.json'

    async def get(self):
        self.set_status(200)
        self.write({'status': 'working'})
