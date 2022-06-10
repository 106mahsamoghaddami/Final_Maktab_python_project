import logging
import hashlib, binascii, os
import file_handeling


class Admin:
    counter = 0

    def __init__(self, first_name, last_name, user_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.admin_name = user_name
        self.password = password
        Admin.counter += 1
        self.admin_id = 'a' + str(Admin.counter)

    def __str__(self):
        return f"you are admin {self.admin_name} and your password is {self.password} " \
               f"please keep them and don't forget (:  "


def sign_in(sign_admin_name, sign_pass, counter):
    """ this method check admin name and password
        i use read_csvfile_as_dictionary method  from file_handeling module for access every admin
        """
    all_admin = admin_file.read_csvfile_as_dictionary()  # list of admins from file
    counter_pass = counter


    for i in range(len(all_admin)):
        if all_admin[i]['admin_name'] == sign_admin_name:  # username is True and want to check pass
            if verify_password(all_admin[i]['password'], sign_pass):
                print(f" Hello {all_admin[i]['first_name']} welcome !! ")
                logging.basicConfig(filename='record.log', level=logging.INFO, filemode='a',
                                    format='%(asctime)s %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p'
                                    )
                logging.info(f" admin  with {all_admin[i]['first_name']} admin name sign in to event system")

                return True
            else:
                print("password is wrong!!")

                if counter_pass < 3:
                    logging.basicConfig(filename='record.log', level=logging.INFO, filemode='a',
                                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
                                        )
                    logging.warning(
                        f" admin {all_admin[i]['admin_name']} entered the password incorrectly {counter_pass} times ")
                elif counter_pass == 3:
                    print("sorry  you entered password incorrectly three time more  ):")
                    logging.basicConfig(filename="record.log", filemode='a',
                                        format="% (level name)s - %(asc time)s  - %(massage)s",
                                        datefmt='%d - %b - % y  %H:%M:%S')
                    logging.warning(
                        f" admin by {all_admin[i]['admin_name']} "
                        f"admin name entered the password incorrectly three times  and account get blocked ")
                return False
        # else:
        #     print("admin name is wrong!!!")
        #
        #     logging.basicConfig(filename="record.log", level=logging.INFO,filemode='a',
        #                         format="% (level name)s - %(asc time)s  - %(massage)s",
        #                         datefmt='%d - %b - % y  %H:%M:%S')
        #     logging.warning(
        #         f" An unknown user is trying to log in !!!! ")
        #     return False


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


#  i should make many instance from admin class and insert them to file admin_info:

# admin1 = Admin('Mahsa', "Moghaddami", 'mahsa1375',hash_password('1375') )
# admin2 = Admin('Sara', 'Saboori', 'sara1370', hash_password('1370'))
# admin3 = Admin('Reza', 'Rezaee', 'reza1365', hash_password('1365'))

admin_file = file_handeling.File('admin_info.csv')

# admin_file.write(admin1.__dict__)
# admin_file.write(admin2.__dict__)
# admin_file.write(admin3.__dict__)
# p =hash_password('1375')
# print(verify_password(p,'1375'))
