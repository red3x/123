from wsgiref.simple_server import make_server
import pytz
import json
from wsgiref.util import setup_testing_defaults, request_uri, shift_path_info
from datetime import datetime, timezone
from dateutil import parser


def get_web_app(url, uri):
   # print('\n#####GET#####')
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    timezone_var = url.replace(f'http://127.0.0.1:1337/', '')

    if uri == '':
        response = str(datetime.now(timezone.utc).time())[0:-7]
    else:
        if timezone_var in pytz.all_timezones:
            zone = pytz.timezone(timezone_var)
            response = str(datetime.now(zone))[11:19]
        else:
            response = ''
            status = '400 Bad Request'
    return headers, status, response



def post_web_app(url, env):
    print('\n#####POST#####')
    status = '200 OK'
    headers = [('Content-type', 'application/json; charset=utf-8')]
    response = ['json take']
    request = json.loads(env['wsgi.input'].read1().decode('utf-8').replace("\\", '')[1:-1])

    if url.count('convert') == 1:
        status, response = convert(request)
        return headers, status, response

    elif url.count('datediff') == 1:
        status, response = datediff(request)
        return headers, status, response
    else:
        print('####### ERROR IN POST ##########\n')
    return headers, status, response



def converter(input_dt, current_tz='UTC', target_tz='America/Indiana/Vevay'):
    print('\n#####CONVERTER#####')
    current_tz = pytz.timezone(current_tz)
    target_tz = pytz.timezone(target_tz)
    target_dt = current_tz.localize(input_dt).astimezone(target_tz)
    return str(target_tz.normalize(target_dt))[:-6]



def convert(request):
    print('\n#####CONVERT#####')
    status = '200 OK'
    if (request['target_tz']) in pytz.all_timezones:

        response = converter(parser.parse(request['date']['date']),request['date']['tz'],
                             request['target_tz'])
    else:
        response = ''
        status = '400 Bad Request'
        print('#####ERR CONVERT#####\n')
    return status, response



def datediff(request):
    print('\n##### DIFFERENCE #####')

    status = '200 OK'
    orig_date = parser.parse(request['first_date'])
    orig_tz = pytz.timezone(request['first_tz'])
    new_date = parser.parse(request['second_date'])
    new_tz = pytz.timezone(request['second_tz'])
    orig = orig_tz.localize(orig_date)
    new = new_tz.localize(new_date)
    response = [str((orig - new).total_seconds())]
    return status, response



def request_processing(env, start_response):
    status = '200 OK'
    setup_testing_defaults(env)
    method = env['REQUEST_METHOD']
    url = request_uri(env)
    uri = shift_path_info(env)

    if method == 'GET':
        headers, status, response = get_web_app(url, uri)

    elif method == 'POST':
        headers, status, response = post_web_app(url, env)

    start_response(status, headers)
    response = [x.encode('utf-8') for x in response]

    return response



with make_server('', 1337, request_processing) as app:
    print(f'Serving on 1337 port\nhttp://127.0.0.1:1337/')
    app.serve_forever()