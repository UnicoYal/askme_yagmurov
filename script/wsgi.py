def application(environ, start_response):
  method = environ['REQUEST_METHOD']

  # Query params
  query_string = environ.get('QUERY_STRING', '')

  # Body length
  try:
      content_length = int(environ.get('CONTENT_LENGTH', '0'))
  except ValueError:
      content_length = 0

  # Body params
  post_data = environ['wsgi.input'].read(content_length).decode('utf-8')

  # Prepare response
  status = '200 OK'
  headers = [('Content-Type', 'text/plain')]
  start_response(status, headers)

  response = f"Method: {method}\n"
  response += f"Query String: {query_string}\n"
  response += f"POST Data: {post_data}\n"

  return [response.encode('utf-8')]
