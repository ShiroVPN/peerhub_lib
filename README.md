# Peerhub python package

This is a python pkg that declares `peerhub` workers. It is used in `main api` to manage peers and in `peerhub workers` to execute tasks.

# Usage example on client

```python
from uuid import uuid4

from pydantic import AmqpDsn
from taskiq_redis import RedisAsyncResultBackend

from shiro_peerhub.broker import (
    BrokerConfigForClient,
    create_broker_for_client,
    define_broker,
)

broker_config = BrokerConfigForClient(
    broker_url=AmqpDsn("amqp://user:password@localhost:5672"),
    exchange_name="kiwi",
)

broker = create_broker_for_client(broker_config).with_result_backend(
    RedisAsyncResultBackend("redis://localhost:6379/0"),
)

define_broker(broker)

# after define_broker was called

from shiro_peerhub.util import route_task_to_peerhub
from shiro_peerhub.workers import enable_peer


async def main():
    task = await route_task_to_peerhub(
        enable_peer,
        uuid4(),
    ).kiq(
        uuid4(),
    )
    result = await task.wait_result()
    print(result.return_value)


if __name__ == "__main__":
    print("Success!")
```

# Usage example on worker

```python
from uuid import UUID, uuid4

from pydantic import AmqpDsn

from shiro_peerhub.broker import (
    BrokerConfigForWorker,
    create_broker_for_worker,
    define_broker,
)

broker_config = BrokerConfigForWorker(
    broker_url=AmqpDsn("amqp://user:password@localhost:5672"),
    exchange_name="kiwi",
    queue_name="q",
    peerhub_id=uuid4(),
)

broker = create_broker_for_worker(broker_config)

define_broker(broker)

# after define_broker was called

from shiro_peerhub.models import Success
from shiro_peerhub.util import define_task
from shiro_peerhub.workers import enable_peer

from .dependencies import db_dependency


# method 1
@define_task(enable_peer)
async def enable_peer_impl(id: UUID, db: db_dependency) -> Success:
    return Success()


# method 2
@broker.task(task_name=enable_peer.task_name)
async def enable_peer_impl(id: UUID, db: db_dependency) -> Success:
    return Success()


# method 3
_ = broker.register_task(enable_peer_impl, enable_peer.task_name)


if __name__ == "__main__":
    print("Success!")
```

# Models

> same for all types of peerhub workers.

| Name    | Fields                                   |
| ------- | ---------------------------------------- |
| Peer    | id: UUID<br/>name: str<br/>enabled: bool |
| PeerAdd | name: str<br/>id: UUID                   |
| Success | ok: bool = True                          |

# Workers

> same for all types of peerhub workers.

| Name                 | Input   | Output  |
| -------------------- | ------- | ------- |
| peerhub.get_peer     | UUID    | Peer    |
| peerhub.add_peer     | PeerAdd | Peer    |
| peerhub.enable_peer  | UUID    | Success |
| peerhub.disable_peer | UUID    | Success |
| peerhub.delete_peer  | UUID    | Success |
| peerhub.get_config   | UUID    | str     |

# Exceptions

| Name           | Description                                 |
| -------------- | ------------------------------------------- |
| peer_not_found | Raised if peer with given id was not found. |
