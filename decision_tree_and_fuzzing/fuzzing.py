from __future__ import print_function

import inspect
import json
import random


class fuzzing_buffer :
    
    def __stack_trace__(self) :
        stack = inspect.stack()
        call_point = stack[2]
        py_name = call_point[1]
        py_name = py_name[py_name.rfind('\\') + 1 : ]
        line = str(call_point[2])
        function = call_point[3]
        code = call_point[4][0].replace('\n','').strip()
        
        return code#py_name + '/\\' + function + '/\\' + code + '/\\' + line
    
    def __init__(self,fuzzing_data) :
        self.data = fuzzing_data
        self.reference_record_list = []
        
    def __getitem__(self,index) :
        reference_infomation = self.__stack_trace__()
        
        self.reference_record_list.append(('getitem',index,reference_infomation))
        
        return self.data[index]
      
    def __setitem__(self,index,value) :
        reference_infomation = self.__stack_trace__()
        
        self.reference_record_list.append(('setitem',index,value,reference_infomation))
        
        self.data[index] = value
    
    def __get__(self) :
        reference_infomation = self.__stack_trace__()
        
        self.reference_record_list.append(('get',0,reference_infomation))
        
        return self.data
        
    def __set__(self,data) :
        self.data = data
        reference_infomation = self.__stack_trace__()
        
        self.reference_record_list.append(('set',0,reference_infomation))
        
    def __len__(self) :
        #reference_infomation = self.__stack_trace__()
        #self.reference_record_list.append(('len',0,reference_infomation))
        
        return len(self.data)
    
    def get_record(self) :
        return self.reference_record_list
    
    def get_data(self) :
        return self.data
    
class fuzzing_decision_node(dict) :
    
    def __init__(self) :
        dict.__init__(self)
        
        self.node_data = []
        
    def add_node_data(self,node_data) :
        if list == type(node_data) :
            for index in node_data :
                if not self.node_data.count(index) :
                    continue
                    
                self.node_data.append(index)
        else :
            if not self.node_data.count(node_data) :
                self.node_data.append(node_data)
        
    def get_node_data(self) :
        return self.node_data
    
class fuzzing_decision_tree :
    
    def __init__(self) :
        self.tree = fuzzing_decision_node()
        self.tree['root'] = fuzzing_decision_node()
        
    @staticmethod
    def __trace_node(search_tree,node_id) :
        key_list = search_tree.keys()
        
        for key_index in key_list :
            if not key_index == node_id :
                continue
                
            return search_tree[key_index]
            
        for key_index in key_list :
            result = fuzzing_decision_tree.__trace_node(search_tree[key_index],node_id)
            
            if not None == result :
                return result
            
        return None
        
    def is_exist_node(self,node_id) :
        node = fuzzing_decision_tree.__trace_node(self.tree,node_id)
        
        if not None == node :
            return True
        
        return False
        
    def get_node_data(self,node_id) :
        node = fuzzing_decision_tree.__trace_node(self.tree,node_id)
        
        if not None == node :
            return node.get_node_data()
        
        return False
        
    def add_node(self,new_node_id,old_node_id = 'root') :
        if self.is_exist_node(new_node_id) :
            return
        
        node = fuzzing_decision_tree.__trace_node(self.tree,old_node_id)
        
        if not None == node :
            node[new_node_id] = fuzzing_decision_node()
    
    def add_node_data(self,node_id,node_data) :
        node = fuzzing_decision_tree.__trace_node(self.tree,node_id)
        
        if not None == node :
            node.add_node_data(node_data)
            
    def print_node(self) :
        print(json.dumps(self.tree,indent = 2))
        
    def make_payload(self,node = None) :
        payload = b''
        
        if None == node :
            node = self.tree['root']
        
        node_data = node.get_node_data()
        
        if len(node_data) :
            data = random.choice(node_data)
            
            payload += data
        
        sub_node = node.keys()
        
        if len(sub_node) :
            payload += self.make_payload(node[random.choice(sub_node)])
        
        return payload
        
    
def make_char_list() :
    char_list = []
    
    for index in range(ord('A'),ord('Z') + 1) :
        char_list.append(chr(index))
        
    #for index in range(ord('a'),ord('z') + 1) :
    #    char_list.append(chr(index))
          
    #for index in range(ord('0'),ord('9') + 1) :
    #    char_list.append(chr(index))
          
    char_list.append('!')
    char_list.append('?')
    
    return char_list
    
def make_string(length = random.randint(0,512)) :
    char_list = make_char_list()
    string = b''
    
    for index in range(length) :
        string += random.choice(char_list)
        
    return string
    
def fuzzing_input(fuzzing_function,fuzzing_data_length = 32) :
    decision_tree = fuzzing_decision_tree()
    
    fuzzing_index = 0
    
    while fuzzing_index < 7 :#for index in range(20000) :
        buffer = fuzzing_buffer(make_string(fuzzing_data_length))
        
        #buffer = fuzzing_buffer(b'MZ\x01\x00\x0C\x00!That is True')
        #buffer = fuzzing_buffer(b'MZ\x01\x00\x0C\x00?PM')
        result = fuzzing_function(buffer)

        record_list = buffer.get_record()
        record_list_length = len(record_list)

        for index in range(record_list_length) :
            node_name = record_list[index][-1]
            node_data_index = record_list[index][1]
            node_data = buffer[node_data_index]

            if not decision_tree.is_exist_node(node_name) :
                print('Found New Path :',node_name)

                if 0 == index :
                    decision_tree.add_node(node_name)
                else :
                    decision_tree.add_node(node_name,record_list[index - 1][2])

                fuzzing_index += 1

            if not -1 == node_name.find('if') :
                if index + 1 >= record_list_length :
                    continue

                next_node_name = record_list[index][-1]
                next_node_data_index = record_list[index][1]
                next_node_data = buffer[next_node_data_index]

                #print '  Test:',node_name,next_node_data_index,next_node_data

                decision_tree.add_node_data(node_name,next_node_data)
            else :
                #print '  Test:',node_name,node_data

                decision_tree.add_node_data(node_name,node_data)
            
    decision_tree.print_node()
    
    #for index in range(10) :
    print('Payload :' , decision_tree.make_payload())
    
    
def test_function2(buffer) :
    b = []
    
    if len(buffer) > 4 :
        return
    
    for i in buffer[0:3]:
        b.append(i*3)
        b.append(chr(ord(i)+1))

    c = ''.join(b)
    
    return c
    
def test_function3(buffer) :
    upnet_ret = buffer
    session_len = ord(upnet_ret[22])
    session = upnet_ret[23:session_len + 23]
    message_len = ord(upnet_ret[session_len + 30])
    message = upnet_ret[session_len + 31:message_len + session_len + 31]
    
def decrypt(buffer) :
    output_buffer = ''
    
    for index in range(len(buffer)) :
        output_buffer += chr(ord(buffer[index]) ^ (index % 255))
        
    return output_buffer
    
def test_function(buffer) :
    if not buffer[:2] == b'MZ' :
        return False
    
    version = buffer[2:4]
    key_length = ord(buffer[5]) * 255 + ord(buffer[4])
    
    if '!' == buffer[6] :
        key = decrypt(buffer[7:key_length])

        if key == 'That' :
            return True
        
    if '?' == buffer[6] :
        if buffer[7:9] == 'PM' :
            return True
    
    return False

    
if __name__ == '__main__' :
    fuzzing_input(test_function)
    #fuzzing_input(test_function2,random.randint(0,8))
    #fuzzing_input(test_function3,512)
