from datetime import datetime
from random import random

db_as_dictionary = {}

BUBBLE_WAIT_TIME = 300

class Queue:

    def __init__(self, name, waiting_bubble_size):

        self.name = name
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
            self.time_when_last_ticket_called = self.time_when_current_ticket_called
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
        return event_id


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

        out_current = None
        out_bubble = []
        out_not_bubble = []
        out_time_elasped = the_queue_object.time_elapsed
        out_ticket_elapsed = the_queue_object.tickets_elapsed

        if len(the_queue_object.tickets_to_call) != 0:
            out_current = the_queue_object.tickets_to_call[0]
        else:
            print("No one in queue")

        

        if the_queue_object.tickets_elapsed > 3:

            avg_time_per_ticket = (the_queue_object.time_elapsed / the_queue_object.tickets_elapsed) if the_queue_object.time_elapsed != 0 else 999
          
            n_tickets_in_bubble = BUBBLE_WAIT_TIME // avg_time_per_ticket

            if n_tickets_in_bubble != 0:
                loop = min(len(the_queue_object.tickets_to_call), n_tickets_in_bubble)
                for i in range(1, loop):
                    out_bubble.append(the_queue_object.tickets_to_call[i])
                if loop < len(the_queue_object.tickets_to_call):
                   
                    for i in range (loop, len(the_queue_object.tickets_to_call)):

                        out_not_bubble.append(the_queue_object.tickets_to_call[i])

                return out_current, out_bubble, out_not_bubble, out_time_elasped, out_ticket_elapsed

        
        loop = min(len(the_queue_object.tickets_to_call), the_queue_object.waiting_bubble_size)
        for i in range(1, loop):
            out_bubble.append(the_queue_object.tickets_to_call[i])
            
        if loop < len(the_queue_object.tickets_to_call):
            for i in range (loop, len(the_queue_object.tickets_to_call)):
                out_not_bubble.append(the_queue_object.tickets_to_call[i])
        return out_current, out_bubble, out_not_bubble, out_time_elasped, out_ticket_elapsed


def get_random_event_id():
    return int(random()*10**6)

def get_all_queues_in_event(event_id):
    if event_id in db_as_dictionary:
        return db_as_dictionary[event_id]
    else:
        print("No such event_id")
        return

def get_brief_info_of_queues(queue_obj):
    return queue_obj.name, queue_obj.tickets_to_call[0], len(queue_obj.tickets_to_call) * time_elapsed / tickets_elapsed



# -------------------------------------------------------------------------------------------
# Organizers
# Input from front end: {Name1: waiting_bubble_size1, Name2: waiting_bubble_size2, etc.}
# Action              : create new event, i.e., a new key-value pair in the dictionary) 
# Output to front end : the event_id, i.e., a six digit number

sample_input = {"Line for Beef": 5, "Line for Beyond Meat": 7}
converted_input = list(sample_input.items())
queue_objs = []
for i in converted_input:
    queue_objs.append(Queue(i[0], i[1]))
newEvent1_id = createEvent(get_random_event_id(), queue_objs)

print("New event created:", newEvent1_id)
print("The db is now:", db_as_dictionary)
sample_output1 = {"event_id": newEvent1_id}
print()




sample_input = {"Line for Apple Juice": 4, "Line for Orange Juice": 2}
converted_input = list(sample_input.items())
queue_objs = []
for i in converted_input:
    queue_objs.append(Queue(i[0], i[1]))
newEvent2_id = createEvent(get_random_event_id(), queue_objs)
print("New event created:", newEvent2_id)
print("The db is now:", db_as_dictionary)
sample_output2 = {"event_id": newEvent2_id}
print()
# -------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------
# Attendees
# Input from front end: **first** {event_id: event_id} **then** {queue_name: queue_name}
# Action              : add_a_ticket
# Output to front end : out_current, out_bubble, out_not_bubble, out_time_elasped, out_ticket_elapsed
# -------------------------------------------------------------------------------------------
sample_input = {"event_id": newEvent2_id}
print("Querying for event_id:", sample_input["event_id"])
queues = get_all_queues_in_event(sample_input["event_id"])
print("Found:", queues)
sample_input2 = {"queue_name": "Line for Apple Juice"}
print("Add a ticket...")
for i in range(len(queues)):
    if queues[i].name == sample_input2["queue_name"]:
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        queues[i].add_a_ticket()
        print("Added a ticket, status:", get_queue_state(sample_input["event_id"], sample_input2["queue_name"]))
        queues[i].call_a_ticket()
        queues[i].call_a_ticket()
        queues[i].call_a_ticket()
        queues[i].call_a_ticket()
        queues[i].call_a_ticket()
        


        print("Added a ticket, status:", get_queue_state(sample_input["event_id"], sample_input2["queue_name"]))

print(db_as_dictionary[newEvent2_id][0].tickets_to_call)



def hash(six_digit_int):
    return int(str(six_digit_int)[::-1])

# -------------------------------------------------------------------------------------------
# Queue Receptionists
# Input from front end: **first** {event_id: event_id} **then** {queue_name: queue_name}
# Action              : show queue state
# Output to front end : out_current, out_bubble, out_not_bubble, out_time_elasped, out_ticket_elapsed

sample_input = {"event_id": hash(newEvent2_id)}
print("Querying for event_id:", hash(sample_input["event_id"]))
sample_output = get_all_queues_in_event(hash(sample_input["event_id"]))
print("Found:", sample_output)

sample_input2 = {"queue_name": "Line for Apple Juice"}

print(get_queue_state(hash(sample_input["event_id"]), sample_input2["queue_name"]))
# -------------------------------------------------------------------------------------------


