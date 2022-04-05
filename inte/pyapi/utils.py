"""
Basic utilities for the API

Author:
    Jiachen Wang
    Chuanyue Xue
    Murali Krishnan Rajasekharan Pillai

Date:
    01.18.2022
"""

from calendar import c
from ctypes import *
from curses.ascii import SUB

HEADER_LEN = 24
SERVICE_HEADER_LEN = 6
SUB_HEADER_LEN = 8


class Header(LittleEndianStructure):
    _fields_ = [
        ("src", c_uint8),
        ("dst", c_uint8),
        ("type_prio", c_uint8),
        ("ver_res", c_uint8),
        ("physical_time", c_uint32),
        ("simulink_time", c_uint32),
        ("sequence", c_uint16),
        ("length", c_uint16),
        ("service", c_uint8),
        ("flag", c_uint8),
        ("option1", c_uint8),
        ("option2", c_uint8),
        ("subframe_num", c_uint16),
    ]


class SubHeader(LittleEndianStructure):
    _field_ = [
        ("data_id", c_uint16),
        ("time_diff", c_uint16),
        ("row", c_uint8),
        ("col", c_uint8),
        ("length", c_uint16),
    ]


class SubPacket:

    def __init__(self, _data_id, _time_diff, _row, _col, _length, _payload):
        self.header = SubHeader(
            _data_id,
            _time_diff,
            _row,
            _col,
            _length,
        )
        self.payload = _payload

    def pkt2Buf(self, _data_id, _time_diff, _row, _col, _length, _payload):
        header_buf = SubHeader(
            _data_id,
            _time_diff,
            _row,
            _col,
            _length,
        )
        double_arr = c_double * _length
        payload_buf = double_arr(*_payload)
        buf = bytes(header_buf) + bytes(payload_buf)
        return buf

    def buf2Pkt(self, buffer):
        self.header = SubHeader.from_buffer_copy(buffer[:SUB_HEADER_LEN])
        double_arr = c_double * self.header.length
        self.payload = double_arr.from_buffer_copy(
            buffer[SUB_HEADER_LEN:SUB_HEADER_LEN + 8 * self.header.length])
        return (self.header._fields_, SUB_HEADER_LEN + 8 * self.header.length)


class Packet:

    def __init__(self, _src, _dst, _type, _prio, _version, _reserved,
                 _physical_time, _simulink_time, _sequence, _length, _service,
                 _flag, _option1, _option2, _subframe_num, _subpackets):
        _type_prio = _type << 4 + _prio
        _ver_res = _version << 4 + _reserved
        self.header = Header(_src, _dst, _type_prio, _ver_res, _version,
                             _reserved, _physical_time, _simulink_time,
                             _sequence, _length, _service, _flag, _option1,
                             _option2, _subframe_num)
        self.subpackets = _subpackets

    # payload is a double list
    def pkt2Buf(self, _src, _dst, _type, _prio, _version, _reserved,
                _physical_time, _simulink_time, _sequence, _length, _service,
                _flag, _option1, _option2, _subframe_num, _subpackets):

        _type_prio = _type << 4 + _prio
        _ver_res = _version << 4 + _reserved
        header_buf = Header(_src, _dst, _type_prio, _ver_res, _version,
                            _reserved, _physical_time, _simulink_time,
                            _sequence, _length, _service, _flag, _option1,
                            _option2, _subframe_num)
        buf = bytes(header_buf)

        for subpkt in _subpackets:
            buf += subpkt.pkt2Buf()

        return buf

    def buf2Pkt(self, buffer):
        self.header = Header.from_buffer_copy(buffer[:HEADER_LEN +
                                                     SERVICE_HEADER_LEN])
        self.subpackets = []
        index = HEADER_LEN + SERVICE_HEADER_LEN

        for i in self.subframe_num:
            subpkt = SubPacket()
            _, index = subpkt.buf2Pkt(buffer[index:])
            self.subpackets.append(subpkt)

        return (self.header._fields_, index)


if __name__ == '__main__':
    subpkt = SubPacket(150, 0, 3, 1, 3, [1, 2, 3])
    subpkt2 = SubPacket(151, 0, 2, 2, 4, [1, 2, 3.5])

    pkt = Packet(0, 1, 0, 4, 0, 0, 123456, 654312, 0, 15, 0, 0, 0, 0, 2,
                 [subpkt, subpkt2])

    buff = pkt.pkt2Buf()

    pkt = pkt.buf2Pkt(buff)
    print(pkt)
