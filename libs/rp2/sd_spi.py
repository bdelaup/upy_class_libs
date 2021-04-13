import os, rp2

from micropython import const

f_bsize = const(0)
f_frsize = const(1)
f_blocks = const(2)
f_bfree = const(3)
f_bavail = const(4)
f_files = const(5)
f_ffree = const(6)
f_favail = const(7)
f_flag = const(8)
f_namemax = const(9)


info_directory = {
    f_bsize : "File system block size",
    f_frsize : "Fragment size",
    f_blocks : "Size of fs in f_frsize units",
    f_bfree : "Number of free blocks",
    f_bavail : "Number of free blocks for unprivileged users",
    f_files : "Number of inodes",
    f_ffree : "Number of free inodes",
    f_favail : "Number of free inodes for unprivileged users",
    f_flag : "Mount flags",
    f_namemax : "Maximum filename length"
}

def fs_info(path, full = False):
    infos = os.statvfs(path)
    total_size = infos[f_frsize] * infos[f_blocks]
    free_size = infos[f_bsize] * infos[f_bfree]
    print ("Size : %dkb | Free : %dkb (%d/100)"%(total_size//1024, free_size//1024, (total_size-free_size)//total_size*100))

    if full:
        for i in range(len(infos)):
            print(info_directory[i]+" "+str(infos[i]))

    

    
if __name__ == "__main__":
    fs_info("/")

# os.umount('path')


# os.chdir('/sd')