from mpi4py import MPI
from draw import draw_states

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()
operations = []


def initiator():
    for i in range(1, nprocs):
        comm.send(f'token-{i}', dest=i)
        operations.append(['send', 0, i, MPI.Wtime()])

    requests = []
    for i in range(1, nprocs):
        req = comm.irecv(source=i)
        requests.append((i, req))

    while requests:
        new_requests = []
        for i, req in requests:
            status, not_initiator_time = req.test()
            recv_time = MPI.Wtime()
            if status:
                operations.append(('recv', i, 0, not_initiator_time))
                operations.append(('send', i, 0, not_initiator_time))
                operations.append(('recv', 0, i, recv_time))
            else:
                new_requests.append((i, req))
        requests = new_requests

    operations.sort(key=lambda x: [x[3], x[2]])
    draw_states(nprocs, operations)


def not_initiator():
    comm.recv(source=0)
    recv_and_send_time = MPI.Wtime()
    comm.send(recv_and_send_time, dest=0)


if rank == 0:
    initiator()
else:
    not_initiator()
