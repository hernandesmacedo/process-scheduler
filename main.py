import random
from datetime import datetime, timedelta
from classes import PCB, Queue

def processes_creator(top_priority_queue, second_priority_queue, third_priority_queue, last_priority_queue):
    end_address = 9999
    date_time = datetime.now()

    for i in range(1, 7):
        name = 'Processo ' + str(i)
        priority = 4
        date_time = date_time + timedelta(minutes=1)
        init_address = end_address + 1
        end_address = init_address + random.randrange(0, 20)
        remaining_time = random.randrange(1, 12)
        process = PCB(name, priority, date_time, [init_address, end_address], remaining_time)
        top_priority_queue.new_process(process)

    for i in range(7, 12):
        name = 'Processo ' + str(i)
        priority = 3
        date_time = date_time + timedelta(minutes=1)
        init_address = end_address + 1
        end_address = init_address + random.randrange(0, 20)
        remaining_time = random.randrange(1, 12)
        process = PCB(name, priority, date_time, [init_address, end_address], remaining_time)
        second_priority_queue.new_process(process)

    for i in range(12, 16):
        name = 'Processo ' + str(i)
        priority = 2
        date_time = date_time + timedelta(minutes=1)
        init_address = end_address + 1
        end_address = init_address + random.randrange(0, 20)
        remaining_time = random.randrange(1, 12)
        process = PCB(name, priority, date_time, [init_address, end_address], remaining_time)
        third_priority_queue.new_process(process)

    for i in range(16, 20):
        name = 'Processo ' + str(i)
        priority = 1
        date_time = date_time + timedelta(minutes=1)
        init_address = end_address + 1
        end_address = init_address + random.randrange(0, 20)
        remaining_time = random.randrange(1, 12)
        process = PCB(name, priority, date_time, [init_address, end_address], remaining_time)
        last_priority_queue.new_process(process)

def main():
    top_priority_queue = Queue(quantum = 4)
    second_priority_queue = Queue(quantum = 3)
    third_priority_queue = Queue(quantum = 2)
    last_priority_queue = Queue(quantum = 2)

    processes_creator(top_priority_queue, second_priority_queue, third_priority_queue, last_priority_queue)

main() 
