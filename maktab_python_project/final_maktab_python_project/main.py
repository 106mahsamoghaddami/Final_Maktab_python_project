import admin
import event
import user


print("Welcome to event system :) ")

while True:
    try:
        valid_num = int(input("sign in ---> enter1 **** sign up---> enter 2 :"))
        if valid_num != 1 and valid_num != 2:
            raise TypeError("Oops!  That was no valid number .  Try again and enter just 1 or 2 ... ")
        else:
            break
    except (TypeError, ValueError):
        print('Oops!  That was no valid number.  Try again and enter just 1 or 2 ...')

""" 
This part is for sign in when user enter 1 .... 
"""
if valid_num == 1:
    print(" please enter you want to sign in  as  A)admin or B)user : ")
    while True:
        try:
            admin_user = input("if you are admin ---> enter A **** if you are user---> enter B :").upper()
            if admin_user != 'A' and admin_user != 'B':
                raise TypeError("Oops!  That was no valid input  .  Try again and enter just A or B ... ")
            else:
                break
        except (TypeError, ValueError):
            print('Oops!  That was no valid input.  Try again and enter just A or B ...')



#***************************************************************************************************************
#admin part

    """ 
    if input ==A that means  want to sign in as admin this part from 38 until 85 is for admin activity
    fist check username and pass to sign in 
    then admin can register new event or see list of all events
    """
    if admin_user == 'A':
        print("you want to sign in as admin !!!")
        sign_admin_name = input("enter your admin name:")
        sign_pass = input("enter your password to sign in :")
        pass_counter = 1

        while pass_counter <= 3:
            # for check username and pass call a function from admin module
            check_account = admin.sign_in(sign_admin_name, sign_pass, pass_counter)

            if check_account:

                break


            else:
                pass_counter += 1
                sign_admin_name = input("enter your  correct admin name:")
                sign_pass = input("enter your  correct password to sign in :")

        if check_account:# admin can sign in succesfully
            print("you as a admin can see event list and define new event ")

            user_act = int(input("1 ) see all events \n  2 )define new event \n 3)exit"))

            while  True :
                if user_act != 1 and user_act != 2 and user_act != 3:
                    raise TypeError("Oops!  That was no valid number .  Try again and enter just 1 , 2 or 3... ")
                    user_act = int(input("1 ) see all events \n  2 )define new event \n 3)exit"))
                elif user_act ==1:
                    """admin want to see event lists"""
                    event_dict = event.show_events()
                    for item in event_dict:
                        print(item)
                    user_act = int(input("1 ) see all events \n  2 )define new event \n 3)exit"))
                elif user_act ==2:
                    """admin want to define new event"""
                    print(f" new event that you define it : {event.define_event()}")
                    user_act = int(input("1 ) see all events \n  2 )define new event \n 3)exit"))
                elif user_act == 3:
                    break


#***************************************************************************************************************
#user part

    elif admin_user == 'B':
        """ 
           if input ==B that means  want to sign in as user this part from 97 until .. is for user  activity
           fist check username and pass to sign in 
           then user can  see event lists and buy  event
        """
        print("you want to sign in as user!!!")
        sign_username = input("enter your user name:")
        sign_password = input("enter your password to sign in :")
        p_counter = 1

        while p_counter <= 3:
            # for check username and pass call a function from user module
            check_user = user.sign_in(sign_username, sign_password, p_counter)

            if check_user:

                break


            else:
                p_counter += 1
                sign_username = input("enter your  correct user name:")
                sign_password = input("enter your  correct password to sign in :")
        if check_user:#user can sign in succesfully

            print("you as a user can see event list and buy an event ")

            user_act = int(input("1 ) see all events \n  2 )to shopping \n 3)exit"))

            while  True :
                if user_act != 1 and user_act != 2 and user_act != 3:
                    raise TypeError("Oops!  That was no valid number .  Try again and enter just 1 , 2 or 3... ")
                    user_act = int(input("1 ) see all events \n  2 )buy event \n 3)exit"))
                elif user_act ==1:
                    """user want to see event lists"""

                    event_dict = event.show_events()
                    for item in event_dict:
                        print(item)

                    user_act = int(input("1 ) see all events \n  2 )buy event \n 3)exit"))
                elif user_act ==2:
                    """user want to buy an event"""
                    event_request_id=int(input("enter your event id to buy it "))

                    # for check event id and find specific event
                    result_search_id=event.find_specific_event(event_request_id)

                    try:
                        if result_search_id[0] == True:
                            print(f" information of your asked event :\n {result_search_id}")

                            number_ticket = input("Enter the number of tickets")
                            do_shopping = event.ticket_sale(number_ticket, event_request_id)




                    except TypeError:
                        print("try with new correct event id....")

                    user_act = int(input("1 ) see all events \n  2 )buy event \n 3)exit"))
                elif user_act == 3:
                    break
#****************************************************************************************************************
# sign up
""" 
This part is for sign up when user enter 2 .... 
"""
if valid_num == 2:
    print("You can only register as a regular user... ")
    new_user=user.User.register_new_user()
    print(new_user)
    write_to_file=user.user_file.write(new_user.__dict__)
