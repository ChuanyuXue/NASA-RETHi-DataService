import pyapi.api as api
import time
from multiprocessing import Process, Queue

QUEUE_SIZE = 1024


def update_data(api: api.API, q: Queue):
    '''
    Receive data from data repository
    '''
    print("[1] Subprocess is working")
    while True:
        data = api.subscribe()
        q.put(data.pkt2dict())


if __name__ == '__main__':
    ## Tell the data repository what data you want
    conn = api.API(local_ip="0.0.0.0",
                   local_port=65533,
                   to_ip="127.0.0.1",
                   to_port=65531,
                   client_id=1,
                   server_id=1)
    ## I want data 3
    conn.subscribe_register(3, 0)

    print("[0] Subscribed")
    ## Queue is for communication between 2 process
    q = Queue(QUEUE_SIZE)

    ## Create a process to collect data
    p = Process(target=update_data, args=(
        conn,
        q,
    ))

    ## Start the process
    p.start()

    ## Get data here without blocking
    while True:
        if not q.empty():
            data = q.get()
            print(data)