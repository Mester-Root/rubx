#!/bin/python

import sqlite3

suffix: str = '.rbs'
rbs_version: int = 1

class SQLiteSession(object):

    def __init__(self, session: str) -> ...:
        self.filename = session
        if not session.endswith(suffix):
            self.filename += suffix

        self._connection = sqlite3.connect(self.filename,
                                           check_same_thread=False)
        cursor = self._connection.cursor()
        cursor.execute('select name from sqlite_master '
                       'where type=? and name=?', ('table', 'version'))
        if cursor.fetchone():
            cursor.execute('select version from version')
            version = cursor.fetchone()[0]
            if rbs_version != version:
                self.upgrade_database(version)

        else:
            cursor.execute(
                'create table version (version integer primary key)')
            cursor.execute('insert into version values (?)', (rbs_version,))
            cursor.execute('create table session (phone text primary key'
                           ', auth text, guid text, agent text)')
            self._connection.commit()
        cursor.close()

    def upgrade_database(self, version):
        pass

    def information(self) -> tuple:
        cursor = self._connection.cursor()
        cursor.execute('select * from session')
        result = cursor.fetchone()
        cursor.close()
        return result

    def insert(
        self        :   'SQLiteSession',
        phone_number:   str =   None,
        key         :   str =   None,
        guid        :   str =   None,
        url         :   str =   None
        ):
        cursor = self._connection.cursor()
        cursor.execute(
            'insert or replace into session (phone, auth, guid, agent)'
            ' values (?, ?, ?, ?)',
            (phone_number, key, guid, url)
        )
        self._connection.commit()
        cursor.close()

    @classmethod
    def from_string(cls, session: object,
                    file_name: str=None) -> (...):
        info = session.information()
        if file_name is None:
            if info is None:
                raise ValueError('file_name arg is not set')
            file_name = info[0]

        session = SQLiteSession(file_name)
        if info is not None:
            session.insert(*info)

        return session