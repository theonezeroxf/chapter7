import os
def run(**args):
    print("[*] In dirlister modules.")
    files=os.listdir(".")
    return str(files)
if __name__=="__main__":
    run()