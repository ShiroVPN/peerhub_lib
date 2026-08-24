from uuid import uuid4

from pydantic import AmqpDsn
from taskiq.middlewares.taskiq_admin_middleware import TaskiqAdminMiddleware
from taskiq_redis import RedisAsyncResultBackend

from shiro_peerhub_worker.broker import (
    BrokerConfigForClient,
    create_broker_for_client,
    define_broker,
    route_task_to_peerhub,
)

broker_config = BrokerConfigForClient(
    broker_url=AmqpDsn("amqp://user:password@localhost:5672"),
    exchange_name="kiwi",
)

broker = (
    create_broker_for_client(broker_config)
    .with_result_backend(
        RedisAsyncResultBackend("redis://localhost:6379/0"),
    )
    .with_middlewares(
        TaskiqAdminMiddleware(
            url="http://localhost:3000",
            api_token="secure_string",
            taskiq_broker_name="peerhub",
        )
    )
)

define_broker(broker)

# after define_broker was called
from shiro_peerhub_worker.workers import enable_peer


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
