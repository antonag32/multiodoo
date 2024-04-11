#!/usr/bin/env python3

from argparse import ArgumentParser
from multiprocessing import Process
from random import randint, choice
from time import sleep

import docker


class ChaosMonkey(Process):
    def __init__(self, amount, min_wait, max_wait):
        super().__init__(target=self.work)
        self.amount = amount
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.running = []
        self.stopped = []

    def work(self):
        client = docker.from_env()
        self.running = client.containers.list(filters={"name": "multiodoo-odoo", "status": "running"})
        self.stopped = client.containers.list(filters={"name": "multiodoo-odoo", "status": "exited"})
        if not self.running and not self.stopped:
            print("No containers found. Stopping...")
            return

        if self.amount < 0:
            self.amount = len(self.running) - 1

        while True:
            sleep(randint(self.min_wait, self.max_wait))
            if len(self.stopped) == self.amount:
                self.start_random_container()

            stop = choice([True, False])
            if self.running and stop:
                self.kill_random_container()
            else:
                self.start_random_container()

    def kill_random_container(self):
        if not self.running:
            return

        index = randint(0, len(self.running) - 1)
        container = self.running.pop(index)

        print(f"Stopping {container.name}")
        container.kill()
        self.stopped.append(container)

    def start_random_container(self):
        if not self.stopped:
            return

        index = randint(0, len(self.stopped) - 1)
        container = self.stopped.pop(index)

        print(f"Starting {container.name}")
        container.start()
        self.running.append(container)


def main():
    parser = ArgumentParser(description="This chaos monkey randomly turns off Odoo servers")
    parser.add_argument(
        "-n",
        "--amount",
        help="How many instances can be off at the same time",
        default=-1,
    )
    parser.add_argument(
        "--min-wait",
        help="Minimum amount of seconds before causing more chaos",
        default=3,
        type=int,
    )
    parser.add_argument(
        "--max-wait",
        help="Maximum amount of seconds before causing more chaos",
        default=10,
        type=int,
    )
    args = parser.parse_args()

    print("Starting Chaos Monkey")
    monkey = ChaosMonkey(args.amount, args.min_wait, args.max_wait)
    monkey.start()
    monkey.join()


if __name__ == "__main__":
    main()
