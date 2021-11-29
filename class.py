class PCB:
    def __init__(self, name, pid, priority, date_time, init_end_address, remaining_time, next):
        self.name = name
        self.pid = pid
        self.priority = priority
        self.date_time = date_time
        self.init_end_address = init_end_address
        self.remaining_time = remaining_time
        self.next = next

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
