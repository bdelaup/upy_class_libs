import os, rp2
import machine
import sdcard
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
    f_bsize : "Fs block size",
    f_frsize : "Fragment size",
    f_blocks : "Fs size f_frsize units",
    f_bfree : "Nb free blocks",
    f_bavail : "Nb free blocks for unprivileged users",
    f_files : "Nb inodes",
    f_ffree : "Nb free inodes",
    f_favail : "Nb free inodes for unprivileged users",
    f_flag : "Mount flags",
    f_namemax : "Maximum filename len"
}

def fs_info(path, unit = "kb", full = False):
    infos = os.statvfs(path)
    total_size = infos[f_frsize] * infos[f_blocks]
    free_size = infos[f_bsize] * infos[f_bfree]
    if unit=="mb":
        print (path+" | Size : %dMb | Free : %dMb [usage : %d%%]"%(total_size//1024//1024, free_size//1024//1024, (total_size-free_size)//total_size*100))
    elif unit =="gb" :
        pass
        print (path+" | Size : %dGb | Free : %dGb [usage : %d%%]"%(total_size//1024//1024//1024, free_size//1024//1024//1024, (total_size-free_size)//total_size*100))
    else : 
        print (path+" | Size : %dKb | Free : %dKb [usage : %d%%]"%(total_size//1024, free_size//1024, (total_size-free_size)//total_size*100))
    
    if full:
        for i in range(len(infos)):
            print(info_directory[i]+" "+str(infos[i]))

# WATCH dirty static management with globals
sd_vfs_fat = None
sd_mnt_point = None

def fs_use_sd(mnt_root_point = "/sd"):    
    # spi = machine.SPI(1)
    global sd_vfs_fat
    global sd_mnt_point
    if sd_vfs_fat != None:
        print("SD already used")
        return

    sd_mnt_point = mnt_root_point
    spi = machine.SPI(1, sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(12))
    # spi = machine.SPI(1)
    cs = machine.Pin(15)
    sd = sdcard.SDCard(spi, cs)
    sd_vfs_fat = os.VfsFat(sd)
    os.mount(sd_vfs_fat, sd_mnt_point)
    print ("SD mounted at "+sd_mnt_point)

def fs_unuse_sd(): 
    global sd_vfs_fat
    global sd_mnt_point
    if sd_vfs_fat == None:
        print("SD not used")
        return

    os.umount(sd_mnt_point)
    sd_vfs_fat = None
    print ("SD unmounted")
    

def test_write_sd():
    fs_use_sd('/sd')
    fs_info("/sd", "mb")

    f = open("/sd/test_write_sd.txt", "w")
    for i in range(100000):
        f.write("aaabbb cccddd\r\n")
    f.close()

    f = open("/sd/test_write_sd.txt", "a")
    for i in range(100000):
        f.write("eeefff ggghhh\r\n")
    f.close()
    
    fs_info("/sd", "mb")
    fs_unuse_sd()
    
def test_write_flash():
    f = open("/test_write_flash.txt", "w")
    fs_info("/")
    for i in range(1000):
        f.write("aaabbb cccddd\r\n")
    f.close()
    fs_info("/")

def test_format_sd():
    sd_mnt_point = "/sd"
    spi = machine.SPI(1, sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(12), baudrate=10000)    
    cs = machine.Pin(15)
    sd = sdcard.SDCard(spi, cs)
    os.VfsFat.mkfs(sd)
    sd_vfs_fat = os.VfsFat(sd)

    os.mount(sd_vfs_fat, sd_mnt_point)
    print ("SD mounted")
    os.umount(sd_mnt_point)
    print ("SD unmounted")

def test_fs_info_sd():
    fs_use_sd('/sd')
    fs_info("/sd", "kb")
    fs_info("/sd", "mb")
    fs_info("/sd", "gb")
    fs_unuse_sd()

def test_fs_info_flash():
    fs_info("/", "kb")
    fs_info("/", "mb")
    fs_info("/", "gb")

if __name__ == "__main__":
    # test_fs_info_sd()
    test_format_sd()
    # test_fs_info_flash()
    # test_write_sd()    
    # test_write_flash()