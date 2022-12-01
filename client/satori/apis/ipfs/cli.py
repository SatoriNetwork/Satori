'''
uses the cli to add a file to ipfs

on program start:
# in a separate thread
ipfs.start

on new observation, or publication:
cid = ipfs.addAndPinDirectoryByCLI(abspath, name)
# send cid to server

on closing a subscription:
cid = ipfs.addAndPinDirectoryByCLI(abspath, name)
ipfs.removeDirectoryByCLI(name)
# remvoe cid from server
'''

import subprocess


class IpfsCli(object):
    def __init__(self, *args):
        super(IpfsCli, self).__init__(*args)
        self.setIpfs()
        self.setVersion()

    def run(self, cmd, ipfs=None):
        return subprocess.run(["powershell", "-Command", (ipfs or self.ipfs) + cmd], capture_output=True).stdout.decode('utf-8').strip()

    def setIpfs(self):
        self.ipfs = self.findOrInstallIpfs()

    def findOrInstallIpfs(self):
        x = self.findIpfs()
        if x is None:
            self.setVersion()
            if self.version == '':
                raise Exception('ipfs not found, and unable to install')
            else:
                x = self.findIpfs()
                if x is None:
                    raise Exception('please install ipfs')
        return x

    def findIpfs(self):
        '''if ipfs is not found in path, look for it in the program directory'''
        for loc in [r'ipfs ', r'~\Apps\kubo_v0.17.0\kubo\ipfs.exe ']:
            if self.run(ipfs=loc, cmd='--version') != '':
                return loc
        return None

    def getVersion(self):
        x = self.run('--version')
        if x == '':
            return None
        return x

    def setVersion(self):
        self.version = self.getVersion() or self.installIpfs()

    def installIpfs(self):
        return self.run(
            r'cd ~\;'
            r'wget https://dist.ipfs.tech/kubo/v0.17.0/kubo_v0.17.0_windows-amd64.zip -Outfile kubo_v0.17.0.zip;'
            r'Expand-Archive -Path kubo_v0.17.0.zip -DestinationPath ~\Apps\kubo_v0.17.0;'
            r'cd ~\Apps\kubo_v0.17.0\kubo;'
            r'.\ipfs.exe --version;')

    def addIpfsToPath(self):
        return self.run(
            r'cd ~\Apps\kubo_v0.17.0\kubo;'
            r'$GO_IPFS_LOCATION = pwd;'
            r'if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force };'
            r'notepad $PROFILE;'
            r'''Add-Content $PROFILE "`n[System.Environment]::SetEnvironmentVariable('PATH',`$Env:PATH+';;$GO_IPFS_LOCATION')";'''
            r'& $profile;'
            r'ipfs --version;')

    def addDirectoryByCLI(self, abspath: str):
        '''all attempts to use the api for this ended in disaster.'''
        return self.run(f'add -r -Q {abspath}')

    def pinDirectoryByCLI(self, cid: str, name: str):
        return self.run(f'files cp /ipfs/{cid} /{name}')

    def pinAndAddDirectoryByCLI(self, abspath: str, name: str):
        return self.run(f'files cp /ipfs/$(ipfs add -r -Q {abspath}) /{name}')

    def init(self, ):
        return self.run(f'init')

    def daemon(self, ):
        ''' run this in a separate thread '''
        return self.run(f'daemon')

    ## interface ##################################################################

    def start(self):
        ''' run this in a separate thread '''
        self.init()
        self.daemon()

    def addAndPinDirectoryByCLI(self, abspath: str, name: str):
        cid = self.addDirectoryByCLI(abspath)
        self.pinDirectoryByCLI(cid, name)
        return cid

    def seeMFSByCLI(self):
        return self.run(f'files ls')

    def removeDirectoryByCLI(self, name: str):
        return self.run(f'files rm -r /{name}')
