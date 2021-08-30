[![PyPi Version](https://img.shields.io/pypi/v/cleanapi.svg?style=flat-square)](https://pypi.org/project/cleanapi)

# CleanAPI
Pretty tornado wrapper for making lightweight REST API services

____
## Installation:
```
pip install cleanapi
```
____
## Example:

### Project folders structure:
```
.
├── handlers
│   └── simple_handler.py
├── log
├── ssl
│   ├── ca.csr
│   └── ca.key
├── static_html
│   └── index.html
└── server_example.py
```

### server_example.py
```python
from cleanapi import server

if __name__ == '__main__':
    # uses http protocol
    server.start('http', 8080, '/', './handlers', './static_html')

    # # uses https protocol
    # server.start('https', 8443, '/', './handlers', './static_html',
    #              path_to_ssl='./ssl', ssl_certfile_name='ca.csr', ssl_keyfile_name='ca.key')
```

### simple_handler.py
```python
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
```

### index.html
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Cleanapy demo</title>
  <link rel="icon" href="/favicon.ico" type="image/x-icon" />
 </head>
<body>

<h1>Cleanapy demo page</h1>

<p>Everything OK</p>

</body>
</html>
```
You also may put 'favicon.ico' file to the 'static_html' folder, but it is not necessary.

Then you can test server responses on [http://localhost:8080](http://localhost:8080) and [http://localhost:8080/example.json](http://localhost:8080/example.json)

See log/cleanapi.log for information about externel access to the server
____

## Example with PydanticHandler:

### pydantic_handler.py
```python
from cleanapi.server import PydanticHandler
from pydantic import BaseModel, validator, NonNegativeInt
from typing import Optional, List


url_tail = '/pydantic.json'


class PydanticRequest(BaseModel):
    """
    Pydantic dataclass for request
    """
    foo: NonNegativeInt
    bar: NonNegativeInt

    @validator('foo', 'bar')
    def _validate_foo_bar(cls, val: str):
        if val == 666:
            raise ValueError(f'Values of foo and bar should not be equal to 666')
        return val


class PydanticResponse(BaseModel):
    """
    Pydantic dataclass for response
    """
    summ: Optional[NonNegativeInt]
    errors: Optional[List[dict]]


# noinspection PyAbstractClass
class Handler(PydanticHandler):
    """
    Example of using PydanticHandler
    """
    request_dataclass = PydanticRequest
    result_dataclass = PydanticResponse

    # noinspection PyUnusedLocal
    def process(self, request: request_dataclass) -> result_dataclass:
        """
        What the handler should do
        :param request: incoming request
        :type request: request_dataclass
        :return: processing result
        :type: result_data class
        """
        result = PydanticResponse(summ=request.foo + request.bar, errors=[])

        if result.summ > 1000:
            raise ValueError('The sum of foo and bar is more than 1000')

        return result

    def if_exception(self, errors: list) -> None:
        """
        What to do if an exception was thrown
        :param errors: list of errors
        :type errors: list
        """
        self.set_status(400)
        self.write({'errors': errors})
        return
```

You can not test it with a browser because of POST method using. You have to use a program like Postman or some custom util like my pynger.py
