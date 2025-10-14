// (Non-Preemptive) and Round Robin (Preemptive).

import java.util.*;

class Process {
	int id, arrival, burst, priority, remaining, completion, waiting, turnaround;
	boolean finished;
	Process(int id, int arrival, int burst, int priority) {
		this.id = id;
		this.arrival = arrival;
		this.burst = burst;
		this.priority = priority;
		this.remaining = burst;
		this.finished = false;
	}
}

public class Scheduling {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter number of processes: ");
		int n = sc.nextInt();
		Process[] processes = new Process[n];
		for (int i = 0; i < n; i++) {
			System.out.println("Process " + (i+1) + ":");
			System.out.print("Arrival Time: ");
			int arrival = sc.nextInt();
			System.out.print("Burst Time: ");
			int burst = sc.nextInt();
			System.out.print("Priority: ");
			int priority = sc.nextInt();
			processes[i] = new Process(i+1, arrival, burst, priority);
		}
		while (true) {
			System.out.println("\nSelect Scheduling Algorithm:");
			System.out.println("1. FCFS");
			System.out.println("2. SJF (Preemptive)");
			System.out.println("3. Priority (Non-Preemptive)");
			System.out.println("4. Round Robin (Preemptive)");
			System.out.println("5. Exit");
			System.out.print("Enter your choice: ");
			int choice = sc.nextInt();
			if (choice == 5) {
				System.out.println("Exiting...");
				break;
			}
			// Deep copy to reset process states for each run
			Process[] copy = new Process[n];
			for (int i = 0; i < n; i++) {
				copy[i] = new Process(processes[i].id, processes[i].arrival, processes[i].burst, processes[i].priority);
			}
			switch (choice) {
				case 1: fcfs(copy); break;
				case 2: sjfPreemptive(copy); break;
				case 3: priorityNonPreemptive(copy); break;
				case 4: 
					System.out.print("Enter Time Quantum: ");
					int tq = sc.nextInt();
					roundRobin(copy, tq); break;
				default: System.out.println("Invalid choice");
			}
		}
	}

	static void fcfs(Process[] p) {
		Arrays.sort(p, Comparator.comparingInt(a -> a.arrival));
		int time = 0;
		for (Process proc : p) {
			time = Math.max(time, proc.arrival);
			proc.waiting = time - proc.arrival;
			time += proc.burst;
			proc.completion = time;
			proc.turnaround = proc.completion - proc.arrival;
		}
		printTable(p, "FCFS");
	}

	static void sjfPreemptive(Process[] p) {
		int n = p.length, completed = 0, time = 0;
		Process[] procs = Arrays.copyOf(p, n);
		while (completed < n) {
			Process shortest = null;
			for (Process proc : procs) {
				if (!proc.finished && proc.arrival <= time && proc.remaining > 0) {
					if (shortest == null || proc.remaining < shortest.remaining) {
						shortest = proc;
					}
				}
			}
			if (shortest == null) { time++; continue; }
			shortest.remaining--;
			if (shortest.remaining == 0) {
				shortest.finished = true;
				shortest.completion = time + 1;
				shortest.turnaround = shortest.completion - shortest.arrival;
				shortest.waiting = shortest.turnaround - shortest.burst;
				completed++;
			}
			time++;
		}
		printTable(procs, "SJF (Preemptive)");
	}

	static void priorityNonPreemptive(Process[] p) {
		int n = p.length, time = 0, completed = 0;
		Process[] procs = Arrays.copyOf(p, n);
		boolean[] done = new boolean[n];
		while (completed < n) {
			Process highest = null;
			for (Process proc : procs) {
				if (!done[proc.id-1] && proc.arrival <= time) {
					if (highest == null || proc.priority < highest.priority) {
						highest = proc;
					}
				}
			}
			if (highest == null) { time++; continue; }
			time = Math.max(time, highest.arrival);
			highest.waiting = time - highest.arrival;
			time += highest.burst;
			highest.completion = time;
			highest.turnaround = highest.completion - highest.arrival;
			done[highest.id-1] = true;
			completed++;
		}
		printTable(procs, "Priority (Non-Preemptive)");
	}

	static void roundRobin(Process[] p, int tq) {
		int n = p.length, time = 0, completed = 0;
		Process[] procs = Arrays.copyOf(p, n);
		Queue<Process> q = new LinkedList<>();
		boolean[] inQueue = new boolean[n];
		while (completed < n) {
			for (Process proc : procs) {
				if (!inQueue[proc.id-1] && proc.arrival <= time && proc.remaining > 0) {
					q.add(proc);
					inQueue[proc.id-1] = true;
				}
			}
			if (q.isEmpty()) { time++; continue; }
			Process curr = q.poll();
			int exec = Math.min(curr.remaining, tq);
			curr.remaining -= exec;
			time += exec;
			for (Process proc : procs) {
				if (!inQueue[proc.id-1] && proc.arrival <= time && proc.remaining > 0) {
					q.add(proc);
					inQueue[proc.id-1] = true;
				}
			}
			if (curr.remaining == 0) {
				curr.completion = time;
				curr.turnaround = curr.completion - curr.arrival;
				curr.waiting = curr.turnaround - curr.burst;
				completed++;
			} else {
				q.add(curr);
			}
		}
		printTable(procs, "Round Robin");
	}

	static void printTable(Process[] p, String algo) {
		System.out.println("\n--- " + algo + " Scheduling Result ---");
		System.out.println("ID\tArrival\tBurst\tPriority\tCompletion\tWaiting\tTurnaround");
		int totalWait = 0, totalTurn = 0;
		for (Process proc : p) {
			System.out.printf("%d\t%d\t%d\t%d\t%d\t%d\t%d\n", proc.id, proc.arrival, proc.burst, proc.priority, proc.completion, proc.waiting, proc.turnaround);
			totalWait += proc.waiting;
			totalTurn += proc.turnaround;
		}
		System.out.printf("Average Waiting Time: %.2f\n", totalWait/(float)p.length);
		System.out.printf("Average Turnaround Time: %.2f\n", totalTurn/(float)p.length);
	}
}

