# pyright: reportUnusedParameter=false

__all__ = [
    "get_peer",
    "add_peer",
    "enable_peer",
    "disable_peer",
    "delete_peer",
    "get_config",
]

from .broker import broker

if broker is None:
    raise RuntimeError(
        """You can not use declared tasks before setting up broker. \
        Use 'declare_broker'."""
    )

from uuid import UUID

from .models import Peer, PeerAdd, Success


@broker.task(task_name="peerhub.get_peer")
async def get_peer(id: UUID) -> Peer: ...


@broker.task(task_name="peerhub.add_peer")
async def add_peer(peer_data: PeerAdd) -> Peer: ...


@broker.task(task_name="peerhub.enable_peer")
async def enable_peer(id: UUID) -> Success: ...


@broker.task(task_name="peerhub.disable_peer")
async def disable_peer(id: UUID) -> Success: ...


@broker.task(task_name="peerhub.delete_peer")
async def delete_peer(id: UUID) -> Success: ...


@broker.task(task_name="peerhub.get_config")
async def get_config(id: UUID) -> str: ...
