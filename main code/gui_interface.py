

import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
from algorithms import CPUScheduler
from visualization import draw_gantt_chart, create_comparison_chart

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2C3E50')
        
        self.processes = []
        self.setup_ui()
    
    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg='#34495E', height=60)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(title_frame, text="🖥️ CPU Scheduling Simulator",
                              font=('Arial', 24, 'bold'), fg='white', bg='#34495E')
        title_label.pack(pady=10)
        
        main_container = tk.Frame(self.root, bg='#2C3E50')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(main_container, bg='#34495E', width=400)
        left_panel.pack(side='left', fill='both', padx=5, pady=5)
        
        self.setup_input_panel(left_panel)
        
        right_panel = tk.Frame(main_container, bg='#34495E')
        right_panel.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.setup_process_list(right_panel)
        self.setup_algorithm_panel(right_panel)
    
    def setup_input_panel(self, parent):
        input_label = tk.Label(parent, text="Add Process", font=('Arial', 16, 'bold'),
                              fg='white', bg='#34495E')
        input_label.pack(pady=10)
        
        fields_frame = tk.Frame(parent, bg='#34495E')
        fields_frame.pack(pady=10, padx=20)
        
        tk.Label(fields_frame, text="Process ID:", font=('Arial', 11),
                fg='white', bg='#34495E').grid(row=0, column=0, sticky='w', pady=5)
        self.pid_entry = tk.Entry(fields_frame, font=('Arial', 11), width=15)
        self.pid_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(fields_frame, text="Arrival Time:", font=('Arial', 11),
                fg='white', bg='#34495E').grid(row=1, column=0, sticky='w', pady=5)
        self.arrival_entry = tk.Entry(fields_frame, font=('Arial', 11), width=15)
        self.arrival_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(fields_frame, text="Burst Time:", font=('Arial', 11),
                fg='white', bg='#34495E').grid(row=2, column=0, sticky='w', pady=5)
        self.burst_entry = tk.Entry(fields_frame, font=('Arial', 11), width=15)
        self.burst_entry.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(fields_frame, text="Priority:", font=('Arial', 11),
                fg='white', bg='#34495E').grid(row=3, column=0, sticky='w', pady=5)
        self.priority_entry = tk.Entry(fields_frame, font=('Arial', 11), width=15)
        self.priority_entry.grid(row=3, column=1, pady=5, padx=10)
        
        button_frame = tk.Frame(parent, bg='#34495E')
        button_frame.pack(pady=20)
        
        add_btn = tk.Button(button_frame, text="➕ Add Process", font=('Arial', 11, 'bold'),
                           bg='#27AE60', fg='white', width=15, command=self.add_process)
        add_btn.pack(pady=5)
        
        clear_btn = tk.Button(button_frame, text="🗑️ Clear All", font=('Arial', 11, 'bold'),
                             bg='#E74C3C', fg='white', width=15, command=self.clear_processes)
        clear_btn.pack(pady=5)
        
        sample_btn = tk.Button(button_frame, text="📋 Load Sample", font=('Arial', 11, 'bold'),
                              bg='#3498DB', fg='white', width=15, command=self.load_sample)
        sample_btn.pack(pady=5)

        run_frame = tk.Frame(parent, bg='#34495E')
        run_frame.pack(side='bottom', fill='x', pady=10)

        run_btn_large = tk.Button(run_frame, text="▶ Run Selected", font=('Arial', 14, 'bold'),
                      bg='#16A085', fg='white', width=22, height=3, command=self.run_algorithms)
        run_btn_large.pack(pady=8)

        compare_btn_large = tk.Button(run_frame, text="≡ Compare All", font=('Arial', 14, 'bold'),
                          bg='#8E44AD', fg='white', width=22, height=3, command=self.compare_all)
        compare_btn_large.pack(pady=8)
    
    def setup_process_list(self, parent):
        list_label = tk.Label(parent, text="Process List", font=('Arial', 14, 'bold'),
                             fg='white', bg='#34495E')
        list_label.pack(pady=10)
        
        tree_frame = tk.Frame(parent, bg='#34495E')
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('PID', 'Arrival', 'Burst', 'Priority')
        self.process_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        self.process_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        delete_btn = tk.Button(parent, text="❌ Delete Selected", font=('Arial', 10, 'bold'),
                              bg='#E67E22', fg='white', command=self.delete_process)
        delete_btn.pack(pady=5)
    
    def setup_algorithm_panel(self, parent):
        algo_label = tk.Label(parent, text="Select Algorithm", font=('Arial', 14, 'bold'),
                             fg='white', bg='#34495E')
        algo_label.pack(pady=10)
        
        # Algorithm selection
        algo_frame = tk.Frame(parent, bg='#34495E')
        algo_frame.pack(pady=10)
        
        self.selected_algos = {
            'FCFS': tk.BooleanVar(value=False),
            'SJF (Non-Preemptive)': tk.BooleanVar(value=False),
            'SJF (Preemptive)': tk.BooleanVar(value=False),
            'Priority': tk.BooleanVar(value=False),
            'Round Robin': tk.BooleanVar(value=False)
        }
        
        for algo, var in self.selected_algos.items():
            cb = tk.Checkbutton(algo_frame, text=algo, variable=var,
                               font=('Arial', 11), fg='white', bg='#34495E',
                               selectcolor='#2C3E50', activebackground='#34495E')
            cb.pack(anchor='w', pady=2)
        
        quantum_frame = tk.Frame(parent, bg='#34495E')
        quantum_frame.pack(pady=10)
        
        tk.Label(quantum_frame, text="Time Quantum (RR):", font=('Arial', 11),
                fg='white', bg='#34495E').pack(side='left', padx=5)
        self.quantum_entry = tk.Entry(quantum_frame, font=('Arial', 11), width=10)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side='left', padx=5)
        
        run_frame = tk.Frame(parent, bg='#34495E')
        run_frame.pack(side='bottom', fill='x', pady=10)
        
        run_btn = tk.Button(run_frame, text=" Run Selected", font=('Arial', 12, 'bold'),
                   bg='#16A085', fg='white', width=20, height=2, command=self.run_algorithms)
        run_btn.pack(pady=5)
        
        compare_btn = tk.Button(run_frame, text=" Compare All", font=('Arial', 12, 'bold'),
                       bg='#8E44AD', fg='white', width=20, height=2, command=self.compare_all)
        compare_btn.pack(side='bottom', fill='x', pady=50)
    
    def add_process(self):
        try:
            pid = int(self.pid_entry.get())
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get())
            
            if burst <= 0:
                raise ValueError("Burst time must be positive")
            
            process = Process(pid, arrival, burst, priority)
            self.processes.append(process)
            
            self.process_tree.insert('', 'end', values=(pid, arrival, burst, priority))
            
            self.pid_entry.delete(0, 'end')
            self.arrival_entry.delete(0, 'end')
            self.burst_entry.delete(0, 'end')
            self.priority_entry.delete(0, 'end')
            
            messagebox.showinfo("Success", f"Process P{pid} added successfully!")
        
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def delete_process(self):
        selected = self.process_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a process to delete")
            return
        
        for item in selected:
            values = self.process_tree.item(item, 'values')
            pid = int(values[0])
            self.processes = [p for p in self.processes if p.pid != pid]
            self.process_tree.delete(item)
        
        messagebox.showinfo("Success", "Process(es) deleted successfully!")
    
    def clear_processes(self):
        if messagebox.askyesno("Confirm", "Clear all processes?"):
            self.processes = []
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)
    
    def load_sample(self):
        self.clear_processes()
        
        sample_processes = [
            Process(1, 0, 5, 2),
            Process(2, 1, 3, 1),
            Process(3, 2, 8, 3),
            Process(4, 3, 6, 2)
        ]
        
        for p in sample_processes:
            self.processes.append(p)
            self.process_tree.insert('', 'end', values=(p.pid, p.arrival_time, p.burst_time, p.priority))
        
        messagebox.showinfo("Success", "Sample processes loaded!")
    
    def run_algorithms(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add processes first!")
            return
        
        selected = [algo for algo, var in self.selected_algos.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one algorithm!")
            return
        
        try:
            quantum = int(self.quantum_entry.get())
        except ValueError:
            quantum = 2
        
        for algo in selected:
            scheduler = CPUScheduler([Process(p.pid, p.arrival_time, p.burst_time, p.priority) 
                                     for p in self.processes])
            
            if algo == 'FCFS':
                avg_tat, avg_wt = scheduler.fcfs()
                draw_gantt_chart(scheduler, "FCFS - First Come First Serve", avg_tat, avg_wt)
            
            elif algo == 'SJF (Non-Preemptive)':
                avg_tat, avg_wt = scheduler.sjf_non_preemptive()
                draw_gantt_chart(scheduler, "SJF (Non-Preemptive)", avg_tat, avg_wt)
            
            elif algo == 'SJF (Preemptive)':
                avg_tat, avg_wt = scheduler.sjf_preemptive()
                draw_gantt_chart(scheduler, "SJF (Preemptive) - SRTF", avg_tat, avg_wt)
            
            elif algo == 'Priority':
                avg_tat, avg_wt = scheduler.priority_scheduling()
                draw_gantt_chart(scheduler, "Priority Scheduling", avg_tat, avg_wt)
            
            elif algo == 'Round Robin':
                avg_tat, avg_wt = scheduler.round_robin(quantum)
                draw_gantt_chart(scheduler, f"Round Robin (Quantum={quantum})", avg_tat, avg_wt)
    
    def compare_all(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add processes first!")
            return
        
        try:
            quantum = int(self.quantum_entry.get())
        except ValueError:
            quantum = 2
        
        results = {}
        
        algorithms = {
            'FCFS': lambda s: s.fcfs(),
            'SJF (NP)': lambda s: s.sjf_non_preemptive(),
            'SJF (P)': lambda s: s.sjf_preemptive(),
            'Priority': lambda s: s.priority_scheduling(),
            'Round Robin': lambda s: s.round_robin(quantum)
        }
        
        for name, func in algorithms.items():
            scheduler = CPUScheduler([Process(p.pid, p.arrival_time, p.burst_time, p.priority) 
                                     for p in self.processes])
            avg_tat, avg_wt = func(scheduler)
            results[name] = {'TAT': avg_tat, 'WT': avg_wt}
            
            title_map = {
                'FCFS': 'FCFS - First Come First Serve',
                'SJF (NP)': 'SJF (Non-Preemptive)',
                'SJF (P)': 'SJF (Preemptive) - SRTF',
                'Priority': 'Priority Scheduling',
                'Round Robin': f'Round Robin (Quantum={quantum})'
            }
            draw_gantt_chart(scheduler, title_map[name], avg_tat, avg_wt)
        
        create_comparison_chart(results)
        
        print("\n" + "="*80)
        print("ALGORITHM COMPARISON SUMMARY")
        print("="*80)
        print(f"{'Algorithm':<20} {'Avg TAT':>12} {'Avg WT':>12}")
        print("-"*80)
        for algo, metrics in results.items():
            print(f"{algo:<20} {metrics['TAT']:>12.2f} {metrics['WT']:>12.2f}")