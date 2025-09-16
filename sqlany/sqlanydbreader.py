import os

import sqlanydb
import hashlib
from dotenv import load_dotenv



class SQLAnyDBReader:
    def __init__(self,as_cursor=False):
        load_dotenv()
        self.con = None
        self.cursor = None
        self.rows = []
        self.desc = None
        self.unique_rows = []
        self.hashed_set = set()
        self.as_cursor = as_cursor

    def __enter__(self):
        self.con = sqlanydb.connect(
            uid=os.getenv("ANYDB_UID"),
            pwd=os.getenv("ANYDB_PWD"),
            servername=os.getenv("ANYDB_SERVERNAME"),
            dbn=os.getenv("ANYDB_DBN"),
            astart="No",
            host=os.getenv("ANYDB_HOST"),
        )
        self.cursor = self.con.cursor()
        if self.as_cursor:
            return self.cursor
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.con:
            self.con.close()


    def querySelect(self, query: str):
        self.cursor.execute(query)
        self.desc = self.cursor.description
        self.rows = self.cursor.fetchall()

    def removeDuplicates(self,rows):
        if not self.rows:
            self.unique_rows = []
            self.hashed_set = set()
            return

        self.unique_rows = []
        self.hashed_set = set()
        for row in self.rows:
            hash_value = hashlib.sha256(str(row).encode('utf-8')).hexdigest()
            if (hash_value,) not in rows:
                self.hashed_set.add((hash_value,))
                self.unique_rows.append(row)


    def close(self):
        try:
            self.cursor.close()
        finally:
            self.con.close()

    def __del__(self):
        self.close()

