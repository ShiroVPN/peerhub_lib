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
