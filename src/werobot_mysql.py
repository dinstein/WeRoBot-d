#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import random
import itertools
import jieba
import re
try:
    import werobot_config
    _MYSQL_HOST = werobot_config._MYSQL_HOST
    _MYSQL_USER = werobot_config._MYSQL_USER
    _MYSQL_PW = werobot_config._MYSQL_PW
    _MYSQL_DB = werobot_config._MYSQL_DB
except Exception, e:
    _MYSQL_HOST = "localhost"
    _MYSQL_USER = "root"
    _MYSQL_PW = "mysql_pw"
    _MYSQL_DB = "mysql_db"


class RobotMysql:
    def __init__(self, host=_MYSQL_HOST, user=_MYSQL_USER, passwd=_MYSQL_PW, db=_MYSQL_DB):
        self.mysql_config = [host, user, passwd, db]
        self.conn = MySQLdb.connect(host, user, passwd, db)
        self.cursor = self.conn.cursor()

    def closeCursor(self):
        self.cursor.close()

    def execute(self, cmd):
        """ execute """
        try:
            r = self.cursor.execute(cmd)
        except:
            self.conn = MySQLdb.connect(host=self.mysql_config[0], user=self.mysql_config[1],
                                        passwd=self.mysql_config[2], db=self.mysql_config[3])
            self.cursor = self.conn.cursor()
            r = self.cursor.execute(cmd)
        return r

    def select(self, cmd):
        count = self.execute(cmd)
        if (count > 0):
            results = self.cursor.fetchmany(count)
        else:
            results = None
        return results

    def searchID(self, id):
        cmd = "select id,match_count,Q,A from talk where id=%s" % str(id)
        return self.select(cmd)

    def insertQA_e(self, QA):
        Ques = QA[0][0:500]
        Anws = QA[1][0:500]
        cmd = "insert into talk_e values(NULL,0,'%s','%s')" % (Ques, Anws)
        return self.execute(cmd)

    def insertQA(self, QA):
        Ques = QA[0][0:500]
        Anws = QA[1][0:500]
        cmd = "insert into talk values(NULL,0,'%s','%s')" % (Ques, Anws)
        return self.execute(cmd)

    def findmin(self, results, Ques):
        ind = 0
        length = len(results[0][3])
        i = 0
        for r in results:
            if (len(r[3]) < length):
                ind = i
                length = len(r[3])
            i = i + 1
        if (len(results[ind][3]) - len(Ques) < 5):
            return ind
        else:
            return random.randint(0, len(results) - 1)

    def searchQ(self, Q):
        Ques = Q[0:200]
        cmd = "select id,match_count,A,Q from talk where Q like '%%%s%%'" % Ques
        count = self.execute(cmd)
#        self.execute("update talk set match_count=%d where id=%d",match_count,id)
        if (count > 0):
            results = self.cursor.fetchmany(count)
#            ind = random.randint(0,count-1)
            ind = self.findmin(results, Ques)
            return (results[ind][0], results[ind][2])
        else:
            return (None, None)

    def searchQs(self, Qs):
        Qs.sort(key=lambda x: len(x), reverse=True)
        Qs = Qs[0:10]
        key_count = 11
        ans_list = list()
        while key_count > 0:
            Qs_iter = itertools.combinations(Qs, key_count)
            for Q in Qs_iter:
                cmd_like = "%' and Q like '%".join(Q)
                cmd = "select id,match_count,A from talk where Q like '%%%s%%'" % cmd_like
                count = self.execute(cmd)
                if (count > 0 & (len(Qs) - key_count<4)):
                    results = self.cursor.fetchmany(count)
                    ind = random.randint(0, count - 1)
                    return (results[ind][0], results[ind][2])
                elif (count > 0):
                    results = self.cursor.fetchmany(count)
                    for r in results:
                        ans_list.append(r)
            key_count = key_count - 1
        if (len(ans_list) > 0):
            ind = random.randint(0, len(ans_list) - 1)
            return (ans_list[ind][0], ans_list[ind][2])
        else:
            return (None, None)

    def delID(self, id):
        cmd = "delete * from talk where id=%d" % id
        self.execute(cmd)

    def insertQAs(self, QAs):
        for QA in QAs:
            self.InsertQA(QA)

    def lookforAns(self, Q):
        Qre = re.sub("[,|.|~|!|@|#|$|%|^|&|:|*|。|，|：]", "", Q)
        (id, ans) = self.searchQ(Qre)
        if ans is None:
            str_list = jieba.cut(Q)
            Ques = list()
            for s in str_list:
                Ques.append(s.encode('utf-8'))
            (id, ans) = self.searchQs(Ques)
            return (id, ans)
        else:
            return (id, ans)

################################################################################
if __name__ == "__main__":
    m = RobotMysql()
    (id, r) = m.searchQ('hi')
    print r
    (id, r) = m.lookforAns('Hello World!')
    print r
    m.closeCursor()
