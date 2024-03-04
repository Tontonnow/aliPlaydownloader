import os
import signal
import time
from ctypes import *
import logging


class DownloadConfig(Structure):
    _fields_ = [
        ("vid", c_char_p),
        ("playAuth", c_char_p),
        ("DownloadedFilePath", c_char_p),
        ("isDownloaded", c_bool),
        ("isDownloadedError", c_bool),
    ]

    def __init__(self):
        self.vid = None
        self.playAuth = None
        self.DownloadedFilePath = b"./download"
        self.isDownloaded = False
        self.isDownloadedError = False
        super(DownloadConfig, self).__init__()

    def __str__(self):
        return f"vid:{self.vid},playAuth:{self.playAuth},DownloadedFilePath:{self.DownloadedFilePath},isDownloaded:{self.isDownloaded},isDownloadedError:{self.isDownloadedError}"


class AliDownloader:
    def __init__(self):
        self.dllName = "./AliPlayeras.dll"
        self.dll = CDLL(self.dllName)
        self.dll.Download.argtypes = [POINTER(DownloadConfig)]
        self.dll.Download.restype = None

    def Download(self, dconfig):
        self.dll.Download(byref(dconfig))
        while True:
            if dconfig.isDownloadedError:
                logging.error("下载失败")
                # 失败会导致异常，线程无法退出，所以需要强制退出
                return False
            elif dconfig.isDownloaded:
                logging.info("下载成功")
                return True
            time.sleep(1)


if __name__ == '__main__':
    config = DownloadConfig()
    config.vid = "86af4e74e6ca4e68968f2571090f3056".encode("utf-8")
    config.playAuth = "eyJTZWN1cml0eVRva2VuIjoiQ0FJU2lBTjFxNkZ0NUIyeWZTaklyNWVFQ3V6RzNLNUQvSUdnY203b25tOFVkUForcUxEdmpEejJJSDFQZlhGdEFlMFp0LzArbVdsUTV2d2FscklxRXNRZkd4ZWRNWkVwdHNrSXJseitKb0hidk5ldTBic0hoWnY5bmExZ29aYWlqcUhvZU96Y1lJNzMwWjdQQWdtMlEwWVJySkwrY1RLOUphYk1VL21nZ29KbWFkSTZSeFN4YVNFOGF2NWRPZ3BscnIwSVZ4elBNdnIvSFJQMnVtN1pIV3R1dEEwZTgzMTQ1ZmFRejlHaTZ4YlRpM2I5ek9FVXFPYVhKNFMvUGZGb05ZWnlTZjZvd093VUVxL2R5M3hvN3hGYjFhRjRpODRpL0N2YzdQMlFDRU5BK3dtbFB2dTJpOE5vSUYxV2E3UVdJWXRncmZQeGsrWjEySmJOa0lpbDVCdFJFZHR3ZUNuRldLR216c3krYjRIUEROc2ljcXZoTUhuZ3k4MkdNb0tQMHprcGVuVUdMZ2hIQ2JGRFF6MVNjVVYxRVd1RWNmYjdvZ21TUDFqOEZQZS92ZnRvZ2NZdi9UTEI1c0dYSWxXRGViS2QzQnNETjRVMEIwRlNiRU5OaERTOEt2SlpLbFVkTGdvL1Yrek5WL2xhYUJGUHRLWFdtaUgrV3lOcDAzVkxoZnI2YXVOcGJnUHIxVVFwTlJxQUFVSnNMNDVZMVUrS0FBK296TzRvdjRQNXlndDBqejZoeUVBQmxzMmF0YWdvRG0vdmVjK0JQeksrY3plVEtuK2lsbFB2NHI3L3FpUVBSWTQ1bWVNVEVpNE9Yd0s1SjhFaXlsSTNPamxmS2xoalJMSHNqazRTYmtZK05GckViZHZrdXREWWlERHNxaDFqT21pbmNIcWY4TW5uWkRHUG5PMDN3bUp2eG9HMHlVaFdJQUE9IiwiQXV0aEluZm8iOiJ7XCJDSVwiOlwibmtjT09MZnBrK05wNDNUaHZqVzlUZEJvNjl0WldrUUNKVG02T1VYTkxqQ3JQbkYvQzhaY0hJdGdSU2kyM1Ziei9HWllENDlJNTRyV3FpVUhoU2dzTVV2UXkwUDBIWFVEVU5kWGhMQlNSTk09XCIsXCJDYWxsZXJcIjpcIm9hd3JiSjRpcnkzQk5LMDhpdDZpNW04UzVHN3RHbklsSFlvazJLTUhJelk9XCIsXCJFeHBpcmVUaW1lXCI6XCIyMDI0LTAzLTA0VDA1OjU2OjU2WlwiLFwiTWVkaWFJZFwiOlwiODZhZjRlNzRlNmNhNGU2ODk2OGYyNTcxMDkwZjMwNTZcIixcIlBsYXlEb21haW5cIjpcInYzMC41MWN0by5jb21cIixcIlNpZ25hdHVyZVwiOlwiTWFtR3YxdDFndWJBSERyZE9hbzlxTTBFcFQwPVwifSIsIlZpZGVvTWV0YSI6eyJTdGF0dXMiOiJOb3JtYWwiLCJWaWRlb0lkIjoiODZhZjRlNzRlNmNhNGU2ODk2OGYyNTcxMDkwZjMwNTYiLCJUaXRsZSI6IjQ3LUdvIOaTjeS9nFJlZGlz5a6e5oiY77yNSGFzaOaTjeS9nOeUqOaIt+eUu+WDj+W6lOeUqDEiLCJDb3ZlclVSTCI6Imh0dHBzOi8vdjMwLjUxY3RvLmNvbS84NmFmNGU3NGU2Y2E0ZTY4OTY4ZjI1NzEwOTBmMzA1Ni9zbmFwc2hvdHMvNjEyZTdlYzg5YmY3NGU1OWFmN2RkODQ4MmFiOTU0ZTItMDAwMDUuanBnIiwiRHVyYXRpb24iOjM0OS4wfSwiQWNjZXNzS2V5SWQiOiJTVFMuTlQxQVZyMXFiS0NLcEhZem9BeHlSR3VEbiIsIlBsYXlEb21haW4iOiJ2MzAuNTFjdG8uY29tIiwiQWNjZXNzS2V5U2VjcmV0IjoiRG1pRDg4RWJqNlJERDNCSGNhUjRxQmRMZ0pxc05ZanNXU1AyNlpUYngzd2kiLCJSZWdpb24iOiJjbi1zaGFuZ2hhaSIsIkN1c3RvbWVySWQiOjExMzI2MzE0MjEwNTc3Nzd9".encode()
    downloader = AliDownloader()
    d=downloader.Download(config)
    if not d:
        os.kill(os.getpid(), signal.SIGTERM)
