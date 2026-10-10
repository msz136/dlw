"""Queue native cell edits for the connected official Colab MCP client."""
from pathlib import Path
import argparse
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
CONTROL = HERE / 'mcp_control'

def call(number, name, arguments):
    request = CONTROL / f'request-{number:04d}.json'
    response = CONTROL / f'response-{number:04d}.json'
    if not request.exists():
        request.write_text(json.dumps({'method':'call_tool', 'name':name, 'arguments':arguments}, ensure_ascii=False), encoding='utf-8')
    while not response.exists():
        time.sleep(.25)
    result = json.loads(response.read_text(encoding='utf-8'))
    if result.get('isError') or result.get('error'):
        raise RuntimeError(f'{name}: {result}')
    return result

def main(base=100):
    notebook = json.loads((HERE / 'Report.ipynb').read_text(encoding='utf-8'))
    mapping = []
    for index, cell in enumerate(notebook['cells']):
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'code':
            name = 'add_code_cell'
            arguments = {'cellIndex':index, 'language':'python', 'code':source}
        else:
            name = 'add_text_cell'
            arguments = {'cellIndex':index, 'content':source}
        result = call(base + index, name, arguments)
        mapping.append({'local_id':cell['id'], 'index':index, 'cell_type':cell['cell_type'],
                        'source_sha256':hashlib.sha256(source.encode()).hexdigest(), 'response':result})
        (HERE / 'colab_cell_mapping.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"Inserted {index+1}/{len(notebook['cells'])}: {cell['id']}", flush=True)
    result = call(base + 200, 'get_cells', {'includeOutputs':False})
    remote = result.get('structuredContent')
    if remote is None:
        remote = json.loads(next(item['text'] for item in result['content'] if item['type']=='text'))
    actual = remote['cells'][:len(mapping)]
    assert len(actual) == len(mapping)
    for expected, observed in zip(mapping, actual):
        source = observed['source']
        if isinstance(source, list):
            source = ''.join(source)
        assert hashlib.sha256(source.encode()).hexdigest() == expected['source_sha256'], expected['local_id']
        expected['remote_id'] = observed['id']
    (HERE / 'colab_cell_mapping.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Verified exact source correspondence for {len(mapping)} native Colab cells.", flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', type=int, default=100)
    main(parser.parse_args().base)
