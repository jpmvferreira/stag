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
    # Tests on filesystem methods
    # ---------------------------------------------------------------------------------------------------------------

    #def test_access(self):
    #    pass

    #def test_chmod(self):
    #    pass

    #def test_chown(self):
    #    pass

    #def test_getattr(self):
    #    pass

    #def test_rename(self):
    #    pass

    #def test_statfs(self):
    #    pass

    #def test_symlink(self):
    #    pass

    #def test_unlink(self):
    #    pass

    #def test_utimens(self):
    #    pass

    # ---------------------------------------------------------------------------------------------------------------
    # Tests on folder methods
    # ---------------------------------------------------------------------------------------------------------------

    #def test_mkdir(self):
    #    pass

    #def test_readdir(self):
    #    pass

    #def test_rmdir(self):
    #    pass

    # ---------------------------------------------------------------------------------------------------------------
    # Tests on file methods
    # ---------------------------------------------------------------------------------------------------------------

    #def test_file1(self):
    #    pass

    # ---------------------------------------------------------------------------------------------------------------
    # Tests using terminal utilities
    # ---------------------------------------------------------------------------------------------------------------

    def test_cli1(self):
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
