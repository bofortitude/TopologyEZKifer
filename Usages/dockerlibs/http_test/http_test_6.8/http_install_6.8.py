#!/usr/bin/env python
from subprocess import call
from os import chdir,getcwd
from re import search
from shutil import copyfile
from os.path import exists
from time import sleep
from sys import exit,argv
from subprocess import Popen,PIPE

if len(argv) ==2:
    if argv[1] == 'full':
        full_bool = True
    elif argv[1] == 'quick':
        quick_bool = True
else:
    full_bool = False
    quick_bool = True

error_list = []
easyinstall_str  = ''
pip_str  = ''
install_bool = False
c_bool = False
f_bool = False
u_bool = False
add_bool = False
six_bool = False

call('tar -xvf http_test_6.8.tar',shell= True)

old_info,error = Popen('ls /bin/http_test -la',shell=True,stdout=PIPE).communicate()
if '->' in old_info:
    old_a = old_info.split('->')[1].strip()
    if search('http_test_(.+).py',old_a) is not None:
        old_v = search('http_test_(.+).py',old_a).group(1)
        if '5.9' > old_v >= '5.4':
            install_bool = False
            add_bool = True
            six_bool = True
        elif old_v < '5.4':
            add_bool = True
            install_bool = True
            six_bool = True
        elif old_v < '6.4':
            six_bool = True
            
    else:
        print '::::it should not appear,can not find that version number'
        install_bool,add_bool,six_bool = True,True,True
    
        
else:
    install_bool,add_bool,six_bool = True,True,True
    
if full_bool:
    install_bool,add_bool,six_bool = True,True,True
        
platform_info,error = Popen('cat /etc/issue',shell=True,stdout=PIPE).communicate()   

if  'Fedora' in platform_info:
    f_bool = True
    print '::::Found it is Fedora'
elif 'CentOS' in platform_info and '6.2' in platform_info:
    c_bool = True
    print '::::Found it is Centos 6.2'
elif 'Ubuntu' in platform_info:
    u_bool = True
    print ':::Found it is Ubuntu'
else:
    f_bool = True
    print ':::Can not recognize system by cat /etc/issue, just think it is fedora family'

if six_bool:
    call('tar xzvf six-1.10.0.tar.gz',shell= True)
    chdir('six-1.10.0')
    call('python setup.py install',shell= True)
    chdir('..')
    call('tar xzvf python-ntlm3-1.0.2.tar.gz',shell= True)
    chdir('python-ntlm3-1.0.2')
    call('python setup.py install',shell= True)
    chdir('..')
    

     
if full_bool:
    if u_bool:
        cmd = 'apt-get update'
        if call(cmd, shell=True) !=0:
            print ":::: Can't update the ubuntu system" 
            error_list.append(':::: INSTALL tkinter fail')
            exit()
    if install_bool:
        easyinstall_info,error = Popen('whereis easy_install',shell=True,stdout=PIPE).communicate()
    
        if '/usr/bin' in easyinstall_info:
            easyinstall_str = 'easy_install'
        else:
            print "::::Can't find the easy_install,try it install it"
            if f_bool or c_bool:
                cmd = 'yum -y install python-setuptools python-devel'
            elif u_bool:
            	cmd = 'apt-get -y install python-setuptools -y --force-yes'
            if call(cmd,shell= True) == 0:
          
                easyinstall_info,error = Popen('whereis easy_install',shell=True,stdout=PIPE).communicate()
                if '/usr/bin' in easyinstall_info:
                    print '::::install setuptools successfully'
                else:
                    print '::::install setuptools Fail'
                    error_list.append("::::install setuptools Fail")
                    exit()    
            else:
                print '::::install setuptools Fail'
                error_list.append("::::install setuptools Fail")
                exit()   
        sleep(1)
    
        
        pip_info,error = Popen('whereis pip',shell=True,stdout=PIPE).communicate()
        if '/usr/bin' in pip_info:
            pip_str = 'pip'
        else:
            pip_info,error = Popen('whereis pip-python',shell=True,stdout=PIPE).communicate()
            if '/usr/bin' in pip_info:
                pip_str = 'pip-python'
            else:
                if f_bool:
                    call('yum  -y install python-pip', shell=True )
                elif u_bool:
                	call('apt-get install python-pip -y --force-yes', shell=True )
                elif c_bool:
                    call('python get-pip.py',shell = True)
                pip_info,error = Popen('whereis pip',shell=True,stdout=PIPE).communicate()
                if '/usr/bin' in pip_info:
                    pip_str = 'pip'
                else:
                    pip_info,error = Popen('whereis pip-python',shell=True,stdout=PIPE).communicate()
                    if '/usr/bin' in pip_info:
                        pip_str = 'pip-python'
        if not pip_str:
            print '::::can not find pip after install '
            exit()
        print '::::try to uninstall pyopenssl firstly'
        print ':::: pip_str is %s' % pip_str
    
    if add_bool:
        call('%s uninstall pyOpenSSL -y' % pip_str, shell=True)
        try:
            import OpenSSL.SSL
            result = str(reload(OpenSSL.SSL))
            dir_ori = search("from '(.+/)SSL.so",str(result))
            if dir_ori is not None:
                dir = dir_ori.group(1)
                print ':::: the dir is %s' % dir
                call('rm %s -rf' % dir, shell = True)
        
                print(':::: rm the old ssl folder')
        except Exception,e:
            print "::: Can not delete ssl due to %s" % e
    
        call('tar -zxvf pyOpenSSL-0.15.1.tar.gz',shell= True)
        chdir('pyOpenSSL-0.15.1')
        call('python setup.py install',shell= True)
        chdir('..')    
        
    if install_bool:
            
        if u_bool:
        	cmd = 'apt-get install build-essential libssl-dev libffi-dev python-dev -y --force-yes'
        else:
            cmd = 'yum  -y install gcc libffi-devel openssl-devel'
        if call(cmd, shell=True ) !=0:
            print 'update gcc fail'
            error_list.append('update gcc fail')
        sleep(1)
        if call('easy_install cryptography', shell=True) !=0:
            print ':::: INSTALL cryptography fail'
            error_list.append(':::: INSTALL cryptography fail')    
        sleep(1)
        if call('easy_install pyasn1', shell=True) == 0:
            print '::::INSTALL pyasn1 successfully '
        else:
            print '::::INSTALL pyasn1 fail'
            error_list.append('::::INSTALL pyasn1 fail')
        
        sleep(1)
        
        
        if call('easy_install ndg-httpsclient', shell=True) == 0:
            print '::::INSTALL ndg-httpsclient successfully'
        else:
            print '::::INSTALL ndg-httpsclient fail'
            
            error_list.append('::::INSTALL ndg-httpsclient fail')
        sleep(1)
    
    
if install_bool:
    if u_bool:
        cmd = 'apt-get update'
        if call(cmd, shell=True) !=0:
            print ":::: Can't update the ubuntusystem" 
            error_list.append(':::: INSTALL tkinter fail')
            exit()
    if u_bool:
        cmd = 'apt-get install python-tk -y --force-yes'
    else:
    	cmd = 'yum -y install tkinter'
    if call(cmd, shell=True) !=0:
        print ':::: INSTALL tkinter fail'
        error_list.append(':::: INSTALL tkinter fail')    
    
    
    sleep(1)
    call('tar -zxvf pyttk-0.3.2.tar.gz',shell= True)


    chdir('pyttk-0.3.2')
    call('python setup.py install',shell= True)
    chdir('..')
cur_dir = getcwd()



call('tar -zxvf httplib2-0.7.4.tar.gz',shell= True)
if install_bool:
    call('tar -zxvf pexpect-2.3.tar.gz',shell= True)
    chdir('pexpect-2.3')
    call('python setup.py install',shell= True)
    chdir('..')
chdir('httplib2-0.7.4')
call('python setup.py install',shell= True)
chdir('..')


call('chmod +x ./http_test_6.8.py',shell= True)
call('chmod +x ./http_gui_6.8.py',shell= True)
call('chmod +x ./update.py',shell= True)

if c_bool:
   call('mv centos.ini http_gui.ini',shell= True) 
if f_bool or u_bool:
   call('mv fedora.ini http_gui.ini',shell= True) 

if exists('/bin/http_test'):
    call('rm /bin/http_test -rf', shell=True)
    print ':::: rmove old http_test link'
if exists('/bin/http_gui'):
    call('rm /bin/http_gui -rf', shell=True)
    print ':::: rmove old http_gui link'
call('ln -s -f %s/http_test_6.8.py /bin/http_test' % cur_dir,shell = True)
call('ln -s -f %s/http_gui_6.8.py /bin/http_gui' % cur_dir,shell = True)
call('ln -s -f %s/update.py /bin/jiasheng_update' % cur_dir,shell = True)
print 'task over'

if error_list:
    for i in error_list:
        print i
        
