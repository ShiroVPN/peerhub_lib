from collections.abc import Coroutine
from typing import TypeVar
from uuid import UUID

from aio_pika import ExchangeType
from pydantic import AmqpDsn, BaseModel
from taskiq import AsyncTaskiqDecoratedTask
from taskiq.kicker import AsyncKicker
from taskiq_aio_pika import AioPikaBroker, Exchange, Queue


class BrokerConfigForClient(BaseModel):
    broker_url: AmqpDsn
    exchange_name: str


class BrokerConfigForWorker(BrokerConfigForClient):
    queue_name: str
    peerhub_id: UUID


def create_broker_for_client(config: BrokerConfigForClient) -> AioPikaBroker:
    exchange = Exchange(name=config.exchange_name, type=ExchangeType.HEADERS)
    broker = AioPikaBroker(url=str(config.broker_url), exchange=exchange)
    return broker


def create_broker_for_worker(config: BrokerConfigForWorker) -> AioPikaBroker:
    exchange = Exchange(name=config.exchange_name, type=ExchangeType.HEADERS)
    task_queues = [
        Queue(
            name=config.queue_name,
            bind_arguments={
                "x-match": "all",
                "peerhub_id": str(config.peerhub_id),
            },
        )
    ]
    broker = AioPikaBroker(
        url=str(config.broker_url),
        exchange=exchange,
        task_queues=task_queues,
    )
    return broker


broker: AioPikaBroker | None = None


def define_broker(value: AioPikaBroker) -> None:
    global broker
    broker = value


C = TypeVar("C", bound=Coroutine[object, object, object])


def route_task_to_peerhub(
    task: AsyncTaskiqDecoratedTask[..., C],
    peerhub_id: UUID,
) -> AsyncKicker[..., C]:
    return task.kicker().with_labels(peerhub_id=str(peerhub_id))
