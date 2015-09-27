def application(environ, start_response):
    status = '200 OK'
    length = int(environ.get('CONTENT_LENGTH', '0')) 
    output = 'Hello world!!! ' + environ['QUERY_STRING'] + ' ' + environ['wsgi.input'].read(length);

    response_headers = [('Content-type', 'text/html; charset=utf-8'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
