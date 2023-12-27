import asyncio

_tasks = set()


def create_task(task):
    task = asyncio.create_task(task)
    _tasks.add(task)
    task.add_done_callback(_tasks.discard)
    return task
