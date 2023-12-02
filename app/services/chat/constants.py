GPT_MESSAGE_TEMPLATE = '''
    (you manage the database and must choose a method based on the message) When using a message, you must determine which type it is from the following:
    1. update|email|{new_email}
    2. update|username|{new_username}
    3. delete|user|{id}
    4. show|my_profile|
    5. var_error
    6. error
    Replace the value in curly braces with the value sent in the message. If the selected type requires a value and one was not passed, then it will be of type var_error. If you cannot determine what type the message is, select the error type. Answer only with the selected type, do not explain your choice. For example, possible responses: update|email|kdksd@gmail.com, show|my_profile|, delete|user|jdshbckskcms, var_error
    
    Message:
'''
