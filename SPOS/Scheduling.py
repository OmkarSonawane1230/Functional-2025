# Scheduling.py
# CPU Scheduling Algorithms: FCFS, SJF (Preemptive), Priority (Non-Preemptive), Round Robin

class Process:
    def __init__(self, id, arrival, burst, priority):
        self.id = id
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0
        self.finished = False


def fcfs(processes):
    processes.sort(key=lambda p: p.arrival)
    time = 0
    for proc in processes:
        time = max(time, proc.arrival)
        proc.waiting = time - proc.arrival
        time += proc.burst
        proc.completion = time
        proc.turnaround = proc.completion - proc.arrival
    print_table(processes, "FCFS")


def sjf_preemptive(processes):
    n = len(processes)
    completed = 0
    time = 0
    procs = [Process(p.id, p.arrival, p.burst, p.priority) for p in processes]
    while completed < n:
        shortest = None
        for proc in procs:
            if not proc.finished and proc.arrival <= time and proc.remaining > 0:
                if shortest is None or proc.remaining < shortest.remaining:
                    shortest = proc
        if shortest is None:
            time += 1
            continue
        shortest.remaining -= 1
        if shortest.remaining == 0:
            shortest.finished = True
            shortest.completion = time + 1
            shortest.turnaround = shortest.completion - shortest.arrival
            shortest.waiting = shortest.turnaround - shortest.burst
            completed += 1
        time += 1
    print_table(procs, "SJF (Preemptive)")


def priority_non_preemptive(processes):
    n = len(processes)
    time = 0
    completed = 0
    procs = [Process(p.id, p.arrival, p.burst, p.priority) for p in processes]
    done = [False] * n
    while completed < n:
        highest = None
        for proc in procs:
            if not done[proc.id-1] and proc.arrival <= time:
                if highest is None or proc.priority < highest.priority:
                    highest = proc
        if highest is None:
            time += 1
            continue
        time = max(time, highest.arrival)
        highest.waiting = time - highest.arrival
        time += highest.burst
        highest.completion = time
        highest.turnaround = highest.completion - highest.arrival
        done[highest.id-1] = True
        completed += 1
    print_table(procs, "Priority (Non-Preemptive)")


def round_robin(processes, tq):
    n = len(processes)
    time = 0
    completed = 0
    procs = [Process(p.id, p.arrival, p.burst, p.priority) for p in processes]
    from collections import deque
    q = deque()
    in_queue = [False] * n
    while completed < n:
        for proc in procs:
            if not in_queue[proc.id-1] and proc.arrival <= time and proc.remaining > 0:
                q.append(proc)
                in_queue[proc.id-1] = True
        if not q:
            time += 1
            continue
        curr = q.popleft()
        exec_time = min(curr.remaining, tq)
        curr.remaining -= exec_time
        time += exec_time
        for proc in procs:
            if not in_queue[proc.id-1] and proc.arrival <= time and proc.remaining > 0:
                q.append(proc)
                in_queue[proc.id-1] = True
        if curr.remaining == 0:
            curr.completion = time
            curr.turnaround = curr.completion - curr.arrival
            curr.waiting = curr.turnaround - curr.burst
            completed += 1
        else:
            q.append(curr)
    print_table(procs, "Round Robin")


def print_table(processes, algo):
    print(f"\n--- {algo} Scheduling Result ---")
    print("ID\tArrival\tBurst\tPriority\tCompletion\tWaiting\tTurnaround")
    total_wait = 0
    total_turn = 0
    for proc in processes:
        print(f"{proc.id}\t{proc.arrival}\t{proc.burst}\t{proc.priority}\t{proc.completion}\t{proc.waiting}\t{proc.turnaround}")
        total_wait += proc.waiting
        total_turn += proc.turnaround
    print(f"Average Waiting Time: {total_wait/len(processes):.2f}")
    print(f"Average Turnaround Time: {total_turn/len(processes):.2f}")


def main():
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        print(f"Process {i+1}:")
        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))
        priority = int(input("Priority: "))
        processes.append(Process(i+1, arrival, burst, priority))
    while True:
        print("\nSelect Scheduling Algorithm:")
        print("1. FCFS")
        print("2. SJF (Preemptive)")
        print("3. Priority (Non-Preemptive)")
        print("4. Round Robin (Preemptive)")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 5:
            print("Exiting...")
            break
        copy = [Process(p.id, p.arrival, p.burst, p.priority) for p in processes]
        if choice == 1:
            fcfs(copy)
        elif choice == 2:
            sjf_preemptive(copy)
        elif choice == 3:
            priority_non_preemptive(copy)
        elif choice == 4:
            tq = int(input("Enter Time Quantum: "))
            round_robin(copy, tq)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
