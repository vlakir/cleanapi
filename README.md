# cleanapi
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
│   └── example_handler.py
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

### example_handler.py
```python
from cleanapi import BaseHandler

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
