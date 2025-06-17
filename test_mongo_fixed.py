from pymongo import MongoClient

# Let's try different URI formats
username = "pranavbhadaneiitkgp"
password = "1234567890"

# Try the full cluster URI from your config
uri1 = "mongodb+srv://pranavbhadaneiitkgp:1234567890@cluster0.ldzbfiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Alternative format
uri2 = f"mongodb+srv://{username}:{password}@cluster0.ldzbfiu.mongodb.net/smartneed?retryWrites=true&w=majority"

print("🔗 Testing MongoDB Atlas connection...")
print(f"URI: {uri1[:50]}...")

for i, uri in enumerate([uri1, uri2], 1):
    try:
        print(f"\n🧪 Test {i}: Connecting...")
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print(f"✅ Test {i}: Connection successful!")
        
        # Test database access
        db = client.smartneed
        print(f"📊 Database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📋 Collections: {collections}")
        
        client.close()
        break
        
    except Exception as e:
        print(f"❌ Test {i}: Connection failed - {e}")

print("\n🔍 If all tests failed, check:")
print("1. MongoDB Atlas cluster is running")
print("2. Your IP is whitelisted")
print("3. Username/password are correct")
print("4. Network connection is stable")
