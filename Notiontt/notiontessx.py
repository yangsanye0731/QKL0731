from notion_database.database import Database

database = Database(
    integrations_token="secret_rxaAzcdjzdVq4pe1hrkqkhzxJlm2isBh96Z4rxdB9Cc"
)
database.retrieve_database(
    database_id="00ca54374986450eaf3cf05678b7268d", get_properties=True
)

print(database.properties_list)