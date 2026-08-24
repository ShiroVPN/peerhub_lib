from uuid import UUID, uuid4

from pydantic import AmqpDsn

from shiro_peerhub_worker.broker import (
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

from shiro_peerhub_worker.models import Success

# after define_broker was called
from shiro_peerhub_worker.workers import enable_peer

from .dependencies import db_dependency


@broker.task(task_name=enable_peer.task_name)
async def _enable_peer_impl(id: UUID, db: db_dependency) -> Success:
    return Success()


if __name__ == "__main__":
    print("Success!")
