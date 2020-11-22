import sqlite3


def createServer():
    global db, sql
    db = sqlite3.connect("server.db", check_same_thread=False)
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS users (id INT, name TEXT, age INT,
     course INT, url TEXT, money INT)""")
    db.commit()


def createMyTaskTableSQL():
    global sql, db
    sql.execute("""CREATE TABLE IF NOT EXISTS mytasks (id TEXT, subject TEXT, difficulty TEXT, cost INT)""")
    db.commit()


def createNotMyTaskTableSQL():
    global sql, db
    sql.execute("""CREATE TABLE IF NOT EXISTS notmytasks (id INT, subject TEXT, difficulty TEXT, cost INT)""")
    db.commit()


def taskCostSQL(subject, difficulty):
    global sql
    sql.execute(f"SELECT cost FROM notmytasks WHERE subject = ? AND difficulty = ?", (subject, difficulty,))
    costTask = sql.fetchall()

    return costTask


def addToInProcessSQL(cost, username, subject, difficulty):
    global db, sql
    sql.execute(f"INSERT INTO mytasks VALUES (?, ?, ?, ?)", (username, subject, difficulty, cost,))
    db.commit()


def showInProcess(user_username):
    global sql
    information = []
    sql.execute(f"SELECT cost FROM mytasks WHERE id = ?", (user_username,))
    information.append(sql.fetchall())
    sql.execute(f"SELECT subject FROM mytasks WHERE id = ?", (user_username,))
    information.append(sql.fetchall())
    sql.execute(f"SELECT difficulty FROM mytasks WHERE id = ?", (user_username,))
    information.append(sql.fetchall())
    return information



def offerTaskSQL(user_id, subject, difficulty, cost):
    global sql, db
    sql.execute(f"INSERT INTO notmytasks VALUES (?, ?, ?, ?)", (user_id, subject, difficulty, cost,))
    db.commit()


def userInfoSQL(user_id):
    global sql
    information = []
    sql.execute(f"SELECT name FROM users WHERE id = ?", (user_id,))
    information.append(sql.fetchone())
    sql.execute(f"SELECT age FROM users WHERE id = ?", (user_id,))
    information.append(sql.fetchone())
    sql.execute(f"SELECT course FROM users WHERE id = ?", (user_id,))
    information.append(sql.fetchone())
    sql.execute(f"SELECT money FROM users WHERE id = ?", (user_id,))
    information.append(sql.fetchone())
    return information


def registration(user_id, user_username):
    global sql, db
    sql.execute(f"SELECT id FROM users WHERE id = ?", (user_id,))
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user_id, '', 0, 0, user_username, 100))
        db.commit()

        return True
    else:
        return False


def SQLreg(user_id, name, url, age, course):
    global sql, db
    sql.execute(f"UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    sql.execute(f"UPDATE users SET age = ? WHERE id = ?", (age, user_id))
    sql.execute(f"UPDATE users SET course = ? WHERE id = ?", (course, user_id))
    sql.execute(f"UPDATE users SET url = ? WHERE id = ?", (url, user_id))
    db.commit()


def botStart():
    createServer()
    createMyTaskTableSQL()
    createNotMyTaskTableSQL()
