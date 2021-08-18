from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from cleanapi.imports import get_handlers
from tornado.web import RequestHandler


# noinspection PyAbstractClass
class BaseHandler(RequestHandler):
    """
    Абстрактный предок хендлера API-запроса
    """
    url_tail = ''

    def initialize(self) -> None:
        self._set_default_headers()

    async def get(self):
        self._write_error(f'Method get is not supported')

    async def post(self):
        self._write_error(f'Method post is not supported')

    async def head(self):
        self._write_error(f'Method head is not supported')

    async def options(self):
        self._write_error(f'Method options is not supported')

    def _write_error(self, message):
        status_code = 400
        self.set_status(status_code)
        self.write({'error': message})

    def _set_default_headers(self) -> None:
        """
        Устанавливает необходимые заголовки для API-хендлера
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')


def start(protocol: str, port: int, static_html_url: str, path_to_handler_dir: str,
          path_to_static_html: str, path_to_ssl='./ssl', ssl_certfile_name='ca.csr', ssl_keyfile_name='ca.key') -> None:
    """
    Содание нод и запуск API-сервера
    :param protocol: протокол ('http' или 'https')
    :type protocol: str
    :param port: порт
    :type port: int
    :param static_html_url: url статического html контента относительно корня web-сервера (начинается с '/')
    :type static_html_url: str
    :param path_to_handler_dir: путь к папке с хэндлерами относительно расположения вызывающего скрипта
    :type path_to_handler_dir: str
    :param path_to_static_html: путь к папке со статическим html контентом относительно расположения вызывающего скрипта
    :type path_to_static_html: str
    :param path_to_ssl: путь к папке c ssl сертификатами относительно расположения вызывающего скрипта (для https)
    :type path_to_ssl: str
    :param ssl_certfile_name: имя файла ssl сертификата (для https)
    :type ssl_certfile_name: str
    :param ssl_keyfile_name:  имя файла ssl ключа (для https)
    :type ssl_keyfile_name: str
    """
    static_content_path = path_to_static_html.strip('/')

    handlers = get_handlers(path_to_handler_dir)

    urls_json = []
    for handler in handlers:
        urls_json.append((handler.Handler.url_tail, handler.Handler))

    urls_json.append((r'/(favicon.ico)', StaticFileHandler,
                      {'path': static_content_path, 'default_filename': 'favicon.ico'}))

    urls_static = [
        (static_html_url.strip() + '(.*)', StaticFileHandler,
         {'path': static_content_path, 'default_filename': 'index.html'})
        ]

    urls_common = urls_json + urls_static
    application_common = Application(urls_common, debug=False)

    if protocol.strip().lower() == 'https':
        server_common = HTTPServer(application_common, ssl_options={
            'certfile': f'{path_to_ssl.strip("/")}/{ssl_certfile_name}',
            'keyfile': f'{path_to_ssl.strip("/")}/{ssl_keyfile_name}',
        })
    else:  # http
        server_common = HTTPServer(application_common)

    server_common.listen(port)

    IOLoop.instance().start()
