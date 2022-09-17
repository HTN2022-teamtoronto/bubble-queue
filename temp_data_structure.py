from datetime import datetime

db_as_dictionary = {}

class Queue:

    def __init__(self, name, host_in_charge, waiting_bubble_size):

        self.name = name
        self.host_in_charge = host_in_charge
        self.waiting_bubble_size = waiting_bubble_size
        self.tickets_to_call = []

        self.time_when_last_ticket_called = 0
        self.time_when_current_ticket_called = 0

        self.time_elapsed = 0
        self.tickets_elapsed = 0

    def call_a_ticket(self):
        if len(self.tickets_to_call) != 0:
            self.tickets_elapsed += 1
            self.time_when_current_ticket_called = datetime.now()
            diff_time = (self.time_when_current_ticket_called - self.time_when_last_ticket_called)
            self.time_elapsed = diff_time.total_seconds()
            return self.tickets_to_call.pop(0)
        else:
            print("No more tickets to call")
            return

    def call_a_specific_ticket(self, ticket):
        if ticket in self.tickets_to_call:
            self.tickets_elapsed += 1
            self.tickets_to_call.remove(ticket)
            return ticket
        else:
            print("Ticket not in list")
            return

    def add_a_ticket(self):
        if len(self.tickets_to_call) != 0:
            largest_ticket = self.tickets_to_call[-1]
            next_ticket = largest_ticket + 1
            self.tickets_to_call.append(next_ticket)
        else:
            next_ticket = 1
            self.tickets_to_call = [next_ticket]
            self.time_when_last_ticket_called = datetime.now()

        return next_ticket


## Methods for Accessing Database
def createEvent(event_id, list_of_queue_objs):
    if event_id in db_as_dictionary:
        print("Event ID is used")
        return
    else:
        db_as_dictionary[event_id] = list_of_queue_objs


line1 = Queue("Hack the North Event", "Host David", 5)
line1.add_a_ticket()
for i in range(9000):
    print(i)
line1.call_a_ticket()