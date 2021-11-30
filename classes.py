class PCB:
    def __init__(self, name, priority, date_time, init_end_address, remaining_time):
        self.name = name.upper()
        self.pid = id(self)
        self.priority = priority
        self.date_time = date_time
        self.init_end_address = init_end_address
        self.remaining_time = remaining_time
        self.next = None
        
    def __repr__(self):
        return self.name + " | pid: " + str(self.pid) + " | priority: " + str(self.priority) + " | date_time: " + str(self.date_time) + " | init_end_address: " + str(self.init_end_address) + " | remaining_time: " + str(self.remaining_time) + "\n"

class Queue:
    def __init__(self, quantum):
        self.first = None
        self.last = None
        self.quantum = quantum

    def new_process(self, process):
        if self.first == None:
            self.first = self.last = process
            self.first.next = self.last.next = process
        else:
            self.last.next = process
            self.last = process
            self.last.next = self.first

    def end_process(self):
        aux = self.first
        self.first = self.first.next
        self.last.next = self.first
        del aux

    def queue_end(self):
        del self

class Scheduler:
    def __init__(self):
        self.ordered_queues = []
    
    def queue_exists_in_ordered_queues(self, priority):
        for queue in self.ordered_queues:
            if(queue.first.priority == priority):
                return self.ordered_queues.index(queue)
        return None

    def new_position_in_ordered_queues(self, priority):
        for queue in self.ordered_queues:
            if(queue.first.priority < priority):
                return self.ordered_queues.index(queue)
        return len(self.ordered_queues)

    def schedule_process(self, process):
        queue_position = self.queue_exists_in_ordered_queues(process.priority)
        if(queue_position is not None):
            self.ordered_queues[queue_position].new_process(process)
        else:
            new_queue = Queue(quantum = process.priority)
            new_queue.new_process(process)
            new_position = self.new_position_in_ordered_queues(process.priority)
            self.ordered_queues.insert(new_position, new_queue)

    def context_switch(self, queue, executing_process, time_unit):
        if executing_process.remaining_time:
            print("TIME {:02d} | Context Switch".format(time_unit))
            queue.first = queue.first.next
            queue.last = queue.last.next
        else:
            print("TIME {:02d} | Endend ".format(time_unit) + str(executing_process))
            aux = queue.first
            queue.first = queue.first.next
            queue.last.next = queue.first
            if queue.first == aux:
                del queue.first
                del aux
                return None
            del aux
        return queue.first

    def round_robin(self, time_unit):
        for queue in self.ordered_queues:
            executing_process = queue.first
            while executing_process is not None:
                time_executing = queue.quantum
                print("TIME {:02d} | Executing ".format(time_unit) + str(executing_process))
                while time_executing and executing_process.remaining_time:
                    executing_process.remaining_time -= 1
                    time_executing -= 1
                    time_unit += 1
                print("TIME {:02d} | Executing ".format(time_unit) + str(executing_process))
                
                executing_process = self.context_switch(queue, executing_process, time_unit) 

