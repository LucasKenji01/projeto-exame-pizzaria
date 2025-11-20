from typing import Dict, List
from fastapi import WebSocket

conexoes: Dict[int, List[WebSocket]] = {}

async def conectar_cliente(pedido_id: int, websocket: WebSocket):
    await websocket.accept()
    conexoes.setdefault(pedido_id, []).append(websocket)

def desconectar_cliente(pedido_id: int, websocket: WebSocket):
    conexoes[pedido_id].remove(websocket)

async def enviar_status(pedido_id: int, status: str):
    for ws in conexoes.get(pedido_id, []):
        await ws.send_text(f"Status atualizado: {status}")
