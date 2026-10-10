"""Use Google's official Colab MCP through a persistent stdio client."""
from pathlib import Path
import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).resolve().parent
CONTROL = HERE / 'mcp_control'

def save(name, value):
    (CONTROL / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

async def main():
    CONTROL.mkdir(exist_ok=True)
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / 'colab_server.py')])
    with (CONTROL / 'server-stderr.log').open('w', encoding='utf-8') as errors:
        async with stdio_client(params, errlog=errors) as (read, write):
            async with ClientSession(read, write) as session:
                init = await session.initialize()
                available = await session.list_tools()
                save('initial_tools.json', available.model_dump(mode='json'))
                save('client_status.json', {'status':'initialized', 'server':init.serverInfo.model_dump(mode='json')})
                print('Official Colab MCP initialized.', flush=True)
                seen = {
                    item.name.replace('response-', 'request-')
                    for item in CONTROL.glob('response-*.json')
                }
                while not (CONTROL / 'stop.json').exists():
                    for request_file in sorted(CONTROL.glob('request-*.json')):
                        if request_file.name in seen:
                            continue
                        request = json.loads(request_file.read_text(encoding='utf-8'))
                        seen.add(request_file.name)
                        result_file = request_file.name.replace('request-', 'response-')
                        try:
                            if request['method'] == 'list_tools':
                                result = await session.list_tools()
                            else:
                                result = await session.call_tool(request['name'], request.get('arguments', {}))
                            save(result_file, result.model_dump(mode='json'))
                            print(request_file.name + ' completed.', flush=True)
                        except Exception as exc:
                            save(result_file, {'error':type(exc).__name__, 'message':str(exc)})
                            print(request_file.name + ' failed: ' + type(exc).__name__, flush=True)
                    await asyncio.sleep(0.25)
                save('client_status.json', {'status':'closed'})

if __name__ == '__main__':
    asyncio.run(main())
