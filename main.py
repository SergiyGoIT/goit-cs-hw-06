from multiprocessing import Process
from http_server import run_http_server
from socket_server import run_socket_server

if __name__ == "__main__":
    http_proc = Process(target=run_http_server)
    socket_proc = Process(target=run_socket_server)

    http_proc.start()
    socket_proc.start()

    http_proc.join()
    socket_proc.join()
