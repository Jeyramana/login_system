
def registration(username, password, filename):
    # Dumping Username and Password
    
    counter = len(open(filename).readlines())
    if counter == 0:
        with open(filename, 'w') as file:
            file.write(f"{username}, {password}")
        print('User Credentials Registered.')
    else:
        with open(filename, 'a') as file:
            file.write(f"\n{username}, {password}")
        print('User Credentials Registered.')
    start_screen()
    
def error_prompt(txt, prompter=''):
    # User friendly error prompter for easy debugging

    if txt == 'user':
        print('Username Invalid !')
        print('Error', prompter)
        start_screen()
    elif txt == 'pass':
        print('Password Invalid !')
        print('Error', prompter)
        start_screen()
    elif txt == 'login_exist':
        print(f"Error: {prompter}")
        start_screen()

def validator(username, password):
    """ 1. Email id should start with letter
        2. Name field shouldn't end with special character or underscore
        3. No more than 1 period in name field
        4. No special character in name field
        5. Appropriate length for domain
        6. Password length b/w 5 - 16
        7. Password must contain chracters [a-z] [A-Z] [0-9] & Special characters
    """

    import re
    small_alpha = 'abcdefghijklmnopqrstuvwxyz'
    capit_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    spcial_chr = '!@#$%^&*()?'
    numbers = '0123456789'

    validity_count = 0
    
    # Validating Username
    if '@' in username and '.' in username:
        user_id = re.split('@', username)
        login_id = re.split('[.]', user_id[1])
        user_id.remove(user_id[1])

        if len(user_id) + len(login_id) == 3 and '' not in user_id and '' not in login_id:
            
            if user_id[0][0] not in (spcial_chr + numbers) and user_id[0][-1] not in spcial_chr+'_':
                if user_id[0].count('.') <= 1:
                    special_s = [user_id[0][i] for i in range(1, len(user_id[0])-1) if user_id[0][i] in spcial_chr+' ']
                    special_s1 = [login_id[0][i] for i in range(len(login_id[0])) if login_id[0][i] in (spcial_chr+numbers)]
                    mailer_len = len(login_id[0])
                    special_s2 = [login_id[1][i] for i in range(len(login_id[1])) if login_id[1][i] in (spcial_chr+numbers)]
                    domain_len = len(login_id[1])
                    if special_s == [] and special_s1 == [] and mailer_len >= 3 and special_s2 == [] and domain_len >= 2:
                        validity_count += 1 
                    else:
                        prompter = str(special_s)+str(special_s1)+str(mailer_len)+str(special_s2)+str(domain_len)
                        prompter = f'5: {username} - Invalid Character exists or Invalid length'
                        error_prompt('user', prompter)
                        return
                else:
                    prompter = f'4: {username} - More than one periods exists'
                    error_prompt('user', prompter)
                    return
            else:
                prompter = f'3: {username} - Special character or number exists in beginning or at the end of user id'
                error_prompt('user', prompter)
                return
        else:
            prompter = f"2: {username} - Problem with @ or '.' or length of user id / domain"
            error_prompt('user', prompter)
            return
    else:
        prompter = f'1: {username} - Missing @ or .'
        error_prompt('user', prompter)
        return

    # Validating Password
    if len(password) > 5 and len(password) < 16:
        count_s, count_c, count_sp, count_n = 0, 0, 0, 0
        for i in password:
            if i in small_alpha: count_s += 1
            elif i in capit_alpha: count_c += 1
            elif i in spcial_chr: count_sp += 1
            elif i in numbers: count_n += 1
        if count_s >= 1 and count_c >= 1 and count_sp >= 1 and count_n >= 1:
            validity_count += 1
        else:
            prompter = f"2: {password} - Password must contain one character from [a-z], [A-Z], [0-9],[!@#$%^&*()?]"
            error_prompt('pass', prompter)
            return
    else:
        prompter = f"1: {password} - Problem with length of password"
        error_prompt('pass', prompter)
        return

    if validity_count == 2:
        return True

def login(username, password, filename):
    # Login checks for user & password match in CSV file

    lines = open(filename).readlines()
    user_found = False
    pass_match = False
    
    for i in lines:
        j = i.split(',')
        if j[0] == username:
            user_found = True
            if  j[1].strip() == password:
                pass_match = True
                print('User Loged In.')
                break
    if user_found == False or pass_match == False:
        if user_found == False:
            print(f'{username}: Username Error !')
        elif pass_match == False:
            print(f'{username}: Password Error !')
        
        prompter = 'Try (F) Forget Password OR (R) Register.\n'
        error_prompt('login_exist',prompter)
    else:
        start_screen()

def retriever(username, filename):
    # Password retrieved from CSV file when Foreget Password option is selected

    result = open(filename).readlines()
    
    user_found = False
    for i in result:
        j = i.split(',')
        if j[0].strip() == username:
            user_found = True
            print(f'Password for {username} : {j[1].strip()}')
            break
    if user_found == False:
        error_prompt('login_exist',username)
    else:
        start_screen()

def caller_func(choice, username, password=''):
    # CSV file input provided manually and respective login, register, forget functions are called

    filename = 'user_pass.csv'
    if choice == 'R':
        valid = validator(username, password)
        if valid:
            print('Validated: ', username, password)
            # Starting Registration Process
            registration(username, password, filename)
    elif choice == 'L':
        login(username, password, filename)
    elif choice == 'F':
        retriever(username, filename)

def start_screen():
    # Provides Options to perform

    print('\nPress (L) for Login')
    print('Press (F) for Forget Password')
    print('Press (R) for Registration')
    choice = input('Press (X) to exit:   ')
    if choice == 'L' or choice == 'R':
        username = input('Enter Username: ')
        password = input('Enter Password: ')
        caller_func(choice, username, password)
    elif choice == 'F':
        username = input('Only Enter Username: ')
        caller_func(choice, username)
    elif choice == 'X':
        return


if __name__ == "__main__":
    # Initiate the Start Screen
    trial_count = 0
    start_screen()      
    
