import os
import pysftp
from bionotes import Plugin


def sftp_uploader(filename):
    sftp = pysftp.Connection(host=Plugin.getVar('FTP_HOST'),
                             port=Plugin.getVar('FTP_PORT'),
                             username=Plugin.getVar('FTP_USER'),
                             password=self.Plugin.getVar('FTP_PASSWORD'))

    with sftp.cd('upload'):
        sftp.put(filename)
