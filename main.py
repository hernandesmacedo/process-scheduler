import random
from datetime import datetime, timedelta
from classes import PCB, Scheduler
import logging
logging.basicConfig(filename = 'output.log', level=logging.DEBUG, format='%(message)s')

def processes_creator(scheduler):
    
    end_address = 9999
    date_time = datetime.now().replace(microsecond=0)
    number_of_processes = 0

    while len(scheduler.ordered_queues) != 4 or number_of_processes < 18:
        name = 'Process {:02d}'.format(number_of_processes + 1)
        priority = random.randrange(1, 5)
        date_time += timedelta(minutes=1)
        init_address = end_address + 1
        end_address = init_address + random.randrange(0, 20)
        remaining_time = random.randrange(2, 18)
        process = PCB(name, priority, date_time, [init_address, end_address], remaining_time)
        scheduler.schedule_process(process)
        number_of_processes += 1

def main():
    scheduler = Scheduler()
    
    time_unit = 0
    
    processes_creator(scheduler)
    
    logging.info("SCHEDULER:")
    logging.info(scheduler)
    
    scheduler.round_robin(time_unit)
            
main() 
