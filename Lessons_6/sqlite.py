import sqlite3

"""
SQLite database
"""


async def db_start():
    global db, cur
    db = sqlite3.connect("users_bot.db")
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS profile(
    user_id INT PRIMARY KEY,
    photo TEXT,
    name TEXT,
    age INT,
    description TEXT 
    
    
    );""")


async def create_profile(user_id):
    user = cur.execute("""SELECT user_id from profile WHERE user_id == '{key}'""".format(key=user_id)).fetchone()
    if not user:
        cur.execute("""INSERT INTO profile VALUES(?,?,?,?,?) """, (user_id, '', '', '', ''))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("""UPDATE profile 
                         SET
                            photo = '{photo}',
                            name = '{name}',
                            age = '{age}',
                            description = '{description}'
                         WHERE user_id == '{user}'   
                            
                            """.format(user=user_id,
                                       photo=data['photo'],
                                       age=data['age'],
                                       description=data['description'],
                                       name=data['name']))
        db.commit()
