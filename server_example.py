from cleanapi import server

if __name__ == '__main__':
    # uses http protocol
    server.start('http', 8080, '/', './handlers', './static_html')

    # # uses https protocol
    # server.start('https', 8443, '/', './handlers', './static_html',
    #              path_to_ssl='./ssl', ssl_certfile_name='ca.csr', ssl_keyfile_name='ca.key')
