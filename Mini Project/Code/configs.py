import psycopg2
def config():
    try:
        return psycopg2.connect(database="postgres",
                            host="aws-0-ap-southeast-1.pooler.supabase.com",
                            user="postgres.gcurjgyrqycujoxguhwl",
                            password="Tarl@576193",
                            port="5432")
    except:
        print("Database Error!!!")
