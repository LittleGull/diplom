# -*- coding: utf-8 -*-
"""
@author: IKlitochenko
"""
import sys
import datetime
import psycopg2
import psycopg2.extras
import settings
import logging


logger = logging.getLogger("main.dboperator")

class DBOperator():
    
        
    def __init__(self): 
        
        self.conn = None
        self.cur = None
        self.ndvi = ''
        self.bands = ''
            
        
    def _open_connection(self):
        
        if not self.conn:            
            try:               
                self.conn = psycopg2.connect("dbname='" + settings.DBNAME + "' user='" + settings.DBUSER + "'" \
                                             " host='" + settings.DBHOST + "' password='" + settings.DBPASSWORD + "'")   
                self.cur = self.conn.cursor() 
            except psycopg2.Error as e:
                logger.critical('Unable to open connection. DB connection error: "{}"'.format(e))
                sys.exit(1)


    def _close_connection(self):

        if self.conn:
            self.cur.close()
            self.conn.close()
            self.conn = None
            self.cur = None


    def get_bounds_wkt(self, year, field_group=None, field_id=None, srid=4326):
        """ Gets coordinates of rectangle frames all fields in database or fields within particular group.
            Geometries of fields valid for particular year.

        :returns:
            (String) Bounds WKT string: 'POLYGON((27.3271211 53.8350367,27.3271211 53.8364177,27.3376134 53.8364177,27.3376134 53.8350367,27.3271211 53.8350367))'
        """
        self._open_connection()

        sql = 'SELECT * FROM __geostl_get_boundpoints_wkt(%s, %s, %s, %s)'
        try:
            self.cur.execute(sql,(year, srid, field_id, field_group))
            latsLons = self.cur.fetchone()[0]
            if latsLons:
                return latsLons
            else:
                logger.critical("Unable to get bounds, geometry is empty for {} year, {} group or {} field.".format(year, field_group, field_id))
                sys.exit(1)

        except psycopg2.Error as e:
            logger.critical('Unable to get coordinates of rectangle frames all fields in database.DB query error: "{}"'.format(e))
            sys.exit(1)
        finally:
            self._close_connection()


    def get_bounds_LatsLons(self, year, field_group=None, field_id=None):
        """ Gets coordinates of rectangle frames all fields, fields within particular group or single field.
            Geometries of fields are actual for particular year.

        :returns:
            List [x_min, y_min, x_max, y_max]
        """
        self._open_connection()

        try:
            sql = 'SELECT * FROM __geostl_get_boundpoints(%s, %s, %s, %s)'
            self.cur.execute(sql, (year, settings.DESTSRID, field_id, field_group))

            latsLons = self.cur.fetchall()

            return [latsLons[0][0], latsLons[0][1], latsLons[2][0], latsLons[2][1]]

        except psycopg2.Error as e:
            logger.critical('Unable to get coordinates of rectangle frames all fields or fields within '
                            'particular group. DB query error: "{}"'.format(e))
            sys.exit(1)
        finally:
            self._close_connection()


    def get_start_date(self, field_group=None):
        """ Gets last date from Layer table and adds 1 day.

        :returns:
            Date
        """
        self._open_connection()

        sql = 'SELECT * FROM __geostl_get_last_date(%s)'
        try:
            self.cur.execute(sql, (field_group,))
            date = self.cur.fetchone()[0]
            if date:
                date = date + datetime.timedelta(days=1)
                return date
            else:
                logger.critical("Unable to get the last date, 'Layer' table is empty. Set start date.")
                sys.exit(1)
        except psycopg2.Error as e:
            logger.critical('Unable to get the last date. DB query error: "{}"'.format(e))
            sys.exit(1)
        except Exception as e:
            logger.critical('Unable to get the last date. Error: "{}"'.format(e))
            sys.exit(1)
        finally:
            self._close_connection()


    def get_field_groups(self):
        """ Gets list of field groups.

        :returns:
            List
        """
        self._open_connection()

        sql = 'SELECT * FROM __geostl_get_field_group_ids()'
        try:
            self.cur.execute(sql)
            groups = self.cur.fetchall()
            if groups:
                groups = [i[0] for i in groups]
            else:
                groups = []

            return groups

        except psycopg2.Error as e:
            logger.critical('Unable to get list of groups of fields. DB query error: "{}"'.format(e))
            sys.exit(1)
        finally:
            self._close_connection()


    def get_group(self, field_id):
        """ Gets group for field.

        :returns:
            Integer
        """
        self._open_connection()

        sql = 'SELECT * FROM __geostl_get_group({})'
        try:
            self.cur.execute(sql.format(field_id))
            group = self.cur.fetchone()[0]
            if not group:
                logger.critical("Unable to get group for field. Field with ID '{}' doesn't exist "
                                "in database or doesn't belong any group.".format(field_id))
                sys.exit(1)

            return group

        except psycopg2.Error as e:
            logger.critical('Unable to get group for field. DB query error: "{}"'.format(e))
            sys.exit(1)
        finally:
            self._close_connection()


    def get_geometries(self, polygon, year, field_group=None, field_id=None):
        """ Gets geometries of fields or geometry of single field as list of WKT multipolygons/polygons.

        :returns:
            List
        """
        self._open_connection()

        try:
            sql = "SELECT * FROM __geostl_get_geometries(%s, %s, %s, %s, %s)"
            self.cur.execute(sql, (year, settings.DESTSRID, field_id, field_group, polygon))
            fields = self.cur.fetchall()
            if fields:
                fields = {i[1]: {'geom': i[0]} for i in fields}
            else:
                logger.warning("There are no geometries of fields for {} year, '{}' group or '{}' field.".format(year, field_group, field_id))
                fields = {}

            return fields

        except psycopg2.Error as e:
            logger.critical("Unable to get geometries of fields as list of WKT multipolygons/polygons. "
                            "DB query error: '{}'.'".format(e))
            sys.exit(1)
        finally:
            self._close_connection()


    def append_field(self, field_id, bytea, ds_name, cloud, date):
        """ Appends field's geotiff and addition data to query string for insert command.

        """
        try:
            if ds_name == 'ndvi':
                values = 'INSERT INTO public."ndvi"(field_id, rast, cloud_cover, date) VALUES ({}, ST_FromGDALRaster({}::bytea, {}), {}::smallint, \'{}\'); '
                self.ndvi += values.format(field_id, psycopg2.Binary(bytea), settings.DESTSRID, cloud, date)
            else:
                values = 'INSERT INTO public."band_raster"(field_id, band, rast, cloud_cover, date) VALUES ({}, \'{}\', ST_FromGDALRaster({}::bytea, {}), {}::smallint, \'{}\'); '
                self.bands += values.format(field_id, ds_name, psycopg2.Binary(bytea), settings.DESTSRID, cloud, date)
        except Exception as e:
            logger.critical("Unable to append field's geotiff and addition data to query string for "
                            "insert command, there is an error: '{}'.".format(e))
            sys.exit(1)


    def insert_images(self, date, field_group=None, field_id=None):
        """ Inserts field's geotiff and addition data to db.

        """
        self._open_connection()

        try:
            query = 'DELETE FROM public."{}" WHERE date = \'{}\' '
            if field_id:
                query += ' AND field_id = {}'.format(field_id)
            elif field_group:
                query += ' AND field_id in (SELECT id FROM public."field" WHERE field_group_id = {})'.format(field_group)
            query += '; {} '

            sql = ''
            if self.ndvi:
                sql = query.format('ndvi', date, self.ndvi)
            if self.bands:
                sql += query.format('band_raster', date, self.bands)

            self.cur.execute(sql)
            self.conn.commit()

        except psycopg2.Error as e:
            logger.critical('Unable to insert field\'s geotiff and addition data to db. DB query error: "{}"'.format(e))
            sys.exit(1)
        finally:              
            self._close_connection()


    def insert_layer(self, layer):

        self._open_connection()

        try:
            sql = 'INSERT INTO public."Layer"(date, set, resolution, agroid, fieldid, name, satellite, isgrouplayer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            self.cur.execute(sql, layer)
            self.conn.commit()

        except psycopg2.Error as e:
            # PostgreSQL unique_violation - 23505 (* PostgreSQL Error Codes). The layer already exists in db table.
            if e.pgcode == '23505':
                pass
            else:
                logger.critical("Unable to insert layer. "
                                "DB query error: '{}'.".format(e))
                sys.exit(1)
        finally:
            self._close_connection()


    def delete_layer(self, layer):

        self._open_connection()

        try:
            sql = 'DELETE FROM public."Layer" WHERE name = \'%s\''
            self.cur.execute(sql % layer)
            self.conn.commit()

        except psycopg2.Error as e:

            logger.critical("Unable to delete layer from db. "
                            "DB query error: '{}'.".format(e))
            sys.exit(1)
        finally:
            self._close_connection()
             
             


if __name__ == '__main__':

    db = DBOperator() 
   
    print(db.get_start_date())