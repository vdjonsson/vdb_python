import subprocess
import sys
import os
import pty

# paths required by VariantDatabase class
vdbPath = "/Users/apw/Downloads/latest7/vdb"
stdbufPath = "/Users/apw/Downloads/latest7/stdbuf"
workingDirectory = "/Users/apw/Downloads/latest7"

# singleton class for interacting with Variant Database
class VariantDatabase(object):

    # initializes vdb on first call
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(VariantDatabase, self).__new__(self)
            input_buffer = sys.stdin
            output_buffer = sys.stdout
            self.stdout_primary_fd, self.stdout_secondary_fd = pty.openpty()
            self.proc = subprocess.Popen([stdbufPath,"-o0",vdbPath],
                            stdin=subprocess.PIPE,            # for vdb input
                            stdout=self.stdout_secondary_fd,  # for vdb output
                            cwd=workingDirectory,
                            universal_newlines=True,
                            bufsize=0)
            print("Starting vdb...")
            loadingOutput = self.command(self,"",init=True)
            for x in range(len(loadingOutput)):
                if loadingOutput[x] == "E" and loadingOutput[x+1] == "n" and loadingOutput[x+2] == "t":
                    break
            loadingOutput = loadingOutput[:x-5]
            print(loadingOutput)
            self.command(self,"displayTextWithColor off")
            self.command(self,"paging off")
            self.command(self,"quiet on")
        return self.instance

    # executes vdb command and returns output in a string
    def command(self,command,init=False):
        if not init:
            print(command, file=self.proc.stdin, flush=True)
        output = bytes()
        foundVDB = False
        while True:
            output += os.read(self.stdout_primary_fd, 10000)
            for x1 in range(len(output)):
                if output[x1] == 10:    # linefeed
                    break
            for x2 in range(len(output)):
                if output[x2] == 118 and output[x2+1] == 100 and output[x2+2] == 98 and output[x2+3] == 62:  # "vdb>"
                    foundVDB = True
                    break
            if foundVDB:
                break
        trimmed = output[x1+1:x2-1]
        return trimmed.decode("utf-8")
# end of VariantDatabase class


# demo testing VariantDatabase class
commands = ["x = ca","y = lineages x","save y -"]
for command in commands:
    output = VariantDatabase().command(command)
    truncatedOutput = (output[:300] + "...") if len(output) > 300 else output
    print("\nOutput from command \""+command+"\":"+truncatedOutput)

