from neo4j import GraphDatabase
import csv

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j")


def upload_friends(session):
    with open('friends.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            friends = row[1]
            friends = friends[1:-1]
            friend_list = list(friends.split(', '))
            for i in friend_list:
                if i:
                    result = session.run("match (a:Person {id:$id}) with count(a) > 0 as exists "
                                         "return exists", id=i)
                    if result.single()[0]:
                        session.run("match (a {id:$id_a}), (b {id:$id_b}) create (a)-[:friends_with]->(b) ",
                                    id_a=row[0], id_b=i)


def upload_nodes(session):
    with open('names.csv', 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            session.run(
                "create (a:Person {id:$id,name:$name,surname:$surname,country:$country,city:$city,sex:$sex,bdate:$bdate})",
                id=row[1], name=row[2], surname=row[3], country=row[4], city=row[5], sex=row[6], bdate=row[7])


def create_person(tx, name):
    tx.run("CREATE (a:Person {name: $name})", name=name)


def create_friend_of(tx, name, friend):
    tx.run("MATCH (a:Person) WHERE a.name = $name "
           "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
           name=name, friend=friend)


session = GraphDatabase.driver(URI, auth=AUTH).session()

# upload_nodes(session)

upload_friends(session)
