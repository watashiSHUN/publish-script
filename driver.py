#! /usr/bin/env python3.6
import platform
import sys
import os
import shutil
from shared import constants
from shared.helper import getUserConfirm
# 1. build package
# { 2. clean install
#   3. test executable
#   4. uninstall }  => all part of testing

def main(*args):
    # assume follow semantic versioning 2.0.0
    constants.VERSION = args[1]
    constants.DRIVERROOTDIR = os.path.dirname(os.path.abspath(__file__))
    platformSystem = platform.system()
    if platformSystem == "Linux":
        d, _, __ = platform.linux_distribution()
        if d == "Ubuntu":
            import ubuntu.bulidDEB as dist
            print("detect Ubuntu, start working on deb package")
        elif d == "Fedora":
            import fedora.buildRPM as dist
            print("detect Fedora, start working on rpm package")
        else:
            print(f"does not support distribution {d} yet")
            return
    elif platformSystem == "Windows":
        import chocolatey.buildNUPKG as dist
        print("detect Windows, start working on nupkg pacakge")
    else:
        print(f"does not support platform {platformSystem} yet")
        return

    # at root
    initWorkingDir(constants.BUILDFOLDER, True)
    initWorkingDir(constants.ARTIFACTFOLDER)

    # 1. build package
    if getUserConfirm("building package"):
        dist.preparePackage()

    def verifyPackage():
        initWorkingDir(constants.TESTFOLDER, True)
        # 2. clean install
        # TODO usually require sudo or administrator privilege
        print("trying to install package")
        dist.installPackage()
        # 3. test executable
        from shared import runTest
        print("trying to run tests")
        assert(runTest.runExecutable())
        # 4. uninstall
        print("trying to uninstall package")
        dist.uninstallPackage()
    
    if getUserConfirm("test pacakge with actual install"):
        verifyPackage()

    if getUserConfirm("publish package online"):
        dist.publish()


def initWorkingDir(dirName, clean = False):
    if clean:
        if os.path.exists(dirName):
            print(f"trying to clear {dirName}/ directory")
            shutil.rmtree(dirName)
    print(f"trying to create {dirName}/ directory")
    os.makedirs(dirName, exist_ok=True)

if __name__ == "__main__":
    # input example: 2.0.1-beta.25
    main(*sys.argv)
