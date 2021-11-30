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
    def __init__(self):
        self.first = None

    def context_switch(self, quantum):
        self.first.remaining_time -= quantum
        self.first = self.first.next

    def process_end(self):
        aux = self.first
        self.first = self.first.next
        del aux

    def queue_end(self):
        del self
