import json
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def delete_all_nodes(tx):
    query = "MATCH (n) DETACH DELETE n"
    tx.run(query)

def create_champion(tx, name, stats, data):
    query = """
    MERGE (c:Champion {name: $name})
    SET c += $stats
    """
    tx.run(query, name=name, stats={**stats, **data})  # Merge stats and data directly into Champion node

def create_role_and_relationship(tx, role, champions):
    query = """
    MERGE (r:Role {name: $role})
    """
    tx.run(query, role=role)

    for champion in champions:
        query = """
        MATCH (r:Role {name: $role})
        MATCH (c:Champion {name: $champion})
        MERGE (c)-[:hasRole]->(r)
        """
        tx.run(query, role=role, champion=champion)

with driver.session() as session:
    session.execute_write(delete_all_nodes)

    with open('champion_data.json', 'r') as json_file:
        champion_data_list = json.load(json_file)

        for champion_data in champion_data_list:
            name = champion_data['name']
            stats = champion_data['stats']
            data = champion_data.get('data', {})  # Use .get() to avoid KeyError

            with driver.session() as session:
                session.execute_write(create_champion, name, stats, data)

    with open('role_data.json', 'r') as json_file:
        role_data = json.load(json_file)

        for role, champions in role_data.items():
            with driver.session() as session:
                session.execute_write(create_role_and_relationship, role, champions)

driver.close()
