import hashlib, ping3, paramiko

class myServer():    
    Host = 'localhost'
    User = 'user'
    Passwd = 'qwerty'
    Port = '22'
    Result = 0

    def ping(self):
        result = ping3.ping(self.Host, timeout=1)
        return result is not None
       
    def hash_file(self, filename):        
        h = hashlib.sha256()
        with open(filename, 'rb') as f:            
            chunk = f.read(8192)
            while chunk:
                h.update(chunk)
                chunk = f.read(8192)
        return h.hexdigest()

    def sv_stop(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.Host, username=self.User, password=self.Passwd, timeout=1)
            stdin, stdout, stderr = ssh.exec_command('/home/stop.sh')
            self.Result = stdout.read().decode('utf-8')# + ' // ' + stderr.read().decode('utf-8')
        finally:
            ssh.close()
        
    def sv_start(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.Host, username=self.User, password=self.Passwd, timeout=1)
            stdin, stdout, stderr = ssh.exec_command('/home/start.sh')
            self.Result = stdout.read().decode('utf-8')# + ' // ' + stderr.read().decode('utf-8')
        finally:
            ssh.close()
        
    def sv_update(self):
        self.sv_stop()
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.Host, username=self.User, password=self.Passwd, timeout=1)
            stdin, stdout, stderr = ssh.exec_command('/patcher/cpw.sh')
            self.Result = stdout.read().decode('utf-8')# + ' // ' + stderr.read().decode('utf-8')
        finally:
            ssh.close()
        
    def ping(self):
        try:
            result = ping3.ping(self.Host, timeout=1)
            return result is not None            
        except:
            return False

    def sv_scan(self):
        if self.ping():
            try:
                stream = paramiko.SSHClient()
                stream.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                stream.connect(hostname=self.Host, username=self.User, password=self.Passwd, timeout=1)
                stdin, stdout, stderr = stream.exec_command(f"ps -aux | grep -v 'grep' | grep -w 'gs'")
                output = stdout.read().decode('utf-8')                
            finally:
                stream.close()
            return output

    def sv_check(self, Component, demon='gs'):
        result = self.ping()       
        if result:
            try:
                stream = paramiko.SSHClient()
                stream.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                stream.connect(hostname=self.Host, username=self.User, password=self.Passwd, timeout=1)
                stdin, stdout, stderr = stream.exec_command(f"ps -aux | grep -v 'grep' | grep -w '{demon}'")
                output = stdout.read().decode('utf-8')            
                result = demon in output
                if result:
                    if Component: Component.config(text="Включен", bg='green')                    
                else :
                    if Component: Component.config(text="Выключен", bg='red')
            finally:
                stream.close()
        else:
            if Component: Component.config(text="Не доступно", bg='gray')
        return result

    def sv_comand(self, comand='ls -l'):
        result = self.ping()        
        if result:
            try:
                stream = paramiko.SSHClient()
                stream.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                stream.connect(hostname=self.Host, username=self.User, password=self.Passwd, timeout=1)
                #stdin, stdout, stderr = 
                stream.exec_command(f"cd /home/gamed/; ./gs {comand} > /home/logs/{comand}.log &")
            finally:
                stream.close()        
        return result
    
    def sv_poweroff(self):
        if self.ping():
            try:
                stream = paramiko.SSHClient()
                stream.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                stream.connect(hostname=self.Host, username=self.User, password=self.Passwd, timeout=1)
                stdin, stdout, stderr = stream.exec_command('poweroff')
                self.Result = stdout.read().decode('utf-8')      
            finally:
                stream.close()
        
