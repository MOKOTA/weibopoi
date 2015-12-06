__author__ = 'YangZongyun'
# -*- coding: utf-8 -*-


from weibo import APIClient
import webbrowser
import MySQLdb
import numpy as np


APP_KEY = YourAppKey  # need init
APP_SECRET = YourAppSecret  # need init
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'  # callback url
CLIENT = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
URL = CLIENT.get_authorize_url()


def db_connect(poiid, title, address, lat, lon, category, checkin_user_num, city):
    if city != u'0025': # 0025 is the code of Nanjing you can change this by you own need
        return
    else:
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user=DbUser,
            passwd=DbPass,
            db=DBName,
            charset='utf8'
        )
        cur = conn.cursor()
        cur.execute('set names utf8')
        try:
            sql = "insert into weibopoi(poiid, title, address, lon, lat, category,checkin_user_num,city)\
         values('%s','%s','%s','%s','%s', '%s', '%s', '%s');"\
              % (poiid, title, address, lon, lat, category, checkin_user_num,city)
            n = cur.execute(sql)
        except:
            conn.rollback()
        cur.close()
        conn.commit()
        conn.close()


def weibo_api(client, deflat, deflong):

    r = client.place.nearby.pois.get(lat=deflat, long=deflong, range=10000)
    return r

if __name__ == '__main__':
    '''db_connect()'''
    webbrowser.open_new(URL)
    code = raw_input('pls input \n')
    CLIENT = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    R = CLIENT.request_access_token(code)
    access_token = R.access_token
    expires_in = R.expires_in
    CLIENT.set_access_token(access_token, expires_in)
    for i in np.linspace(0, 1.384, 1500, endpoint=False):
        LAT = 31.23 + i
        for j in np.linspace(0, 0.88, 1500, endpoint=False):
            LONG = 118.36 + j
            LAT = float('%0.5f' % LAT)
            LONG = float('%0.5f' % LONG)
            try:  # consider the situation of weibo api times limits
                Json_content = weibo_api(client=CLIENT, deflat=LAT, deflong=LONG)
                print str(LAT)+'\t'+str(LONG)+'\n'
                try:  # keep the programm going on when Json_comtent is empty, keep the code not crushing
                    for poi in Json_content['pois']:
                        _poiid = poi['poiid']
                        _title = poi['title']
                        _address = poi['address']
                        _lat = poi['lat']
                        _lon = poi['lon']
                        _category = poi['category_name']
                        _checkin_user_num = poi['checkin_user_num']
                        _city = poi['city']
                        db_connect(poiid=_poiid, title=_title, address=_address, lat=_lat, lon=_lon, category=_category,  checkin_user_num=_checkin_user_num, city=_city)
                except:
                    pass
            except:
                webbrowser.open_new(URL)
                code = raw_input('pls input \n')
                CLIENT = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
                R = CLIENT.request_access_token(code)
                access_token = R.access_token
                expires_in = R.expires_in
                CLIENT.set_access_token(access_token, expires_in)
