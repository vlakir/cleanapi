from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler
from cleanapi.third_party_libs import importdir


# noinspection PyAbstractClass
class BaseHandler(RequestHandler):
    """
    Generic parent for API request handlers
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
        Set headers
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')


def start(protocol: str, port: int, static_html_url: str, path_to_handler_dir: str,
          path_to_static_html: str, path_to_ssl='./ssl', ssl_certfile_name='ca.csr', ssl_keyfile_name='ca.key',
          enable_consol_messages=True) -> None:
    """
    Creating nodes and launching the API server
    :param protocol: protocol ('http' or 'https')
    :type protocol: str
    :param port: port
    :type port: int
    :param static_html_url: url of static html content relative to the root of the web server (must start with '/')
    :type static_html_url: str
    :param path_to_handler_dir: path to the folder with handlers (relative to the location of the calling script)
    :type path_to_handler_dir: str
    :param path_to_static_html: path to the folder with static html content
    :type path_to_static_html: str
    :param path_to_ssl: path to the folder with ssl certificates (for https only)
    :type path_to_ssl: str
    :param ssl_certfile_name: the file name of the ssl certificate (for https only)
    :type ssl_certfile_name: str
    :param ssl_keyfile_name: file name of the ssl key (for https only)
    :type ssl_keyfile_name: str
    :param enable_consol_messages: print startup messages
    :type enable_consol_messages: bool
    """
    handlers = get_handlers(path_to_handler_dir)

    if enable_consol_messages:
        root_url = f'{protocol}://localhost:{port}'
        print(f'Server is listening...')
        print('Available nodes:')
        for handler in handlers:
            print(f'{root_url}{handler.url_tail}')
        print('Static html root:')
        print(f'{root_url}{static_html_url}')

    static_content_path = path_to_static_html.strip('/')

    urls_json = []
    for handler in handlers:
        urls_json.append((handler.url_tail, handler.Handler))

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


def get_handlers(path_to_handlerd_dir: str) -> list:
    """
    Returns all handlers in the given folder
    Attention! Do not put any another .py files to this folder
    :param path_to_handlerd_dir: path to the folder
    :type path_to_handlerd_dir: str
    :return: handlers
    :rtype: list
    """
    path_to_handlerd_dir.strip('/')

    importdir_dict = {}
    importdir.do(path_to_handlerd_dir.strip('/'), importdir_dict)

    list_handler_instances = []
    for __, value in importdir_dict.items():
        list_handler_instances.append(value)

    return list_handler_instances
