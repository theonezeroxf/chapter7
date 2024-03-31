import os
def run(**args):
    print("[*] In environment modules.")
    return str(os.environ)
if __name__=="__main__":
    run()

