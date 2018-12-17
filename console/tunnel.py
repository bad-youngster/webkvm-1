import logging
import os
import signal
import socket
from functools import reduce


class Tunnel(object):
    def __init__(self):
        self.outfd = None
        self.errfd = None
        self.pid = None

    def open(self,connhost,connuser,connport,gaddr,gport,gsocket):
        if self.outfd is not None:
            return  -1

        #ssh cmd
        argv = ["ssh","ssh"]
        if connport:
            argv += ["-p",str(connport)]

        if connuser:
            argv += ['-l',connuser]

         # shell script to detect close vnc tunnel
        if gsocket:
            nc_params = "-U %s" % gsocket
        else:
            nc_params = "%s %s" % (gaddr,gport)

        nc_cmd = (
            """nc -q 2>&1 | grep "requires an argument" > /dev/null;"""
            """if [$? -eq 0] ; then"""
            """    CMD="nc -q 0 %(nc_params)s";"""
            """else"""
            """    CMD="nc %(nc_params)s";"""
            """fi;"""
            """eval "$CMD";""" %
            {'nc_params': nc_params}
        )

        argv.append("sh -c")
        argv.append("'%s'" % nc_params)

        argv_str = reduce(lambda x,y: x + " " +y,argv[1:])
        logging.debug("Creating SSH tunnel: %s",argv_str)

        fds = socket.socketpair()
        errorfds = socket.socketpair()

        pid = os.fork()

        if pid == 0:
            fds[0].close()
            errorfds[0].close()

            os.close(0)
            os.close(1)
            os.close(2)
            os.dup(fds[1].fileno())
            os.dup(fds[1].fileno())
            os.dup(errorfds[1].fileno())
            os.execle(*argv)
            os._exit(1)

        else:
            fds[1].close()
            errorfds[1].close()

        logging.debug("Tunnel PID=%d OUTFD=%d ERRFD=%d",
                      pid,fds[0].fileno(),errorfds[0].fileno())
        errorfds[0].setblocking(0)

        self.outfd = fds[0]
        self.errfd = errorfds[0]
        self.pid = pid

        fd = fds[0].fileno()
        if fd < 0:
            raise SystemError("con't open a new tunnel: fd=%d" % fd)
        return fd

    def close(self):
        if self.outfd is None:
            return

        logging.debug("Shuting down tunnel PID=%d OUTFD=%d ERRPD=%d",
                      self.pid,self.outfd.fileno(),
                      self.errfd.fileno())
        self.outfd.close()
        self.outfd = None
        self.errfd.close()
        self.errfd = None

        os.kill(self.pid,signal.SIGKILL)
        self.pid = None


    def get_err_output(self):
        errout = " "
        while True:
            try:
                new = self.errfd.recv(1024)
            except:
                break

            if not new:
                break

            errout += new

        return errout
