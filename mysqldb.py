#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import MySQLdb

def connection():
    conn = MySQLdb.connect("localhost", "root", "sdbitwtg", "sgdb")
    
    c = conn.cursor()
    
    return c, conn

