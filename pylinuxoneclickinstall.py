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
import json
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
        run_rollback_commands = False
        real_url = os.path.join("https://raw.githubusercontent.com/yucefsourani/pylinuxoneclickinstall/main/",url.split(":",1)[1][2:].replace("?","/"))
        if real_url.endswith("#"):
            real_url = real_url[:-1]
            run_rollback_commands = True
        with tempfile.TemporaryDirectory() as tmpdirname:
            print("Downloading {} Plugin...\n".format(real_url))
            plugin_location = downlaod(real_url,tmpdirname)
            if plugin_location:
                if plugin_location.endswith(".py"):
                    clear = True
                    while True:
                        if clear:
                            os.system("clear")
                        clear = True
                        print("\n\033[31mWARNING !\033[0m \033[34mPython Module will be running and may be doing some invisible actions\033[0m\n\n\033[34mDo you agree\033[0m  \033[32my/n ? (R To View Python Module)\033[0m\n")
                        answer = input("\n- ").strip()
                        if answer == "y" or answer == "Y" :
                            break
                        if answer == "r" or answer == "R" :
                            if os.path.isfile(plugin_location):
                                with open(plugin_location) as mfp:
                                    for line in mfp:
                                        print(line)
                            else:
                                print("{} Not Found.".format(plugin_location))
                            clear = False
                        elif answer == "n" or answer == "N":
                            exit__("\nBye...",0)
                    plugin__ = load_plugin(plugin_location)
                    plugin__ = plugin__.__dict__.copy()
                elif plugin_location.endswith(".json"):
                    with open(plugin_location) as json_f:
                        plugin__ = json.load(json_f)
                else:
                    exit__("\nLoading {} Fail.\n".format(plugin_location),2) 
                if plugin__:
                    arch = plugin__["__arch__"]
                    if "all" not in arch  and system_arch not in arch:
                        exit__("\nThis Module Support This Arch '{}' Only .\n".format(arch),4)

                    distro = plugin__["__distro__"]
                    
                    if "all" not in distro  and get_distro_name_like() not in distro:
                        exit__("\nThis Module Support This Distro '{}' Only .\n".format(distro),5)

                    distro_version = plugin__["__distro_version__"]
                    if "all" not in distro_version  and get_distro_version_like() not in distro_version:
                        exit__("\nThis Module Support This Distro Version '{}' Only .\n".format(distro_version),6)

                    desktop = plugin__["__desktop__"]
                    if desktop != "None":
                        if "all" not in desktop  and not any([True for i in desktop if distro_desktop  in i]):
                            exit__("\nThis Module Support This Desktop '{}' Only .\n".format(desktop),7)

                    if run_rollback_commands:
                        commands = plugin__["__rollback_commands__"].copy()
                    else:
                        commands = plugin__["__run_task_commands__"].copy()
                    if not commands:
                        commands.append("\nNothing To Do.\n")
                    commands.append("echo Press any key to exit.")
                    commands.append("read")
                    
                    file_to_run = write_to_tmp(commands)
                    while True:
                        os.system("clear")
                        print("\n"+real_url+"\n")
                        print("\nCommands To Run y/n ?\n")
                        count = 1
                        if run_rollback_commands:
                            for i in plugin__["__rollback_commands__"]:
                                print("[Command {}]- {}".format(count,i))
                                count += 1
                        else:
                            for i in plugin__["__run_task_commands__"]:
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
                    exit__("\nLoading {} Fail.\n".format(plugin_location),2)
            else:
                exit__("\nError Downloading {} .\n".format(real_url),3)
    except Exception as e:
        print(e)
        
