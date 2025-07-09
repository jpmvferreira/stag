# global imports
from fuse import FUSE, FuseOSError, Operations
import multiprocessing
import tempfile
import sqlite3
import shutil
import time
import os

# local imports
import stag

class TestStag:
    # ---------------------------------------------------------------------------------------------------------------
    # Auxiliary functions
    # ---------------------------------------------------------------------------------------------------------------

    # create a stag repository, should be used before each test
    def __create_stag(self):
        # create directories
        tmpdir = tempfile.mkdtemp()
        src = f"{tmpdir}/src"
        mnt = f"{tmpdir}/mnt"
        os.mkdir(src)
        os.mkdir(mnt)

        files = f"{tmpdir}/src/files"
        os.mkdir(files)

        # create dummy files
        with open(f"{files}/berne.txt",     "w") as f: f.write("content of berne.txt")
        with open(f"{files}/castle.txt",    "w") as f: f.write("content of castle.txt")
        with open(f"{files}/fuji.txt",      "w") as f: f.write("content of fuji.txt")
        with open(f"{files}/mountains.txt", "w") as f: f.write("content of mountains.txt")
        with open(f"{files}/porto.txt",     "w") as f: f.write("content of porto.txt")
        with open(f"{files}/tallinn.txt",   "w") as f: f.write("content of tallinn.txt")
        with open(f"{files}/shirakawa.txt", "w") as f: f.write("content of shirakawa.txt")

        # create directories (tags)
        os.mkdir(f"{files}/city")
        os.mkdir(f"{files}/mountains")
        os.mkdir(f"{files}/snow")

        # create database
        db  = f"{src}/stag.sql"
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute("CREATE TABLE files(path, tags)")
        cur.execute("""
            INSERT INTO files VALUES
                ('berne.txt',     '/city//mountains/'      ),
                ('castle.txt',    '/snow//mountains/'      ),
                ('fuji.txt',      '/city//mountains/'      ),
                ('mountains.txt', '/mountains/'            ),
                ('porto.txt',     '/city/'                 ),
                ('tallinn.txt',   '/city//snow/'           ),
                ('shirakawa.txt', '/city//snow//mountains/')
        """)

        con.commit()
        con.close()

        # create filesystem object
        fs = stag.StagFS(files, db)

        return fs, tmpdir, mnt

    # mount a stag repository
    def __mount_stag(self, fs, mnt):
        p = multiprocessing.Process(target=lambda mnt: FUSE(fs, mnt, nothreads=True, foreground=True), args=(mnt,))
        p.start()
        time.sleep(0.1)  # not sure I need this or previous operation is blocking

        return p

    # unmount a stag repository, must be called before __remove_stag if there was acall to __mount_stag
    def __unmount_stag(self, p):
        p.terminate()
        p.join()

        pass

    # remove a stag repository, should be used after running each test
    def __remove_stag(self, tmpdir):
        shutil.rmtree(tmpdir)

        pass

    # ---------------------------------------------------------------------------------------------------------------
    # Tests
    # ---------------------------------------------------------------------------------------------------------------

    # list files and folders on the root directory and in a random subfolder
    def test_ls(self):
        fs, tmpdir, mnt = self.__create_stag()
        p = self.__mount_stag(fs, mnt)

        ls = os.popen(f"ls {mnt}").read()
        ls_city = os.popen(f"ls {mnt}/city").read()

        try:
            assert ls == "berne.txt\ncastle.txt\ncity\nfuji.txt\nmountains\nmountains.txt\nporto.txt\nshirakawa.txt\nsnow\ntallinn.txt\n"
            assert ls_city == "berne.txt\nfuji.txt\nmountains\nporto.txt\nshirakawa.txt\nsnow\ntallinn.txt\n"

        finally:
            self.__unmount_stag(p)
            self.__remove_stag(tmpdir)

        pass

    # create a directory (i.e. a tag)
    def test_mkdir(self):
        fs, tmpdir, mnt = self.__create_stag()
        p = self.__mount_stag(fs, mnt)

        os.system(f"mkdir {mnt}/buildings")
        ls = os.popen(f"ls {mnt}").read()

        try:
            assert "buildings" in ls

        finally:
            self.__unmount_stag(p)
            self.__remove_stag(tmpdir)

        pass

    # remove a file from the repository
    def test_rm(self):
        fs, tmpdir, mnt = self.__create_stag()
        p = self.__mount_stag(fs, mnt)

        os.system(f"rm {mnt}/fuji.txt")
        ls = os.popen(f"ls {mnt}").read()
        ls_city = os.popen(f"ls {mnt}/city").read()

        try:
            assert "fuji.txt" not in ls
            assert "fuji.txt" not in ls_city

        finally:
            self.__unmount_stag(p)
            self.__remove_stag(tmpdir)

        pass

    # remove tag(s) from file(s)
    def test_rm2(self):

        # TODO: remove some tags from a file and the check subfolders to see if its gone but still exists in the root repo

        pass

    # remove tag(s) from the repository
    def test_rmdir(self):

        # TODO: remove a tag or two from the directory, check root folder and subfolders

        pass

    # read content from file(s)
    def test_read(self):
        fs, tmpdir, mnt = self.__create_stag()
        p = self.__mount_stag(fs, mnt)

        ls = os.popen(f"ls {mnt}").read()
        ls_mountains = os.popen(f"ls {mnt}/mountains").read()

        try:
            for path in ls.split():
                if ".txt" in path:
                    assert f"content of {path}" == os.popen(f"cat {mnt}/{path}").read()

            for path in ls_mountains.split():
                if ".txt" in path:
                    assert f"content of {path}" == os.popen(f"cat {mnt}/mountains/{path}").read()

        finally:
            self.__unmount_stag(p)
            self.__remove_stag(tmpdir)

        pass

    # write new contents to an already existing file
    def test_write(self):
        fs, tmpdir, mnt = self.__create_stag()
        p = self.__mount_stag(fs, mnt)

        os.system(f"echo -n 'something totally different' > {mnt}/porto.txt")

        try:
            assert os.popen(f"cat {mnt}/porto.txt").read() == "something totally different"

        finally:
            self.__unmount_stag(p)
            self.__remove_stag(tmpdir)

        pass

    # create a new file on the repository
    def test_create(self):
        fs, tmpdir, mnt = self.__create_stag()
        p = self.__mount_stag(fs, mnt)

        os.system(f"echo -n 'content of lisbon.txt' > {mnt}/city/lisbon.txt")
        ls = os.popen(f"ls {mnt}").read()
        ls_city = os.popen(f"ls {mnt}/city").read()

        try:
            assert "lisbon.txt" in ls
            assert "lisbon.txt" in ls_city
            assert "content of lisbon.txt" == os.popen(f"cat {mnt}/lisbon.txt").read()

        finally:
            self.__unmount_stag(p)
            self.__remove_stag(tmpdir)

        pass
