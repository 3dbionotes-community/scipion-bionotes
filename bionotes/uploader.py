import pysftp


class FileUploader():

    FTP_HOST = "campins.cnb.csic.es"
    FTP_PORT = "22722"
    FTP_USER = "scipion"
    FTP_PASSWORD = "change.me"

    def file_uploader():
        pass

    def sftp_uploader(self, filename):
        srv = pysftp.Connection(host=self.FTP_HOST, port=self.FTP_PORT,
                                username=self.FTP_USER,
                                password=self.FTP_PASSWORD)

        srv.cd('upload')
        srv.put(filename)
        with srv.cd('upload'):
            srv.put(filename)
