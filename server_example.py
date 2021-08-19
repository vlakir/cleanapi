from cleanapi import server

if __name__ == '__main__':
    try:
        # protocol = 'https'
        protocol = 'http'

        if protocol == 'https':
            server.start(protocol, 8080, '/', './handlers', './static_html',
                         path_to_ssl='./ssl', ssl_certfile_name='ca.csr', ssl_keyfile_name='ca.key')
        elif protocol == 'http':
            server.start(protocol, 8080, '/', './handlers', './static_html')
        else:
            print(f'Protocol {protocol} is not supported')
    except KeyboardInterrupt:
        print('Server was stopped by user')
        exit()
