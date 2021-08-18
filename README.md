# cleanapi
Pretty tornado wrapper for making lightweight REST API services

____
## Installation:
```
pip install cleanapi
```
____
## Example:

### server_example.py
```python
from cleanapi import server

if __name__ == '__main__':
    try:
        # protocol = 'https'
        protocol = 'https'
        port = 8080
        static_html_url = '/'
        print(f'Server is listening {protocol} port {port}...')

        if protocol == 'https':
            server.start(protocol, port, static_html_url, './handlers', './static_html',
                         path_to_ssl='./ssl', ssl_certfile_name='ca.csr', ssl_keyfile_name='ca.key')
        elif protocol == 'http':
            server.start(protocol, port, static_html_url, './handlers', './static_html')
        else:
            print(f'Protocol {protocol} is not supported')
    except KeyboardInterrupt:
        print('Server stopped by user')
        exit()
```

### example_handler.py
Put it to the 'handlers' folder
```python
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
```

### index.html
Put it to the 'static_html' folder
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
You also may put 'favicon.ico' file to the 'static_html' folder

Then you can test server responses on [http://localhost:8080](http://localhost:8080) and [http://localhost:8080/example.json](http://localhost:8080/example.json)
____
