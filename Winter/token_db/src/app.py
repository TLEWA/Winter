from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import yaml
from os import path
import logging
import re
import httpx

RE_TOKEN = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
RE_UID = "^\\d{1,7}$"
RE_COLIPBOARD = "[a-z0-9]{5,9}"


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("token_db")
app = FastAPI()
config = yaml.safe_load(open("config.yaml", "r"))


class Database(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def execute(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor

    def execute_sql(self, sql: str, params: list = []):
        # 读取SQL文件内容
        try:
            with open(path.abspath(path.join("../db/", sql+".sql")), encoding='utf-8', mode='r') as f:
                sql_list = f.read().split(';')
                sql_list = [x.replace("\n", " ") for x in sql_list
                            if x.replace("\n", " ") != '' and not x.replace("\n", " ").isspace()]
                logger.info(f"execute sql list: {sql_list}")
                if (params != []):
                    if len(params) != len(sql_list):
                        raise Exception("params length not match sql length")
                    for x, p in zip(sql_list, params):
                        sql_item = x+';'
                        logger.info(f"execute sql: {
                                    sql_item} with params: {p}")
                        self.execute(sql_item, p)
                else:
                    for x in sql_list:
                        sql_item = x+';'
                        logger.info(f"execute sql: {sql_item}")
                        self.execute(sql_item)
        except Exception as e:
            logger.error(f"execute sql error: {e} when execute {sql}")
        return self.cursor

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        result = self.cursor.fetchone()
        logger.info(f"fetch one: {result}")
        return result


db = Database(path.abspath(path.join("../db/", config["db"]["name"])))
db.execute_sql("query_table")
if db.fetchone() is None:
    db.execute_sql("create_table")


class Item(BaseModel):
    paste: str | None = None
    token: str | None = None


@app.get("/")
async def read_root():
    return "heartbeating!"


@app.get("/get/{numbers}")
async def get_token(numbers: int):
    # return {"item_id": item_id, "q": q}
    pass


@app.get("/getnumber")
async def get_number():
    db.execute_sql("query_table_number")
    return {"status": 200, "number": db.fetchone()[0]}


@app.post("/change/{uid}")
async def change_token(uid: str, item: Item):

    if item is None:
        return 422
    if item.paste is None and item.token is None:
        return 422
    if re.match(RE_UID, uid) is None:
        return 422
    if item.token is not None and not re.match(RE_TOKEN, item.token):
        return 422
    if item.paste is not None and not re.match(RE_COLIPBOARD, item.paste):
        return 422
    paste = item.paste
    token = item.token

    # 开始检验 paste
    req_data = {"uid": int(uid), "paste": paste}
    request = httpx.post("https://api.paintboard.ayakacraft.com:11451/api/auth/gettoken",
                         json=req_data)
    logging.info(f"request paintboard API: {
                 request} and respond with message: {request.text}")

    respond = request.json()

    if respond["statusCode"] == 200:
        # 检验成功
        token = respond["data"]["token"]
    else:
        logger.warning(f"cilpboard check error: {respond}")
        if respond["statusCode"] == 403:
            return 402

    db.execute_sql("query_uid", [[uid]])
    if db.fetchone() is None:
        db.execute_sql("insert", [[uid, paste, token]])
    else:
        db.execute_sql("change", [[paste, token, uid]])
    return 200
