#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pylinuxoneclickinstall.py
#  
#  Copyright 2021 yucef sourni <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import time
import os
import tempfile
import sys
import subprocess
from site import addsitedir
import urllib.request as request
import importlib


system_arch = os.uname().machine
distro_desktop = os.getenv("XDG_CURRENT_DESKTOP",False)

def get_distro_name(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("ID") and not l.startswith("ID_"):
                result=l.split("=",1)[1].strip()
    return result.replace("\"","").replace("'","")

def get_distro_name_like(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("ID_LIKE") :
                result=l.split("=",1)[1].strip()
    if not result:
        result = get_distro_name(location)
    return result.replace("\"","").replace("'","")
    
def get_distro_version(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("VERSION_ID"):
                result=l.split("=",1)[1].strip()
    return result.replace("\"","").replace("'","")
    
def get_distro_version_like(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("VERSION_ID_LIKE") :
                result=l.split("=",1)[1].strip()
    if not result:
        result = get_distro_version(location)
    return result.replace("\"","").replace("'","")

def load_plugin(module_file):
    if module_file.endswith(".py") and os.path.isfile(module_file):
        module_name, module_extension = os.path.splitext(os.path.basename(module_file))
        plugin_folder = os.path.dirname(module_file)
        addsitedir(plugin_folder)
        spec   = importlib.util.spec_from_file_location(module_name,os.path.join(plugin_folder,module_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return False

    
def write_to_tmp(commands):
    time_now      = int(time.time()) * 4
    file_to_write = os.path.join(tempfile.gettempdir(),"{}.sh".format(time_now))
    with open(file_to_write,"w") as mf:
        for command in commands:
            mf.write(command+"\n")
    subprocess.call("chmod 755 "+file_to_write,shell=True)
    return file_to_write
    
def downlaod(link,location):
    agent  = {"User-Agent":"Mozilla/5.0"}
    name   = os.path.basename(link)
    saveas = os.path.join(location,name)
    os.makedirs(location, exist_ok=True)
    try:
        req   = request.Request(link,headers=agent)
        opurl = request.urlopen(req,timeout=10)
        size  = int(opurl.headers["Content-Length"])
        psize = 0
        ch    = 600
        print ("["+"-"*100+"]"+" "+str(size)+"b"+" "+"0%",end="\r",flush=True)
        with open(saveas, 'wb') as op:
            while psize < size:
                if ch > (size-psize):
                    chunk  = opurl.read(size-psize)
                    psize += size-psize
                else:
                    chunk  = opurl.read(ch)
                    psize += ch
                count = int((psize*100)//size)
                n = "#" * count
                op.write(chunk)
                print ("["+n+"-"*(100-count)+"]"+" "+str(size)+"b"+" "+str(round((psize*100)/size,2))+"%",end="\r",flush=True)
                op.flush()
        print (" "*200,end="\r",flush=True)
        print ("["+"#"*100+"]"+" "+str(size)+"b"+" "+"100%")
    except Exception as e:
        print(e)
        return False
    return saveas


def exit__(msg,code):
    print(msg)
    os.system("echo Press any key to exit.;read")
    exit(code)
    
if __name__ == "__main__" : 
    try:
        url = sys.argv[1]
        real_url = os.path.join("https://raw.githubusercontent.com/yucefsourani/pylinuxoneclickinstall/main",url.split(":",1)[1][2:].replace("?","/"))
        with tempfile.TemporaryDirectory() as tmpdirname:
            module_location = downlaod(real_url,tmpdirname)
            if module_location:
                module__ = load_plugin(module_location)
                if module__:
                    arch = module__.__arch__
                    if "all" not in arch  and system_arch not in arch:
                        exit__("\nThis Module Support This Arch '{}' Only .\n".format(arch),4)

                    distro = module__.__distro__
                    
                    if "all" not in distro  and get_distro_name_like() not in distro:
                        exit__("\nThis Module Support This Distro '{}' Only .\n".format(distro),5)

                    distro_version = module__.__distro_version__
                    if "all" not in distro_version  and get_distro_version_like() not in distro_version:
                        exit__("\nThis Module Support This Distro Version '{}' Only .\n".format(distro_version),6)

                    desktop = module__.__desktop__
                    if desktop != "None":
                        if "all" not in desktop  and not any([True for i in desktop if distro_desktop  in i]):
                            exit__("\nThis Module Support This Desktop '{}' Only .\n".format(desktop),7)

                    
                    commands = module__.__commands__.copy()
                    commands.append("echo Press any key to exit.")
                    commands.append("read")
                    file_to_run = write_to_tmp(commands)
                    while True:
                        os.system("clear")
                        print("\n"+real_url+"\n")
                        print("\nCommands To Run y/n ?\n")
                        count = 1
                        for i in module__.__commands__:
                            print("[Command {}]- {}".format(count,i))
                            count += 1
                        answer = input("\n- ").strip()
                        if answer == "y" or answer == "Y" :
                            break
                        elif answer == "n" or answer == "N":
                            exit__("\nBye...",0)

                    if subprocess.call("bash -c '{}'".format(file_to_run),shell=True) != 0 :
                        exit__("\nTask Fail.\n",1)

                else:
                    exit__("\nLoading {} Fail.\n".format(module_location),2)
            else:
                exit__("\nError Downloading {} .\n".format(real_url),3)
    except Exception as e:
        print(e)
        
