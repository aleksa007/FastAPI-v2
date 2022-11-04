while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi-v2', user='postgres', password='Vodavoda1', 
        cursor_factory=RealDictCursor) #RealDict is for colomn names (without it it wont retrive columns)
        cursor= conn.cursor() #Used to execute SQL querees
        print("Success Connection")
        break
    except Exception as error:
        print("Failed")
        