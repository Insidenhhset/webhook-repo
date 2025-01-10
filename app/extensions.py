from flask_pymongo import PyMongo

mongo = PyMongo()


def init_extensions(app):
    mongo.init_app(app)


# Define the schema for the collection
# git_operations_schema = {
#     "$jsonSchema": {
#         "bsonType": "object",
#         "required": ["request_id", "author", "action", "from_branch", "to_branch", "timestamp"],
#         "properties": {
#             "request_id": {
#                 "bsonType": "string",
#                 "description": "Unique ID for the request"
#             },
#             "author": {
#                 "bsonType": "string",
#                 "description": "Name of the author"
#             },
#             "action": {
#                 "enum": ["MERGE", "PULL_REQUEST", "PUSH"],
#                 "description": "Type of action performed"
#             },
#             "from_branch": {
#                 "bsonType": "string",
#                 "description": "Source branch name"
#             },
#             "to_branch": {
#                 "bsonType": "string",
#                 "description": "Target branch name"
#             },
#             "timestamp": {
#                 "bsonType": "date",
#                 "description": "Timestamp of the operation"
#             }
#         }
#     }
# }
