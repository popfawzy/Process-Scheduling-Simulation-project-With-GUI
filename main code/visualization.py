
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_gantt_chart(scheduler, title, avg_turnaround, avg_waiting, parent=None):

    if not scheduler.timeline:
        print("No timeline to display!")
        return None
    
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.4, wspace=0.3)
    
    ax_gantt = fig.add_subplot(gs[0, :])
    colors = plt.cm.Set3(range(len(scheduler.processes)))
    color_map = {p.pid: colors[i] for i, p in enumerate(scheduler.processes)}
    
    for slot in scheduler.timeline:
        duration = slot['end'] - slot['start']
        ax_gantt.barh(0, duration, left=slot['start'], height=0.5,
                     color=color_map[slot['pid']], edgecolor='black', linewidth=2)
        ax_gantt.text(slot['start'] + duration/2, 0, f"P{slot['pid']}",
                     ha='center', va='center', fontweight='bold', fontsize=11)
    
    ax_gantt.set_ylim(-0.5, 0.5)
    ax_gantt.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax_gantt.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax_gantt.set_yticks([])
    ax_gantt.grid(True, axis='x', alpha=0.3)
    
    max_time = max(slot['end'] for slot in scheduler.timeline)
    ax_gantt.set_xlim(0, max_time + 1)
    
    ax_table = fig.add_subplot(gs[1, :])
    ax_table.axis('tight')
    ax_table.axis('off')
    
    table_data = [['Process', 'Arrival', 'Burst', 'Priority', 'Completion', 'Turnaround', 'Waiting']]
    for p in sorted(scheduler.processes, key=lambda x: x.pid):
        table_data.append([
            f'P{p.pid}', str(p.arrival_time), str(p.burst_time), str(p.priority),
            str(p.completion_time), str(p.turnaround_time), str(p.waiting_time)
        ])
    
    table = ax_table.table(cellText=table_data, cellLoc='center', loc='center', colWidths=[0.12] * 7)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)
    
    for i in range(7):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(1, len(table_data)):
        for j in range(7):
            table[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else '#ffffff')
    
    ax_table.set_title('Process Metrics', fontsize=13, fontweight='bold', pad=15, x=0.56, y=1.1)
    
    ax_avg1 = fig.add_subplot(gs[2, 0])
    ax_avg2 = fig.add_subplot(gs[2, 1])
    
    processes_sorted = sorted(scheduler.processes, key=lambda x: x.pid)
    pids = [f'P{p.pid}' for p in processes_sorted]
    turnaround_times = [p.turnaround_time for p in processes_sorted]
    waiting_times = [p.waiting_time for p in processes_sorted]
    
    bars1 = ax_avg1.bar(pids, turnaround_times, color='skyblue', edgecolor='black', linewidth=1.5)
    ax_avg1.axhline(y=avg_turnaround, color='red', linestyle='--', linewidth=2,
                    label=f'Average: {avg_turnaround:.2f}')
    ax_avg1.set_ylabel('Time Units', fontsize=11, fontweight='bold')
    ax_avg1.set_xlabel('Process', fontsize=11, fontweight='bold')
    ax_avg1.set_title('Turnaround Time', fontsize=12, fontweight='bold')
    ax_avg1.legend()
    ax_avg1.grid(True, alpha=0.3, axis='y')
    
    for bar in bars1:
        height = bar.get_height()
        ax_avg1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    bars2 = ax_avg2.bar(pids, waiting_times, color='lightcoral', edgecolor='black', linewidth=1.5)
    ax_avg2.axhline(y=avg_waiting, color='red', linestyle='--', linewidth=2,
                    label=f'Average: {avg_waiting:.2f}')
    ax_avg2.set_ylabel('Time Units', fontsize=11, fontweight='bold')
    ax_avg2.set_xlabel('Process', fontsize=11, fontweight='bold')
    ax_avg2.set_title('Waiting Time', fontsize=12, fontweight='bold')
    ax_avg2.legend()
    ax_avg2.grid(True, alpha=0.3, axis='y')
    
    for bar in bars2:
        height = bar.get_height()
        ax_avg2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if parent:
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas.get_tk_widget()
    else:
        plt.show()
        return None


def create_comparison_chart(results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    algorithms = list(results.keys())
    tat_values = [results[algo]['TAT'] for algo in algorithms]
    wt_values = [results[algo]['WT'] for algo in algorithms]
    
    bars1 = ax1.bar(algorithms, tat_values, color='skyblue', edgecolor='black', linewidth=2)
    ax1.set_ylabel('Time Units', fontsize=12, fontweight='bold')
    ax1.set_title('Average Turnaround Time Comparison', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
    
    bars2 = ax2.bar(algorithms, wt_values, color='lightcoral', edgecolor='black', linewidth=2)
    ax2.set_ylabel('Time Units', fontsize=12, fontweight='bold')
    ax2.set_title('Average Waiting Time Comparison', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.show()