
USER = input("Mysql username:")
PASS = input("Password:")
import subprocess

proc = subprocess.Popen(["mysql", "--user=%s" % USER, "--password=%s" % PASS, "database"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
out, err = proc.communicate(file("/setup.sql").read())
