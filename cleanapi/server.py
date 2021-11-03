from tornado.web import Application
from tornado.web import StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler
from cleanapi.third_party_libs import importdir
from cleanapi.logger import server_logger
import json
from asgiref.sync import sync_to_async
from pydantic import BaseModel
from abc import abstractmethod


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


# noinspection PyAbstractClass
class PydanticHandler(BaseHandler):
    """
    Generic parent for handlers operating with pydantic data classes
    """

    request_dataclass = BaseModel
    result_dataclass = BaseModel

    async def post(self):
        errors = []

        try:
            body_json_dict = json.loads(self.request.body)

            input_request = self.request_dataclass(**body_json_dict)
            self.check_request(input_request)

            result = await sync_to_async(self.process)(input_request)
        except Exception as ex:
            errors.append({
                'error': {
                    'id': None,
                    'description': f'{str(ex.__class__.__name__)}: {str(ex)}'
                }
            })

            self.if_exception(errors)
            return

        if len(result.errors) == 0:
            result.errors = None
            status_code = 200
        else:
            status_code = 400

        output_json = result.json(exclude_none=True)

        self.set_status(status_code)
        self.write(output_json)

    # noinspection PyUnusedLocal
    @staticmethod
    @abstractmethod
    def process(request: request_dataclass) -> result_dataclass:
        """
        What the handler should do
        :param request: incoming request
        :type request: request_dataclass
        :return: processing result
        :type: result_data class
        """
        pass

    # noinspection PyUnusedLocal
    @abstractmethod
    def if_exception(self, errors: list) -> None:
        """
        What to do if an exception was thrown
        :param errors: list of errors
        :type errors: list
        """
        pass

    # noinspection PyUnusedLocal
    @staticmethod
    @abstractmethod
    def check_request(request: request_dataclass) -> None:
        """
        Checking the correctness of the incoming request.
        If an error is detected, then you need to throw ValueError
        :param request: incoming request
        :type request: request_dataclass
        """
        # raise ValueError
        pass


def start(protocol: str, port: int, static_html_url: str,
          path_to_handler_dir: str, path_to_static_html: str, path_to_log='./log', path_to_ssl='./ssl',
          ssl_certfile_name='ca.csr', ssl_keyfile_name='ca.key', enable_consol_messages=True,
          max_log_size_mb=10, max_log_back_up_count=5) -> None:
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
    :param path_to_log: path to the folder with log (relative to the location of the calling script)
    :type path_to_log: str
    :param path_to_ssl: path to the folder with ssl certificates (for https only)
    :type path_to_ssl: str
    :param ssl_certfile_name: the file name of the ssl certificate (for https only)
    :type ssl_certfile_name: str
    :param ssl_keyfile_name: file name of the ssl key (for https only)
    :type ssl_keyfile_name: str
    :param enable_consol_messages: print startup messages
    :type enable_consol_messages: bool
    :param max_log_size_mb: log files size limit in MB
    :type max_log_size_mb: int
    :param max_log_back_up_count: count of log backups created after exceeding the size limit
    :type max_log_back_up_count: int
    """
    try:
        server_logger.init(path_to_log, max_log_size_mb=max_log_size_mb, max_log_back_up_count=max_log_back_up_count)

        handlers = get_handlers(path_to_handler_dir)

        if enable_consol_messages:
            root_url = f'{protocol}://localhost:{port}'
            print(f'Cleanapi server is listening...')
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
        elif protocol.strip().lower() == 'http':
            server_common = HTTPServer(application_common)
        else:
            raise NotImplementedError(f'Protocol {protocol} is not supported')

        server_common.listen(port)

        IOLoop.instance().start()
    except KeyboardInterrupt:
        print('Cleanapi server was stopped by user')
        exit()


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
        if value.__name__ != '__init__':
            list_handler_instances.append(value)
    return list_handler_instances
