#! /usr/bin/env python3.6
import sys
import os
import shutil
import time
import signal
from .helper import restoreDirectory
from .helper import printReturnOutput
from . import constants

@restoreDirectory
def runExecutable():
    print("performing basic functionality test on func...")
    # 1. check the version output
    # TODO print output as well as test for version
    print("verify func...")
    output = printReturnOutput(constants.CMD)
    assert(f"Azure Functions Core Tools ({constants.VERSION})" in output)
    # make sure command used in this test scripts are presented in the help
    assert("init " in output)
    assert("new " in output)
    assert("start " in output)

    # 2. test ability to create function
    os.chdir(constants.TESTFOLDER)

    # 2.1 func init
    print("verfiy func init...")
    output = printReturnOutput(
        [constants.CMD, "init", "--worker-runtime", "dotnet"])
    assert("was created successfully" in output)
    assert(os.path.exists("host.json"))
    assert(os.path.exists("test.csproj"))

    # 2.2 func new
    functionName = "dummyHttp"
    print("verify func new...")
    # test csx since its scripting language, does not require additional runtimes
    output = printReturnOutput(
        [constants.CMD, "new", "--csx", "-t", "Http Trigger", "-n", functionName])
    assert(os.path.exists(os.path.join(functionName,"run.csx")))
    # 2.3 func start
    # print("verify func start...")
    # popen = subprocess.Popen([CMD, "start", "--build"],
    #                          stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    # # FIXME
    # # wait a bit, then send control-c as suggested
    # time.sleep(10)
    # popen.send_signal(signal.SIGINT)
    # stdout = popen.stdout.read()
    # assert(f"{testFolder}.{functionName}.Run" in stdout)
    # assert("Generating 1 job function(s)" in stdout)
    # assert(f"{functionName}: http://localhost:7071/api/{functionName}" in stdout)

    return True
