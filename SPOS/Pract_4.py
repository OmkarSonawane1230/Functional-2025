# Pract_4.py
# Classical Producer-Consumer Problem using Mutex and Semaphore
import threading
import time
from collections import deque

class ProducerConsumer:
    def __init__(self, capacity):
        self.buffer = deque()
        self.capacity = capacity
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.mutex = threading.Lock()

    def produce(self, item):
        self.empty.acquire()
        with self.mutex:
            self.buffer.append(item)
            print(f"Produced: {item}")
        self.full.release()

    def consume(self):
        self.full.acquire()
        with self.mutex:
            item = self.buffer.popleft()
            print(f"Consumed: {item}")
        self.empty.release()
        return item

def main():
    pc = ProducerConsumer(5)

    def producer():
        for i in range(1, 11):
            pc.produce(i)
            time.sleep(0.1)

    def consumer():
        for i in range(1, 11):
            pc.consume()
            time.sleep(0.15)

    t_producer = threading.Thread(target=producer)
    t_consumer = threading.Thread(target=consumer)
    t_producer.start()
    t_consumer.start()
    t_producer.join()
    t_consumer.join()

if __name__ == "__main__":
    main()
