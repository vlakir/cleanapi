from cleanapi import server

if __name__ == '__main__':
    try:
        # protocol = 'https'
        protocol = 'http'
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
