
#!/usr/bin/python3
 
import pymysql
 
def save_total(id, total,db):
    cursor = db.cursor()
    # SQL 插入语句
    sql = "update INTO mm_info set total="+total+" where id='"+id+"'"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("save success")
    except:
        # 如果发生错误则回滚
        db.rollback()

def save_mm_pic(id, name, page, db):
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute("SELECT count(1) from mm_pic where id="+id +" and name='" +name+"'")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    if data[0] == 0 :
        # SQL 插入语句
        sql = "INSERT INTO mm_pic(id,name,page) \
            VALUES ('%s','%s',%s)" % \
            (id, name, page)
        print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print("save success")
        except:
            # 如果发生错误则回滚
            db.rollback()

def save_mm_info(id, tag, src, title, url, db):
    # 打开数据库连接
    # db = pymysql.connect("localhost","root","Test123456","pinkdao" )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute("SELECT count(1) from mm_info where id="+id)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    
    print ("get count by id : %s " % data)
    if data[0] == 0 :
        # SQL 插入语句
        sql = "INSERT INTO mm_info(id,tag,src,title,orglink,create_time,update_time) \
            VALUES ('%s','%s','%s','%s','%s', now(), now() )" % \
            (id, tag, src, title, url)
    #    "INSERT INTO mm_info(id,tag,src,title,orglink,create_time,update_time) VALUES ("+id+","+tag+","+src+","+title+","+url+",now(),now())"
        print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print("save success")
        except:
            # 如果发生错误则回滚
            db.rollback()
    
    # # 关闭数据库连接
    # db.close()

# save_mm_info('11111', 'hot','testsrc','testtitle','testorglink')