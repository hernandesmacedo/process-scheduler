import logging
logging.basicConfig(filename = 'output.log', level=logging.DEBUG, format='%(message)s')

class PCB:
    """
    Process Control Block class used to create new processes objects.

    Defines a process containing:
        `name`: String as process name
        `pid`: Unique int as process ID
        `priority`: int as process priority
        `date_time`: datetime as process creation date and time
        `remaining_time`: int representing the time units for the process to be finished
        `next`: PCB process that comes after current PCB process in a queue
    """
    def __init__(self, name, priority, date_time, init_address, end_address, remaining_time):
        """Initiate a new PCB process with values provided from processes_creator function."""
        self.name = name
        self.pid = id(self)
        self.priority = priority
        self.date_time = date_time
        self.memory_address = [init_address, end_address]
        self.remaining_time = remaining_time
        self.next = None
        
    def __repr__(self):
        """Formats the way we want to see a process and its attributes."""
        return self.name + " | pid: " + str(self.pid) + " | priority: " + str(self.priority) + " | date_time: " + str(self.date_time) + " | memory_address: " + str(self.memory_address) + " | remaining_time: {:02d}".format(self.remaining_time)

class Queue:
    """
    Circular queue of processes with same priority.

    Creates a processes queue containing:
        `first`: Current first PCB process in queue
        `last`: Current last PCB process in queue (the one right before the first one)
        `length`: int as quantity of processes currently in queue
        `quantum`: int as the limit time units for a process in this Queue to use CPU
    """
    def __init__(self, quantum):
        """
        Initiate a new empty Queue with quantum value provided from Scheduler based
        on priority of processes that will be in this queue.
        """
        self.first = None
        self.last = None
        self.length = 0
        self.quantum = quantum

    def new_process(self, process):
        """
        Adds a new PCB process to a Queue.
        If a Queue is empty, it will be the first and last PCB process in it, pointing to itself as next,
        otherwise it will assume the last position and point to the first PCB process as its next.
        """
        if self.first == None:
            self.first = self.last = process
            self.first.next = self.last.next = process
        else:
            self.last.next = process
            self.last = process
            self.last.next = self.first
        self.length += 1

    def end_queue(self):
        """Frees Queue memory space when all PCB processes in it have been finished."""
        del self

class Scheduler:
    """
    Scheduler is responsible for sorting all Queues and processes in it.
    It uses priority rule to arrange the Queues and then, uses Round Robin to 
    organize how processes will use CPU.

    Creates an object containing:
        `sorted_queues`: A list with all Queues with different priorities. This list is sorted by priority,
        so in first list index will be the Queue of processes with highest priority,
        and in the last list index will be the Queue of processes with lowest priority.
    """
    def __init__(self):
        """Initiate a new empty Scheduler with no Queue."""
        self.sorted_queues = []
        
    def __repr__(self):
        """Formats the way we want to see a Scheduler and its Queues."""
        description = ""
        for queue in self.sorted_queues:
            priority_queue = queue.first.priority
            description += "QUEUE PRIORITY " + str(priority_queue) + " | " + str(queue.length) + " processes | quantum " + str(queue.quantum) + "\n"
            process = queue.first
            while True:
                description += str(process) + "\n"
                process = process.next
                if process == queue.first:
                    break
        return description
    
    def queue_exists_in_sorted_queues(self, priority):
        """
        Verifies if a Queue already exists in Scheduler by comparing priority value.

        Args:
            `self`: Scheduler
            `priority`: priority to be searched in the Scheduler Queues

        Returns:
            None if there is not a Queue of processes with this `priority` value in `Scheduler`,
            or returns the position of this Queue in the `Scheduler` sorted list of Queues.
        """
        for queue in self.sorted_queues:
            if(queue.first.priority == priority):
                return self.sorted_queues.index(queue)
        return None

    def new_position_in_sorted_queues(self, priority):
        """
        If there is not a Queue of processes with a `priority` value in `Scheduler`,
        this method verifies where a new processes Queue must be inserted in order to
        maintain the priority rule.

        Args:
            `self`: Scheduler
            `priority`: priority of the new Queue

        Returns:
            The position (index) where the new Queue must be inserted based in its `priority` value,
            in order to maintain the priority rule.
        """
        for queue in self.sorted_queues:
            if(queue.first.priority < priority):
                return self.sorted_queues.index(queue)
        return len(self.sorted_queues)

    def schedule_process(self, process):
        """
        Receives a new PCB process and verifies if there is a Queue with same priority in Scheduler.
        If not, creates a new Queue and insert it in a position based in process
        `priority` value, to maintain the priority rule.
        If already exists a Queue with same priority in Scheduler, then just adds it to the end of this Queue.

        Args:
            `self`: Scheduler
            `process`: PCB process object.
        """
        queue_position = self.queue_exists_in_sorted_queues(process.priority)
        if(queue_position is not None):
            self.sorted_queues[queue_position].new_process(process)
        else:
            new_queue = Queue(quantum = process.priority)
            new_queue.new_process(process)
            new_position = self.new_position_in_sorted_queues(process.priority)
            self.sorted_queues.insert(new_position, new_queue)

    def context_switch(self, queue, running_process, time_unit):
        """
        This method executes the Context Switch.
        If the running process still has remaining time to be finished, then points to the next
        process as the first in Queue, logs a message of Stopped process, Quantum endend and Context Switch event.
        If the running process does not have remaining time to be finished, this means it has already been finished,
        then points to the next process as the first in Queue, deletes the finished process memory space, decreases the
        Queue length by 1, and logs a message of Endend process, Quantum endend and Context Switch event.

        Args:
            `self`: Scheduler
            `queue`: current running priority Queue.
            `running_process`: current running PCB process.
            `time_unit`: the time unit that the context switch has happened.
            
        Returns:
            If next process is the same as a finished process itself, that means it was the last running 
            process, and the Queue finished all processes, returning None to indicate that there are no more
            processes to be runned in this Queue.
            Otherwise, returns the updated first process in `queue`, because Round Robin works in a circular Queue.
        """
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
            if queue.length == 0:
                logging.info("TIME {:03d} | QUEUE PRIORITY ".format(time_unit) + str(queue.first.priority) + " ENDED | CONTEXT SWITCH\n")
                del queue.first
                del aux
                queue.end_queue()
                return None
            del aux
        return queue.first

    def round_robin(self, time_unit):
        """
        This method simulates the Round Robin execution of processes.
        Because the processes Queue are executed respecting their priority values,
        a for loop is performed to iterate over the Queues in this `scheduler` list of Queues,
        that was sorted by priority values, so the Queue with highest priority will be executed first.
        For each Queue, the process to be executed will be the first in the Queue, and it can only use CPU
        during the `runtime` value that is a copy from queue's `quantum` value.
        For each time unit, the `runtime` for the process to use CPU decreases 1 unit, its `remaining_time`
        also decreases 1 unit and the `time_unit` of processing increases 1 unit to simulate the real life time.
        When the `runtime` is 0, that means the quantum of time for that process is finished, and a context switch
        must happen in diffent ways:
        - Gives the CPU to the next process in the same Queue, if there is another process;
        - The same process continues in CPU, if it is the last process in this Queue and still has remaining time;
        - Gives the CPU to the next highest priority Queue, if this process was the last process
        in this Queue and it has no remaining time (has finished);
        - Ends Round Robin scheduling, if this process has no remaning time and it is already in the lowest priority Queue (the last one).
        
        Args:
            `self`: Scheduler
            `time_unit`: the time unit that the Round Robin is happening.
        """
        logging.info("ROUND ROBIN EXECUTION:")
        for queue in self.sorted_queues:
            running_process = queue.first
            while running_process is not None:
                runtime = queue.quantum
                logging.info("TIME {:03d} | Executing ".format(time_unit) + str(running_process))
                while runtime and running_process.remaining_time:
                    running_process.remaining_time -= 1
                    runtime -= 1
                    time_unit += 1
                running_process = self.context_switch(queue, running_process, time_unit)
