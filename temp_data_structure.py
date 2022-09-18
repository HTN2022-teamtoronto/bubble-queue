from datetime import datetime

db_as_dictionary = {}

BUBBLE_WAIT_TIME = 300
BUBBLE_WAIT_NUMBER = 5

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


# Call when a user enters an event and selects a queue
# Pass in event_id and queue_name
def enqueue(event_id, queue_name):
    list_of_queue_objs = db_as_dictionary[event_id]
    the_queue_object = None
    for a_queue_obj in list_of_queue_objs:
        if a_queue_obj.name == queue_name:
            the_queue_object = a_queue_obj
    if the_queue_object:
        return the_queue_object.add_a_ticket()


def get_queue_state(event_id, queue_name):
    list_of_queue_objs = db_as_dictionary[event_id]
    the_queue_object = None
    for a_queue_obj in list_of_queue_objs:
        if a_queue_obj.name == queue_name:
            the_queue_object = a_queue_obj
    if the_queue_object:
        if len(the_queue_object.tickets_to_call) != 0:
            out_current = the_queue_object.tickets_to_call[0]
        else:
            print("No one in queue")
            return

        out_bubble = []
        out_not_bubble = []

        if the_queue_object.tickets_elapsed > 3:
            avg_time_per_ticket = time_elapsed / tickets_elapsed
            n_tickets_in_bubble = BUBBLE_WAIT_TIME / avg_time_per_ticket
            
            loop = min(len(the_queue_object.tickets_to_call), n_tickets_in_bubble)

            for i in range(1, loop):
                out_bubble.append(the_queue_object.tickets_to_call[i])

            if loop < len(the_queue_object.tickets_to_call):
                for i in range (loop, len(the_queue_object.tickets_to_call))
                out_not_bubble.append(the_queue_object.tickets_to_call[i])

        else:
            loop = min(len(the_queue_object.tickets_to_call), BUBBLE_WAIT_NUMBER)
            for i in range(1, loop):
                out_bubble.append(the_queue_object.tickets_to_call[i])
                
            if loop < len(the_queue_object.tickets_to_call):
                for i in range (loop, len(the_queue_object.tickets_to_call))
                out_not_bubble.append(the_queue_object.tickets_to_call[i])



def 


line1 = Queue("Hack the North Event", "Host David", 5)
line1.add_a_ticket()
for i in range(9000):
    print(i)
line1.call_a_ticket()
asdf= {"asdff":12}
print(asdf["asdff"])