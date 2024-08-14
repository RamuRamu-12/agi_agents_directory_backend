import psycopg2

class PostgreSQLDB:
    def __init__(self, dbname, user, password, host='cornelius.db.elephantsql.com', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except Exception as e:
            print(e)
            return None

    def table_creation(self):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                CREATE TABLE IF NOT EXISTS agents (
                  id SERIAL PRIMARY KEY,
                  name VARCHAR(255) NOT NULL, 
                  description TEXT NOT NULL,
                  category VARCHAR(50) NOT NULL,
                  industry VARCHAR(50) NOT NULL,
                  pricing_model VARCHAR(20) NOT NULL,
                  accessory_model VARCHAR(20) NOT NULL,
                  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  website_url VARCHAR(200)
                );
                """
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def add_agent(self, name, description, category, industry, pricing_model, accessory_model, website_url):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                INSERT INTO agents (name, description, category, industry, pricing_model, accessory_model, website_url) 
                VALUES(%s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, (name, description, category, industry, pricing_model, accessory_model, website_url))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def get_agent_data(self, agent_id):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "SELECT * FROM agents WHERE id=%s;"
                cursor.execute(query, (agent_id,))
                res = cursor.fetchone()
                cursor.close()
                conn.close()
                return res
        except Exception as e:
            print(e)

    def update_agent(self, agent_id, name, description, category, industry, pricing_model, accessory_model, website_url):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                UPDATE agents 
                SET name = %s, description = %s, category = %s, industry = %s, pricing_model = %s, accessory_model = %s, website_url = %s
                WHERE id = %s;
                """
                cursor.execute(query, (name, description, category, industry, pricing_model, accessory_model, website_url, agent_id))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def delete_agent(self, agent_id):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "DELETE FROM agents WHERE id=%s;"
                cursor.execute(query, (agent_id,))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def get_all_agents(self):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "SELECT * FROM agents;"
                cursor.execute(query)
                res = cursor.fetchall()
                cursor.close()
                conn.close()
                return res
        except Exception as e:
            print(e)

if __name__ == "__main__":
    db = PostgreSQLDB(dbname='uibmogli', user='uibmogli', password='8ogImHfL_1G249lXtM3k2EAIWTRDH2mX')
    db.table_creation()
    
    # Add an agent
    db.add_agent('Agent Name', 'Description of the agent', 'Category', 'Industry', 'Pricing Model', 'Accessory Model', 'https://example.com')
    
    # Retrieve an agent's data
    print(db.get_agent_data(1))  # Fetch agent with ID 1
    
    # Update an agent's data
    #db.update_agent(1, 'Updated Name', 'Updated Description', 'Updated Category', 'Updated Industry', 'Updated Pricing Model', 'Updated Accessory Model', 'https://updated-example.com')
    
    # Delete an agent
   # db.delete_agent(1)
    
    # Get all agents
   # print(db.get_all_agents())
