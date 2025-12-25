
from collections import deque
from process import Process

class CPUScheduler:
    def __init__(self, processes, context_switch_time=0):

        self.processes = processes
        self.context_switch_time = context_switch_time
        self.timeline = []
        self.current_time = 0
    
    def reset_processes(self):

        for p in self.processes:
            p.reset()
        self.timeline = []
        self.current_time = 0
    
    def calculate_metrics(self):
        if not self.processes:
            return 0, 0
        
        avg_turnaround = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        avg_waiting = sum(p.waiting_time for p in self.processes) / len(self.processes)
        
        return avg_turnaround, avg_waiting
    
    def fcfs(self):
        self.reset_processes()
        sorted_processes = sorted(self.processes, key=lambda x: x.arrival_time)
        
        for process in sorted_processes:
            if self.current_time < process.arrival_time:
                self.current_time = process.arrival_time
            
            if process.start_time == -1:
                process.start_time = self.current_time
            
            self.timeline.append({
                'pid': process.pid,
                'start': self.current_time,
                'end': self.current_time + process.burst_time
            })
            
            self.current_time += process.burst_time
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.current_time += self.context_switch_time
        
        return self.calculate_metrics()
    
    def sjf_non_preemptive(self):
        self.reset_processes()
        remaining = self.processes.copy()
        
        while remaining:
            available = [p for p in remaining if p.arrival_time <= self.current_time]
            
            if not available:
                self.current_time = min(p.arrival_time for p in remaining)
                continue
            
            process = min(available, key=lambda x: x.burst_time)
            
            if process.start_time == -1:
                process.start_time = self.current_time
            
            self.timeline.append({
                'pid': process.pid,
                'start': self.current_time,
                'end': self.current_time + process.burst_time
            })
            
            self.current_time += process.burst_time
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            remaining.remove(process)
            
            if remaining:
                self.current_time += self.context_switch_time
        
        return self.calculate_metrics()
    
    def sjf_preemptive(self):
        self.reset_processes()
        remaining = self.processes.copy()
        current_process = None
        
        while remaining or current_process:
            available = [p for p in remaining if p.arrival_time <= self.current_time]
            
            if current_process and current_process.remaining_time > 0:
                available.append(current_process)
            
            if not available:
                if remaining:
                    self.current_time = min(p.arrival_time for p in remaining)
                continue
            
            process = min(available, key=lambda x: x.remaining_time)
            
            if current_process and current_process != process and current_process.remaining_time > 0:
                if self.context_switch_time > 0:
                    self.current_time += self.context_switch_time
            
            if process.start_time == -1:
                process.start_time = self.current_time
            
            next_arrival_time = float('inf')
            for p in remaining:
                if p.arrival_time > self.current_time:
                    next_arrival_time = min(next_arrival_time, p.arrival_time)
            
            execute_time = min(
                process.remaining_time,
                next_arrival_time - self.current_time if next_arrival_time != float('inf') else process.remaining_time
            )
            
            self.timeline.append({
                'pid': process.pid,
                'start': self.current_time,
                'end': self.current_time + execute_time
            })
            
            self.current_time += execute_time
            process.remaining_time -= execute_time
            
            if process.remaining_time == 0:
                process.completion_time = self.current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                if process in remaining:
                    remaining.remove(process)
                current_process = None
            else:
                current_process = process
                if process in remaining:
                    remaining.remove(process)
        
        return self.calculate_metrics()
    
    def priority_scheduling(self):
        self.reset_processes()
        remaining = self.processes.copy()
        
        while remaining:
            available = [p for p in remaining if p.arrival_time <= self.current_time]
            
            if not available:
                self.current_time = min(p.arrival_time for p in remaining)
                continue
            
            process = min(available, key=lambda x: x.priority)
            
            if process.start_time == -1:
                process.start_time = self.current_time
            
            self.timeline.append({
                'pid': process.pid,
                'start': self.current_time,
                'end': self.current_time + process.burst_time
            })
            
            self.current_time += process.burst_time
            process.completion_time = self.current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            remaining.remove(process)
            
            if remaining:
                self.current_time += self.context_switch_time
        
        return self.calculate_metrics()
    
    def round_robin(self, time_quantum=2):
        self.reset_processes()
        ready_queue = deque()
        remaining = sorted(self.processes.copy(), key=lambda x: x.arrival_time)
        
        while remaining and remaining[0].arrival_time <= self.current_time:
            ready_queue.append(remaining.pop(0))
        
        while ready_queue or remaining:
            if not ready_queue:
                self.current_time = remaining[0].arrival_time
                ready_queue.append(remaining.pop(0))
            
            process = ready_queue.popleft()
            
            if process.start_time == -1:
                process.start_time = self.current_time
            
            execute_time = min(time_quantum, process.remaining_time)
            
            self.timeline.append({
                'pid': process.pid,
                'start': self.current_time,
                'end': self.current_time + execute_time
            })
            
            self.current_time += execute_time
            process.remaining_time -= execute_time
            
            while remaining and remaining[0].arrival_time <= self.current_time:
                ready_queue.append(remaining.pop(0))
            
            if process.remaining_time == 0:
                process.completion_time = self.current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
            else:
                ready_queue.append(process)
            
            if ready_queue or remaining:
                self.current_time += self.context_switch_time
        
        return self.calculate_metrics()