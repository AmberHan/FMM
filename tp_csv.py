# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/11 9:46
# !@Author : DongHan Yang
# !@File   : tp_csv.py
# Import the driver
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import csv
from urllib.parse import quote


class App:
    # 实例化驱动
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # 建立唯一性关系（防止出现冗余节点）
    def constraint(self, category, title):
        query = f"""
        CREATE CONSTRAINT FOR ({category}:{category}) REQUIRE {category}.{title} IS UNIQUE
        """
        self.run_query(query)

    # 关闭驱动
    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    # 执行csv数据库指令
    def run_query(self, query):
        # Create the driver session
        with self.driver.session() as session:
            try:
                print(session.run(query).data())
            # 可能有问题
            except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                    query=query, exception=exception))
                raise


# 处理csv的head
def pd_head(file):
    with open(file, 'r', encoding='utf-8') as fr:
        reader = csv.DictReader(fr)
        headers = reader.fieldnames
        fn = file.split('/')[-1].split('.')[0]
        # headers.insert(0, fn)
        # print(headers)
        return fn, headers


# 创建语句
def create_quary(file, fn, hd):
    # fn, hd = pd_head(file)
    csv_quary0 = f"""
        LOAD CSV
          WITH HEADERS
          FROM '{file}' AS row
        MERGE (ca:`{fn}` {{`{hd[0]}`: row.`{hd[0]}`}}) ON CREATE SET ca.`{hd[0]}` = row.`{hd[0]}`"""
    for index in range(1, len(hd)):
        h = hd[index]
        # for h in hd:
        csv_quary0 = csv_quary0 + """, ca.`""" + h + """` = row.`""" + h + """`"""
    csv_quary1 = """  RETURN count(*)"""
    return csv_quary0 + csv_quary1


# 关系语句
def relationship_quary(file, fn1, fn2, hd):
    csv_quary = f"""
        LOAD CSV
              WITH HEADERS
              FROM '{file}' AS row
              FIELDTERMINATOR ','
            MATCH (a:`{fn1}` {{`{hd[0]}`: row.`{hd[0]}`}})
            MATCH (b:`{fn2}` {{`{hd[2]}`: row.`{hd[2]}`}})
            MERGE (a)-[actedIn:`{hd[1]}`]->(b)
              ON CREATE SET actedIn.`{hd[1]}` = split(row.`{hd[1]}`, ';')
            RETURN count(*)
    """
    return csv_quary


# 处理本地和云端数据
def do_path(fname):
    fnamek = quote(fname)
    path = f"csv/{fname}.csv"
    path1 = f"https://github.com/AmberHan/FMM/raw/main/csv/{fnamek}.csv"
    category, hd = pd_head(path)
    return category, hd, path1


# 实体
def node(fname):
    category, hd, path = do_path(fname)
    title = hd[0]
    try:
        app.constraint(category, title)  # 建立依赖
    except:
        pass
    load_csv = create_quary(path, category, hd)
    print(load_csv)
    app.run_query(load_csv)


# 关系
def relation(fname):
    categorys, hd, path = do_path(fname)
    ca = categorys.split('_')
    load_csv = relationship_quary(path, ca[0], ca[1], hd)
    print(load_csv)
    app.run_query(load_csv)


# 实体csv: 文件名为类名；文件头为属性；第一列为唯一性
# 实体关系：文件名为两个类名；文件头为类1的属性、关系、类2的属性（对应实体csv的head）
# 注意本代码都要是中文 加了``
# 第一次运行时，需要建立实体的独立性
if __name__ == "__main__":
    uri = "neo4j+s://5bd229c3.databases.neo4j.io"
    user = "neo4j"
    password = "fUAA-yIqnA5MXltzdWHBSPYJ5cDRiTuVJvWz1Sg3IEY"
    app = App(uri, user, password)
    # 实体1
    node("词牌名")
    node("牡丹亭")
    # 实体间的关系
    relation("牡丹亭_词牌名")

    # 实体诗人
    # node("诗人")
    # # 实体间的关系
    # for i in range(1, 9):
    #     relation(f"牡丹亭_诗人_{i}")
    # app.close()
