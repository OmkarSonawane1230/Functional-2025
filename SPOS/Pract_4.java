
// Write a program to solve Classical Problems of Synchronization using Mutex and Semaphore.

import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.Semaphore;

class ProducerConsumer {
	private final Queue<Integer> buffer = new LinkedList<>();
	private final int capacity;
	private final Semaphore empty;
	private final Semaphore full;
	private final Object mutex = new Object();

	public ProducerConsumer(int capacity) {
		this.capacity = capacity;
		this.empty = new Semaphore(capacity);
		this.full = new Semaphore(0);
	}

	public void produce(int item) throws InterruptedException {
		empty.acquire();
		synchronized (mutex) {
			buffer.add(item);
			System.out.println("Produced: " + item);
		}
		full.release();
	}

	public int consume() throws InterruptedException {
		full.acquire();
		int item;
		synchronized (mutex) {
			item = buffer.poll();
			System.out.println("Consumed: " + item);
		}
		empty.release();
		return item;
	}
}

public class Pract_4 {
	public static void main(String[] args) {
		ProducerConsumer pc = new ProducerConsumer(5);

		// Producer thread
		Thread producer = new Thread(() -> {
			for (int i = 1; i <= 10; i++) {
				try {
					pc.produce(i);
					Thread.sleep(100);
				} catch (InterruptedException e) {
					Thread.currentThread().interrupt();
				}
			}
		});

		// Consumer thread
		Thread consumer = new Thread(() -> {
			for (int i = 1; i <= 10; i++) {
				try {
					pc.consume();
					Thread.sleep(150);
				} catch (InterruptedException e) {
					Thread.currentThread().interrupt();
				}
			}
		});

		producer.start();
		consumer.start();
		try {
			producer.join();
			consumer.join();
		} catch (InterruptedException e) {
			Thread.currentThread().interrupt();
		}
	}
}
