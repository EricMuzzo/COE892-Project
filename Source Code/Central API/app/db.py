from motor.motor_asyncio import AsyncIOMotorClient

#hardcoding mongo connection string for now
MONGO_URI = "mongodb+srv://ericmuzzo:Eric123@coe692project.1facf.mongodb.net/?retryWrites=true&w=majority&appName=coe692project"
DB_NAME = 'coe692db'

client: AsyncIOMotorClient = None
database = None

async def connect_to_mongo(app) -> None:
    global client, database
    client = AsyncIOMotorClient(MONGO_URI)
    database = client.get_database(DB_NAME)
    app.mongodb_client = client
    app.database = database
    print(f"Connected to the {DB_NAME} database")

async def close_mongo_connection(app) -> None:
    client.close()
    print("Disconnected from MongoDB database")