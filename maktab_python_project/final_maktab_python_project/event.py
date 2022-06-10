import logging
import pandas as pd
import file_handeling

my_discount_codes = {"student_@_iran": 0.2, "disabled_person_ABC": 0.5, "spacial_office_$so": 0.3}
class Event:



    def __init__(self, name, event_datetime, place, capacity, remain_capacity, ticket_cost, discount_percent=0):
        self.name = name
        self.event_datetime = event_datetime
        self.place = place
        self.capacity = capacity
        self.remain_capacity = remain_capacity
        self.ticket_cost = ticket_cost
        self.discount_percent = discount_percent

        self.event_id = getting_event_id()

    def cal_discount(self):
        """"Apply a discount on the price this method is for admin when want to define new event with discount code"""
        self.discount_percent = float(int(self.discount_percent) / 100)
        new_cost = float(self.ticket_cost) - (float(self.ticket_cost) * float(self.discount_percent))
        self.ticket_cost = new_cost
        return self.ticket_cost

    def __repr__(self):
        return (
            f" event name:{self.name} ,date:{self.event_datetime}, place:{self.place}, capacity:{self.capacity}, "
            f"remain capacity:{self.remain_capacity}"
            f",ticket cost:{self.ticket_cost}, discount:{self.discount_percent},event id{self.event_id}")

    def __str__(self):
        return (
            f" event name:{self.name} ,date:{self.event_datetime}, place:{self.place}, capacity:{self.capacity}, "
            f"remain capacity:{self.remain_capacity}"
            f",ticket cost:{self.ticket_cost}, discount:{self.discount_percent},event id{self.event_id}")


event_file = file_handeling.File("event_info.csv")




def define_event():
    """this function is for take value from admin when define a new event"""
    name, event_datetime, place, capacity, remain_capacity, ticket_cost, discount_percent = input(" enter name,"
                                                                                                  "event_datetime, "
                                                                                                  "place, capacity, "
                                                                                                  "remain_capacity,"
                                                                                                  " ticket_cost,"
                                                                                                  " discount_percent:") \
        .split(',')

    event = Event(name, event_datetime, place, capacity, remain_capacity, ticket_cost, discount_percent)
    logging.basicConfig(filename='record.log', level=logging.INFO, filemode='a',
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("register new event by admin")
    event.cal_discount()
    event_file.write(event.__dict__)# now by __dict__ make dictionary from new instance and write it in file
    return event


# for sale a event should use this function

def ticket_sale(number_of_ticket, e_id):
    """ some time when define a new event by admin ,may be  admin insert discount and some time may user have code
     in this part first calculator final cost of ticket  when user insert another discount  """
    all_events = event_file.read_csvfile_as_dictionary()

    for i in range(len(all_events)):


        if int(all_events[i]['event_id']) == e_id:

            all_events[i]['ticket_cost']=float(all_events[i]['ticket_cost'])
            check = int(input("enter 1 if you have discount code  otherwise enter 0 : "))
            try:
                while True:
                    if check == 1:
                        user_code = input("please inter your discount code if you have?")
                        for key in my_discount_codes:
                            if user_code == key:
                                discount_percent = my_discount_codes[key]
                                print(f" discount for this code is :{discount_percent}")
                                new_price = int(all_events[i]['ticket_cost']) - (int(all_events[i]['ticket_cost']) * discount_percent)
                                all_events[i]['ticket_cost'] = new_price

                                break
                        break
                    elif check == 0:

                        break
                    elif check != 1 and check != 0:
                        print("just 0 and 1 is valid numbers!!!!")
                        check = int(input("enter 1 if you have discount code  otherwise enter 0 : "))

            except ValueError as v:
                print(v)

            if int(all_events[i]['remain_capacity']) >= int(number_of_ticket):
                # after check remain capacity customer can keep shopping a otherwise break from function

                total_cost = int(number_of_ticket) * int(all_events[i]['ticket_cost'])
                agreement = int(input(f"the total cost is {total_cost}  1) agree and buy 2)cancel :"))
                try:
                    if agreement == 1:
                        print("Thank you  for buying and  have a good time")
                        remain_capacity = int(all_events[i]['remain_capacity']) - int(number_of_ticket)
                        # for update remain capacity in file
                        df = pd.read_csv("event_info.csv")
                        df.head(8)  # prints 8 heading rows
                        df.loc[df["event_id"] == e_id, "remain_capacity"] = remain_capacity
                        df.to_csv("event_info.csv", index=False)

                        logging.basicConfig(filename='record.log', level=logging.INFO, filemode='a',
                                            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
                                            )
                        logging.info(f"bought {number_of_ticket} ticket from event_id:{e_id} "
                                     f"now the remain capacity for this event is :{remain_capacity} ")
                    elif agreement == 2:
                        print("you canceled your tickets !!!")


                except ValueError:
                    print("you should enter 1  or 2 ")
            else:
                print("sorry number of ticket is more than remain capacity.....")
                break

def show_events():
    """ when user or admin want to see event file call this function"""
    all_events = event_file.read_csvfile_as_dictionary()
    return all_events


def find_specific_event(id):
    """ show spacial event that user want to see it information """

    try:
        # making data frame from csv file
        data = pd.read_csv("event_info.csv", index_col="event_id")
        # print(data)
        # retrieving row by loc method
        find_event = data.loc[id]
        return True,find_event
    except KeyError:
        print("event with this id there is not find")

def getting_event_id():
    """ for create a new event and set event_id for it  first should find the last event id and plus it 1   """
    with open("event_info.csv", 'r') as file:
        data = file.readlines()
        new_id=len(data)#new event id = number of last line in file

    return new_id










# event1 = Event("concert", "2021/12/25", "milad towel", 400, 350, 200, 20)
# event2 = Event ("Health Conference","2022/1/22","tehran",5000,5000,100,10)
# event3 = Event ("festival","2022/5/22","tabriz",7000,7000,150,5)
#
# event1.cal_discount()
# event2.cal_discount()
# event3.cal_discount()



# event_file.write(event1.__dict__)
# event_file.write(event2.__dict__)
# event_file.write(event3.__dict__)
