from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pizzaria_api_pkg.services.rastreamento_service import conectar_cliente, desconectar_cliente

router = APIRouter(prefix="/rastreamento", tags=["Rastreamento"])

@router.websocket("/ws/pedido/{pedido_id}")
async def rastrear_pedido(websocket: WebSocket, pedido_id: int):
    await conectar_cliente(pedido_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        desconectar_cliente(pedido_id, websocket)
