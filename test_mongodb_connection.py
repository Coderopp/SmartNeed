from pymongo import MongoClient

username = "pranavbhadaneiitkgp"
password = "1234567890"  # encode if it contains special characters
uri = f"mongodb+srv://{username}:{password}@cluster0.mongodb.net/?retryWrites=true&w=majority"

print("🔗 Connecting to MongoDB Atlas...")
client = MongoClient(uri)

# Test
try:
    client.admin.command('ping')
    print("✅ Connection successful!")
except Exception as e:
    print("❌ Connection failed:", e)
