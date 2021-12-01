import logging
logging.basicConfig(filename = 'output.log', level=logging.DEBUG, format='%(message)s')

class PCB:
    def __init__(self, name, priority, date_time, memory_address, remaining_time):
        self.name = name.upper()
        self.pid = id(self)
        self.priority = priority
        self.date_time = date_time
        self.memory_address = memory_address
        self.remaining_time = remaining_time
        self.next = None
        
    def __repr__(self):
        return self.name + " | pid: " + str(self.pid) + " | priority: " + str(self.priority) + " | date_time: " + str(self.date_time) + " | memory_address: " + str(self.memory_address) + " | remaining_time: {:02d}".format(self.remaining_time)

class Queue:
    def __init__(self, quantum):
        self.first = None
        self.last = None
        self.length = 0
        self.quantum = quantum

    def new_process(self, process):
        if self.first == None:
            self.first = self.last = process
            self.first.next = self.last.next = process
        else:
            self.last.next = process
            self.last = process
            self.last.next = self.first
        self.length += 1

    def end_queue(self):
        del self

class Scheduler:
    def __init__(self):
        self.ordered_queues = []
        
    def __repr__(self):
        description = ""
        for queue in self.ordered_queues:
            priority_queue = queue.first.priority
            description += "QUEUE PRIORITY " + str(priority_queue) + " | " + str(queue.length) + " processes | quantum " + str(queue.quantum) + "\n"
            process = queue.first
            while True:
                description += str(process) + "\n"
                process = process.next
                if process == queue.first:
                    break
        return description
    
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

    def context_switch(self, queue, running_process, time_unit):
        if running_process.remaining_time:
            queue.first = queue.first.next
            queue.last = queue.last.next
            logging.info("TIME {:03d} | Stopped   ".format(time_unit) + str(running_process))
            if queue.length > 1:
                logging.info("TIME {:03d} | QUANTUM ENDED | CONTEXT SWITCH".format(time_unit))
            else:
                logging.info("TIME {:03d} | QUANTUM ENDED".format(time_unit))
        else:
            logging.info("TIME {:03d} | Endend    ".format(time_unit) + str(running_process))
            if queue.length > 1:
                logging.info("TIME {:03d} | QUANTUM ENDED | CONTEXT SWITCH".format(time_unit))
            else:
                logging.info("TIME {:03d} | QUANTUM ENDED".format(time_unit))
            aux = queue.first
            queue.first = queue.first.next
            queue.last.next = queue.first
            queue.length -= 1
            if queue.first == aux:
                logging.info("TIME {:03d} | QUEUE PRIORITY ".format(time_unit) + str(queue.first.priority) + " ENDED | CONTEXT SWITCH")
                del queue.first
                del aux
                return None
            del aux
        return queue.first

    def round_robin(self, time_unit):
        logging.info("ROUND ROBIN EXECUTION:")
        for queue in self.ordered_queues:
            running_process = queue.first
            while running_process is not None:
                time_executing = queue.quantum
                logging.info("TIME {:03d} | Executing ".format(time_unit) + str(running_process))
                while time_executing and running_process.remaining_time:
                    running_process.remaining_time -= 1
                    time_executing -= 1
                    time_unit += 1
                
                running_process = self.context_switch(queue, running_process, time_unit) 
                
            queue.end_queue()
