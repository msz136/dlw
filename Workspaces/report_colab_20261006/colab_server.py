"""Official pinned Colab MCP with room for this notebook's embedded figures."""
from colab_mcp import main
from colab_mcp import websocket_server
from colab_mcp import session

# The browser consent step can outlast the official one-minute window.
session.UI_CONNECTION_TIMEOUT = 600.0

# The four original report figures make a whole-notebook response exceed 1 MiB.
# Keep the official authentication and origin checks, and bound messages to 8 MiB.
_official_serve = websocket_server.websockets.serve

def _report_serve(*args, **kwargs):
    kwargs.setdefault('max_size', 8 * 1024 * 1024)
    return _official_serve(*args, **kwargs)

websocket_server.websockets.serve = _report_serve

if __name__ == '__main__':
    main()
