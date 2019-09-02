import requests

#method that initializes the connection to HomeAccessCenter and returns the contained HTML in the page
def connect(user_name, pass_word):
    header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

    login_data = {
        'SCKTY00328510CustomEnabled' : 'False',
        'Database' : '10',
        'LogOnDetails.UserName' : user_name,
        'LogOnDetails.Password' : pass_word
    }

    #creates a session that initiates a login connection with specified paramaters
    with requests.Session() as c:
        url = 'https://lis-hac.eschoolplus.powerschool.com/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess'
        c.get(url)
        c.post(url, data = login_data, headers = header)
        assignments_page = c.get('https://lis-hac.eschoolplus.powerschool.com/HomeAccess/Content/Student/Assignments.aspx')
        return assignments_page

def write_updates(text):
    with open('reminders.txt', 'w') as file:
        file.write(text)

def get_credentials():
    user_name = ''
    pass_word = ''
    with open('credentials.txt', 'r') as file:
        user_name = file.readline()
        user_name = user_name[user_name.index('\'')+1: user_name.rfind('\'')]
        pass_word = file.readline()
        pass_word = pass_word[pass_word.index('\'')+1: pass_word.rfind('\'')]
    return user_name, pass_word
