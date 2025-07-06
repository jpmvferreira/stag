# global imports
import tempfile
import sqlite3
import shutil
import os

# local imports
import stag

class TestStag:
    # ---------------------------------------------------------------------------------------------------------------
    # Auxiliary functions
    # ---------------------------------------------------------------------------------------------------------------

    # setup a stag repository for each test
    def __setup_stag(self):
        # create directories
        tmpdir = tempfile.mkdtemp()
        src = f"{tmpdir}/src"
        mnt = f"{tmpdir}/mnt"
        os.mkdir(src)
        os.mkdir(mnt)

        files = f"{tmpdir}/src/files"
        os.mkdir(files)

        # create dummy files
        with open(f"{files}/berne.txt",     "w") as f: f.write("berne.txt")
        with open(f"{files}/castle.txt",    "w") as f: f.write("castle.txt")
        with open(f"{files}/fuji.txt",      "w") as f: f.write("fuji.txt")
        with open(f"{files}/mountains.txt", "w") as f: f.write("mountains.txt")
        with open(f"{files}/porto.txt",     "w") as f: f.write("porto.txt")
        with open(f"{files}/tallinn.txt",   "w") as f: f.write("tallinn.txt")
        with open(f"{files}/shirakawa.txt", "w") as f: f.write("shirakawa.txt")

        # create database
        db  = f"{src}/stag.sql"
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute("CREATE TABLE files(path, tags)")
        cur.execute("""
            INSERT INTO files VALUES
                ('berne.jpg',     '/city//mountains/'      ),
                ('castle.jpg',    '/snow//mountains/'      ),
                ('fuji.jpg',      '/city//mountains/'      ),
                ('mountains.jpg', '/mountains/'            ),
                ('porto.jpg',     '/city/'                 ),
                ('tallinn.jpg',   '/city//snow/'           ),
                ('shirakawa.jpg', '/city//snow//mountains/')
        """)

        con.commit()
        con.close()

        # create filesystem object
        fs = stag.StagFS(files, db)

        return fs, tmpdir

    # cleanup the mock stag repository after running each test
    def __clean_stag(self, tmpdir):
        shutil.rmtree(tmpdir)

        pass

    # ---------------------------------------------------------------------------------------------------------------
    # Tests on filesystem methods
    # ---------------------------------------------------------------------------------------------------------------

    def test_access(self):
        fs, tmpdir = self.__setup_stag()
        self.__clean_stag(tmpdir)

        pass

    def test_chmod(self):
        pass

    def test_chown(self):
        pass

    def test_getattr(self):
        pass

    def test_rename(self):
        pass

    def test_statfs(self):
        pass

    def test_symlink(self):
        pass

    def test_unlink(self):
        pass

    def test_utimens(self):
        pass

    # ---------------------------------------------------------------------------------------------------------------
    # Tests on folder methods
    # ---------------------------------------------------------------------------------------------------------------

    def test_mkdir(self):
        pass

    def test_readdir(self):
        pass

    def test_rmdir(self):
        pass

    # ---------------------------------------------------------------------------------------------------------------
    # Tests on file methods
    # ---------------------------------------------------------------------------------------------------------------

    # criar um test que testa varias funcionalidades nao so uma, e.g.: criar e escrever, ou abrir e escrever, etc.
    def test_file1(self):
        pass
