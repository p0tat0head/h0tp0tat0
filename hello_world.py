#!/usr/bin/env python2
import os,stat,errno
import fuse
from fuse import Fuse

fuse.fuse_python_api = (0, 2)

hello_path = '/hello'
hello_str = 'Hello World!\n'

class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode=0
        self.st_ino=0
        self.st_dev=0
        self.st_nlink=0
        self.st_uid=0
        self.st_gid=0
        self.st_size=0
        self.st_atime=0
        self.st_mtime=0
        self.st_ctime=0
        
class HelloFS(Fuse):
    flags = 1
    def getattr(self, path):
        st = MyStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif path == hello_path:
            st.st_mode = stat.S_IFREG | 0444
            st.st_nlink = 1
            st.st_size = len(hello_str)
        else:
            return -errno.ENOENT
        return st
    
    def readdir(self, path, offset):
        ret = ['.',
               '..',
               hello_path[1:]]
        for r in ret:
            yield fuse.Direntry(r)
            
    def open(self, path, flags):
        if path!=hello_path:
            return -errno.ENOENT
        if (flags & 3) != os.O_RDONLY:
            return -errno.EACCES
        return 0

    def read(self, path, size, offset):
        if path != hello_path:
            return -errno.ENOENT
        slen = len(hello_str)
        if offset < slen:
            if (offset+size)>slen:
                size = slen-offset
                buf = hello_str[offset:offset+size]
            else:
                buf = ''
            return buf

def main():
    usage="""
    Userspace hello example
    
    """ + Fuse.fusage
    server = HelloFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(values=server, errex=1)
    server.main()
        

if __name__=='__main__':
    main()
