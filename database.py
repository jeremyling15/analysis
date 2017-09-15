__author__ = "JL"
__version__ = "0.1a"

from sqlalchemy.ext.automap import  automap_base
from sqlalchemy import Table, Column, String, Integer, Float, Boolean, DateTime, and_
import datetime

class TableFactory(object):
    """
    Class for dynamically creating tables if they do not exists.
    """
    # engine defaults to lite memory if not specified
    def __init__(self, tablename, metadata, engine, session, tabledata=None):
        """

        :param tablename: Name of the table to be created
        :param metadata: sqlalchemy metadata object
        :param engine: sqlalchemy engine
        :param tabledata: list of dictionaries of **(header, data)
        """
        self.engine = engine
        self.metadata = metadata
        self.session = session
        if tabledata:
            self.tabledata = tabledata
        # check if table exists. TODO: seems dumb
        if self.engine.dialect.has_table(self.engine, tablename):
            Table(tablename, self.metadata, autoload=True, autoload_with=self.engine)
        else:
            self.__create_table(tablename=tablename)
        if self.tabledata:
            self.base = automap_base()
            self.base.prepare(self.engine, reflect=True)
            self.__table_load(tablename=tablename)


    def __analyze_data(self, ):
        """
        Takes in table data from init and analyzes what the table should be constructed as.
        :return: Column structure for table
        """
        final = {}
        for row in self.tabledata:
            for key in row:
                var = row[key]
                ctype=None
                ##Quick duck typing
                try:
                    var = float(var)
                    if var == int(var) and final.get(key) is not float:
                        ctype = Integer
                    else:
                        ctype = Float
                except (ValueError, TypeError) as  e:
                    if final.get(key) not in (float, int) and str(var) in ('False', 'True'):
                        ctype = Boolean
                    elif final.get(key) not in (float, int, bool, datetime.datetime):
                        ctype = String
                final[key.lower()] = ctype
        #TODO: Implement foreign key constraint looks ups
        #TODO: Duck typing for date datatypes
        return final

    def __create_table(self, tablename):
        cols = self.__analyze_data()
        self.table = Table(tablename,
                      self.metadata,
                      Column(tablename + '_id', Integer, autoincrement=True, primary_key=True),
                      *(Column(col.lower(), cols[col]) for col in cols),
                      Column('createddate', DateTime, default=datetime.datetime.now()),
                      Column('updateddate', DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
                      )
        self.metadata.create_all(bind=self.engine)

    def __table_load(self, tablename):
        #TODO: duplicate entriees on load? need an upsert if table exists and is loaded
        for row in self.tabledata:
            table = getattr(self.base.classes, tablename)()
            for key in row:
                key_ = key.lower()
                setattr(table, key_, row[key])
            self.session.add(table)
        self.session.flush()
