import sys

methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "CONNECT"]
response = ["200 OK", "400 BAD REQUEST", "500 INTERNAL SERVER ERROR"]
reserved = [";", ":", "@", "+", "$", ","]
HTTP_VERSION = ['HTTP/1.0', 'HTTP/1.1', 'HTTP/2.0']


def parse_header(line):
    if ': ' not in line:
        raise ValueError("Invalid header format")
    key, value = line.split(': ', 1)
    return key, value


def parse_request(request):
    try:
        lines = request.split("\r\n")
        method, uri, http_version = lines[0].split(' ')

        if method not in methods or any(res in uri for res in reserved) or http_version not in HTTP_VERSION:
            return f"400 BAD REQUEST"

        path, _, query_string = uri.partition('?')

        # Parsing query string into a dictionary
        query_params = {}
        if query_string:
            query_items = query_string.split('&')
            for item in query_items:
                key, value = item.split('=', 1)
                query_params[key] = value

        headers = {}
        for line in lines[1:]:
            if line:
                key, value = parse_header(line)
                headers[key] = value
            else:
                break

        body = ""
        if len(lines) > 2 and lines[-1] != '':
            _, body = request.split("\r\n\r\n", 1)

        return method, path, http_version, headers, body, query_params

    except Exception as e:
        return f"500 INTERNAL SERVER ERROR - {e}"


def parse_request_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            file_contents = file.read()
            return parse_request(file_contents)
    except FileNotFoundError:
        return f"File '{filepath}' Not Found"
    except Exception as e:
        return f"Error reading file '{filepath}': {e}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python http_parser.py <file_path>')
        sys.exit(1)
    file_path = sys.argv[1]
    response = parse_request_from_file(file_path)
    print(response)
