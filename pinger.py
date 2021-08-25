import requests
import json
import urllib3
from funnydeco import benchmark


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = 'http://localhost:8080'

url_pydantic = f'{host}/pydantic.json'

headers = {'Content-type': 'application/json'}

params_pydantic = {
                    "foo": 6660,
                    "bar": 4
                }


# noinspection PyUnusedLocal
@benchmark
def requester(url: str, params: dict, print_benchmark=False, benchmark_name='') -> None:
    response = requests.post(url, verify=False, data=json.dumps(params), headers=headers)
    print('Server response:')
    print(f'Status code - {response.status_code}')
    print(json.dumps(response.json(), sort_keys=False, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    print_bench = True
    bench_name = 'Request execution'

    requester(url_pydantic, params_pydantic, print_benchmark=print_bench, benchmark_name=bench_name)

