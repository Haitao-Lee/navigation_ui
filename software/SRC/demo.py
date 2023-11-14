import base64
import json
import socket
import struct
import time


class SophiarApi:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.s.connect((host, port))
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def send_message(self, msg):
        len_bin = struct.pack('!H', len(msg))
        packet = len_bin + msg
        self.s.send(packet)

    def send_command(self, cmd):
        self.send_message(bytes(cmd, 'ascii'))

    def receive_message(self):
        len_bin = self.s.recv(2)
        length = struct.unpack('!H', len_bin)[0]
        reply_bin = self.s.recv(length)
        return reply_bin

    def receive_reply(self):
        reply_bin = self.receive_message()
        reply = reply_bin.decode('ascii')
        return reply.split(',')


class SophiarVariableIO:
    def __init__(self, host, port):
        self.api = SophiarApi(host, port)
        self.var_index_map = {}
        self.var_name_map = {}

    @staticmethod
    def pack_variable(var_type, val):
        if val is None:
            return bytes()
        if var_type == 'bool_obj':
            return struct.pack('?', val)
        elif var_type == 'u64int_obj':
            return struct.pack('!Q', val)
        elif var_type == 'double_obj':
            return struct.pack('!d', val)
        elif var_type == 'scalarxyz_obj':
            return struct.pack('!ddd', *val)

    @staticmethod
    def unpack_variable(var_type, val_bin):
        if len(val_bin) == 0:
            return None
        if var_type == 'bool_obj':
            return struct.unpack('?', val_bin)[0]
        elif var_type == 'u64int_obj':
            return struct.unpack('!Q', val_bin)[0]
        elif var_type == 'double_obj':
            return struct.unpack('!d', val_bin)[0]
        elif var_type == 'scalarxyz_obj':
            return struct.unpack('!ddd', val_bin)

    def config(self, cmd, var_list):
        var_name_list = [var_info['name'] for var_info in var_list]
        self.api.send_command(f'{cmd} {",".join(var_name_list)}')
        reply = self.api.receive_reply()
        var_index_list = [int(index_str) for index_str in reply]
        for var_info in zip(var_index_list, var_list):
            var_index = var_info[0]
            var_name = var_info[1]['name']
            var_type = var_info[1]['type']
            self.var_index_map[var_index] = {'name': var_name, 'type': var_type}
            self.var_name_map[var_name] = {'index': var_index, 'type': var_type}

    def config_as_input(self, var_list):
        self.config('VARINB', var_list)

    def config_as_output(self, var_list):
        self.config('VAROUTB', var_list)

    def update_variable(self, var_list):
        msg = bytes()
        for var_info in var_list:
            var_name = var_info['name']
            var_index = self.var_name_map[var_name]['index']
            var_type = self.var_name_map[var_name]['type']
            var_bin = self.pack_variable(var_type, var_info['value'])
            prefix_bin = struct.pack('!HB', var_index, len(var_bin))
            msg += prefix_bin + var_bin
        self.api.send_message(msg)

    def receive_update(self):
        msg = self.api.receive_message()
        ret = []
        while len(msg) != 0:
            var_index, val_size = struct.unpack('!HB', msg[:3])
            msg = msg[3:]
            var_type = self.var_index_map[var_index]['type']
            var_name = self.var_index_map[var_index]['name']
            var_val = self.unpack_variable(var_type, msg[:val_size])
            msg = msg[val_size:]
            ret.append({'name': var_name, 'value': var_val})
        return ret


class SophiarController:
    def __init__(self, host, port):
        self.api = SophiarApi(host, port)

    def init_objs(self, obj_name_list):
        self.api.send_command(f'INIT {",".join(obj_name_list)}')
        return self.api.receive_reply()

    def start_objs(self, obj_name_list):
        self.api.send_command(f'START {",".join(obj_name_list)}')
        return self.api.receive_reply()

    def stop_objs(self, obj_name_list):
        self.api.send_command(f'STOP {",".join(obj_name_list)}')
        return self.api.receive_reply()

    def reset_objs(self, obj_name_list):
        self.api.send_command(f'RESET {",".join(obj_name_list)}')
        return self.api.receive_reply()

    @staticmethod
    def encode_patch(patch):
        return base64.b64encode(json.dumps(patch).encode('ascii')).decode('ascii')

    def patch_init_config(self, obj_name, patch):
        self.api.send_command(f'INITCONF {obj_name},{self.encode_patch(patch)}')
        return self.api.receive_reply()

    def patch_start_config(self, obj_name, patch):
        self.api.send_command(f'STARTCONF {obj_name},{self.encode_patch(patch)}')
        return self.api.receive_reply()


# if __name__ == '__main__':
#     api = SophiarController('127.0.0.1', 5277)
#     print(api.start_objs(['all']))
#
#     time.sleep(1)
#
#     _var_list = [{
#         'name': 'var_bool',
#         'type': 'bool_obj',
#     }, {
#         'name': 'var_num',
#         'type': 'u64int_obj',
#     }, {
#         'name': 'var_float',
#         'type': 'double_obj'
#     }, {
#         'name': 'var_vec',
#         'type': 'scalarxyz_obj'
#     }]
#
#     var_output = SophiarVariableIO('127.0.0.1', 5278)
#     var_output.config_as_output(_var_list)
#     print(var_output.var_name_map)
#     print(var_output.receive_update())
#
#     time.sleep(1)
#
#     var_input = SophiarVariableIO('127.0.0.1', 5278)
#     var_input.config_as_input(_var_list)
#
#     update_list = [{
#         'name': 'var_bool',
#         'value': False
#     }, {
#         'name': 'var_num',
#         'value': 87654321
#     }, {
#         'name': 'var_float',
#         'value': 5678.1234
#     }, {
#         'name': 'var_vec',
#         'value': (3.0, 2.0, 15.0)
#     }]
#     var_input.update_variable(update_list)
#
#     time.sleep(1)
#
#     print(var_output.receive_update())

# if __name__ == '__main__':
#     api = SophiarController('127.0.0.1', 5277)
#     print(api.start_objs(['proxy', 'target']))
#
#     time.sleep(5)
#
#     print(api.stop_objs(['proxy']))
#     print(api.patch_start_config('proxy', {'start_value': 5000}))
#     print(api.start_objs(['proxy']))
#
#     time.sleep(5)
#
#     print(api.stop_objs(['source']))
#     print(api.patch_start_config('proxy', {'start_value': 2000}))
#     print(api.patch_start_config('source', {'start_value': 0}))
#     print(api.start_objs(['proxy']))

if __name__ == '__main__':
    api = SophiarController('127.0.0.1', 5277)
    print(api.start_objs(['all']))

    time.sleep(1)

    _var_list = [{
        'name': 'var_num',
        'type': 'u64int_obj',
    }, {
        'name': 'var_float',
        'type': 'double_obj'
    }]

    var_output = SophiarVariableIO('127.0.0.1', 5278)
    var_output.config_as_output(_var_list)
    var_output.receive_update()

    var_input = SophiarVariableIO('127.0.0.1', 5278)
    var_input.config_as_input(_var_list)

    start_ts = time.perf_counter()
    for i in range(10000):
        var_input.update_variable([{'name': 'var_num', 'value': i},
                                   {'name': 'var_float', 'value': i}])
        _reply = var_output.receive_update()
        assert len(_reply) == 2
        assert _reply[0]['value'] == i
    print(time.perf_counter() - start_ts)

# if __name__ == '__main__':
#     api = SophiarController('127.0.0.1', 5277)
#     print(api.start_objs(['tracker_all']))
#     # print(api.start_objs(['reg_model']))
#
#     # print(api.stop_objs(['probe_tip_transformer_for_model_ref']))
#     # print(api.start_objs(['test_reg']))
