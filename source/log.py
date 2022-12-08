from datetime import date, datetime, timedelta
from os import listdir, remove, fsync, mkdir, getcwd
from os.path import isfile, join, isdir

class Log:
    def __init__(self, directory='log/', days_to_keep=14):
        self.dir = directory
        if not isdir(self.dir):
            mkdir(f'{getcwd()}/{self.dir[:-1]}')
            
        self.day = date.today().strftime('%Y-%m-%d')
        self.file = open(f'{self.dir}{self.day}.log', 'a', encoding="utf-8")
        self.days_to_keep = days_to_keep
        self.append_log('Start of log')
        

    def reset_file(self): # Resets the log file for a new day
        self.file.write('Log roll over')
        self.file.flush()
        fsync(self.file.fileno())
        
        self.file.close()
        self.day = date.today().strftime('%Y-%m-%d')
        self.file = open(f'{self.dir}{self.day}.log', 'a', encoding="utf-8")
        self.remove_old_log(self.days_to_keep)
        self.append_log('Log roll over')


    def append_log(self, message, console=True):
        if self.day != date.today().strftime('%Y-%m-%d'): # Check whether log roll over is required
            self.reset_file()
            
        time = datetime.now().strftime('%H:%M:%S')
        message = f'[{time}] {message}\n'
        if console:
            print(message[:-1])

        self.file.write(message)
        self.file.flush()
        fsync(self.file.fileno())


    def remove_old_log(self, days_old = 14):
        # Assumes the date portion starts at the front of the file and is 10 charatcers long
        files = [f[:10] for f in listdir(self.dir) if isfile(join(self.dir, f))]
        self.append_log(f'Deleting logs {days_old} days old')
        no_logs = 0
        for file in files:
            if file < (datetime.today() - timedelta(days=days_old)).strftime('%Y-%m-%d'):
                no_logs += 1
                remove(f'{self.dir}{file}.log')

        self.append_log(f'{no_logs} logs deleted')
        