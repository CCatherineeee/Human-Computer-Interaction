from aip import AipSpeech



""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()



def get_command():
    result = client.asr(get_file_content('source/temp.wav'), 'wav', 8000, {
        'dev_pid': 1737,
    })
    return result['result']


# get_command()
# get_command()
