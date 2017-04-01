import os
import os.path
import operator
import json
from processhandler import ProcessHandler


class FileHandler(object):
    def write_to_file_simple(self, path, data):
        with open(path, 'w') as outfile:
            for datum in data:
                out = datum
                if datum != data[-1]:
                    out = out + "\n"
                outfile.write(out)

    def write_to_file(self, path, data):
        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def read_from_file(self, path, **kwargs):
        if not os.path.isfile(path):
            return False

        # First read
        with open(path, 'r') as outfile:
            data = json.load(outfile)

        # Merge multiple instances
        if kwargs.get("aggregate"):
            ph = ProcessHandler()
            directory = path.rsplit('/', 1)[:-1][0]
            filename = path.rsplit('/', 1)[-1]
            count = ph.run_command("cd {0} && ls -d *{1}* | wc -l ".format(directory, filename))[0]
            for i in range(1, int(count)):
                temp_path = "{0}_{1}".format(path, str(i))
                with open(temp_path, 'r') as outfile:
                    data_b = json.load(outfile)
                data = self.merge_data(data, data_b)

        return data

    def update_file(self, path, data):
        # Check if has space, otherwise make a new file
        if not self.has_space(path):
            ph = ProcessHandler()
            directory = path.rsplit('/', 1)[:-1][0]
            filename = path.rsplit('/', 1)[-1]
            count = ph.run_command("cd {0} && ls -d *{1}* | wc -l ".format(directory, filename))[0]
            count = str(int(count) - 1) if int(count) > 1 else count
            data = self.update_file("{0}_{1}".format(path, count), data)
            return data

        # If the file exists, grab data and merge it with this data
        elif os.path.isfile(path):
            old_data = self.read_from_file(path)
            data = self.merge_data(old_data, data)

        # Update and return data
        data.sort(key=operator.itemgetter(1))
        self.write_to_file(path, data)
        return data

    def makedir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def has_space(self, path):
        if not os.path.exists(path):
            return True
        statinfo = os.stat(path)
        size = statinfo.st_size >> 20
        return size < 20

    def merge_data(self, data_a, data_b):
        for datum1 in data_a:
            key1 = datum1[0]
            found = False
            for datum2 in data_b:
                key2 = datum2[0]
                if key1 == key2:
                    found = True
                    break
            if found == False:
                data_b.append(datum1)
        return data_b