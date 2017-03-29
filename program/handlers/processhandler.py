import os
import subprocess

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
