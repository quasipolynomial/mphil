import os
import subprocess
import timeit


class ProcessHandler(object):
    def run_command(self, command):
        """
        Run a command and return list
        :param command: 
        :return: 
        """
        p = os.popen(command, "r")
        out = []
        while 1:
            line = p.readline()
            if not line:
                break
            out.append(line.rstrip())
        return out

    def open_process(self, command):
        """
        Return a subprocess object
        :param command: 
        :return: 
        """
        process = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process

    def run_process(self, command, inputs):
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        outputs = []
        for input in inputs:
            print inputs
            outputs.append(process.stdin.write(input))
        print process.stdout
        return outputs,

    def run_function_timed(self, f, args, **kwargs):
        # print args
        start = timeit.default_timer()
        ret = f(*args)
        time = timeit.default_timer() - start
        if kwargs.get("return_args"):
            return time, ret
        return time
