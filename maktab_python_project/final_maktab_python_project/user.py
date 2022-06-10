import logging
import hashlib, binascii, os
import file_handeling


class User:

    saved = None

    def __init__(self, first_name, last_name, user_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password
        self.user_id = 'u' + str(getting_user_id())





    @classmethod
    def register_new_user(cls):
        print("welcome to event system enter your information to register !!! ")
        first_name = input("enter your first name:")
        last_name = input("enter your last name:")
        user_name = input("enter a user_name to use it when login to system:")
        # that is  better to chose a  spacial pattern for password fix it later
        password1 = input("enter password to use it when login to system:")
        password2 = input("repeat your password :")
        while True:
            """ you should check this new user there is not in user file  because we can not use duplicate user """
            all_user = user_file.read_csvfile_as_dictionary()
            i = 0
            while i < len(all_user):

                if all_user[i]['user_name'] == user_name:
                    i = 0# When it finds a duplicate username, it must check again that the new input is not duplicated

                    print("sorry before you another person register with this user name")

                    user_name = input("enter another user_name :")
                else:
                    i += 1
            if password1 != password2:
                print("sorry the passwords entered are not the same ")
                password1 = input("enter password to use it when login to system:")
                password2 = input("repeat your password :")

            elif password1 == password2:
                User.saved=password1#before hash pass saved it in a calss attribute to show user

                password = hash_password(password1)
                break
        logging.basicConfig(filename='record.log', level=logging.INFO, filemode='a',
                            format='%(asctime)s %(message)s %(name)s', datefmt='%m/%d/%Y %I:%M:%S %p'
                            )
        logging.info(f"{user_name} register as a new user ")


        return cls(first_name, last_name, user_name, password)

    def __str__(self):
        return f"{self.first_name}  {self.last_name} you register as new user your user name : " \
               f"{self.user_name} and your password : {User.saved} " \
               f"please keep them and don't forget (:  "


def sign_in(sign_username, sign_pass, counter):
    """ this method check admin name and password
        i use read_csvfile_as_dictionary method  from file_handeling module for access every admin
        """
    all_user = user_file.read_csvfile_as_dictionary()  # list of users from file
    counter_pass = counter

    for i in range(len(all_user)):

        if all_user[i]['user_name'] == sign_username:  # username is True and want to check pass
            if verify_password(all_user[i]['password'], sign_pass):
                print(f" Hello {all_user[i]['first_name']} welcome !! ")
                logging.basicConfig(filename='record.log', level=logging.INFO, filemode='a',
                                    format='%(asctime)s %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p'
                                    )
                logging.info(f" admin  with {all_user[i]['first_name']} admin name sign in to event system")

                return True
            else:
                print("password is wrong!!")

                if counter_pass <= 3:
                    logging.basicConfig(filename='record.log', level=logging.INFO, filemode='a',
                                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
                                        )
                    logging.warning(
                        f" admin {all_user[i]['user_name']} entered the password incorrectly {counter_pass} times ")
                elif counter_pass == 3:
                    print("sorry  you entered password incorrectly three time more  ):")
                    logging.basicConfig(filename="record.log", filemode='a',
                                        format="% (level name)s - %(asc time)s  - %(massage)s",
                                        datefmt='%d - %b - % y  %H:%M:%S')
                    logging.warning(
                        f" user by {all_user[i]['user_name']} "
                        f"user name entered the password incorrectly three times  and account get blocked ")
                return False


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def getting_user_id():
    """ for create a new event and set event_id for it  first should find the last event id and plus it 1   """
    with open("user_info.csv", 'r') as file:
        data = file.readlines()
        new_id=len(data)#new user id = number of last line in file

    return new_id


user_file = file_handeling.File("user_info.csv")
# user1=User.register_new_user()
# user_file.write(user1.__dict__)
