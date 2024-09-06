import psycopg2
import logging
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.ERROR)

class PostgreSQLDB:
    def __init__(self, dbname: str, user: str, password: str, host: str = 'cornelius.db.elephantsql.com', port: int = 5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self) -> Optional[psycopg2.extensions.connection]:
        try:
            return psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except psycopg2.Error as e:
            logging.error(f"Connection error: {e}")
            return None

    def drop_table(self):
        try:
            conn = self.connect()
            if conn is not None:
                with conn.cursor() as cursor:
                    cursor.execute("DROP TABLE IF EXISTS agents;")
                    conn.commit()
                logging.info("Table 'agents' dropped successfully.")
        except psycopg2.Error as e:
            logging.error(f"Error dropping table: {e}")
        finally:
            if conn:
                conn.close()

    def create_table(self):
        try:
            conn = self.connect()
            if conn is not None:
                with conn.cursor() as cursor:
                    query = """
                    CREATE TABLE agents (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        description TEXT NOT NULL,
                        category VARCHAR(50),
                        industry VARCHAR(50),
                        pricing_model VARCHAR(20),
                        accessory_model VARCHAR(20),
                        website_url VARCHAR(200),
                        email VARCHAR(150),
                        tagline VARCHAR(255),
                        likes INTEGER DEFAULT 0,
                        overview TEXT,
                        key_features TEXT[],
                        use_cases TEXT[],
                        created_by VARCHAR(255),
                        access VARCHAR(50),
                        tags TEXT[],
                        preview_image VARCHAR(500),
                        logo VARCHAR(500),
                        demo_video VARCHAR(500)
                    );
                    """
                    cursor.execute(query)
                    conn.commit()
                logging.info("Table 'agents' created successfully.")
        except psycopg2.Error as e:
            logging.error(f"Error creating table: {e}")
        finally:
            if conn:
                conn.close()

    def add_agent(self, name: str, description: str, category: str, industry: str, pricing_model: str, accessory_model: Optional[str], website_url: str,email=str, tagline: Optional[str] = None, likes: int = 0, overview: Optional[str] = None, key_features: Optional[List[str]] = None, use_cases: Optional[List[str]] = None, created_by: Optional[str] = None, access: Optional[str] = None, tags: Optional[List[str]] = None, preview_image: Optional[str] = None,logo: Optional[str] = None, demo_video: Optional[str] = None) -> Optional[int]:
        conn = self.connect()
        if conn is not None:
            try:
                with conn.cursor() as cursor:
                    query = """
                    INSERT INTO agents (
                        name, description, category, industry, pricing_model, accessory_model, website_url, email,
                        tagline, likes, overview, key_features, use_cases, created_by, access, tags, 
                        preview_image, logo,demo_video
                    ) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s)
                    RETURNING id;
                    """
                    cursor.execute(query, (
                        name, description, category, industry, pricing_model, accessory_model, website_url,email,
                        tagline, likes, overview, key_features, use_cases, created_by, access,tags,
                        preview_image,logo, demo_video
                    ))
                    new_id = cursor.fetchone()[0]  # Fetch the new ID
                    conn.commit()
                    return new_id
            except psycopg2.Error as e:
                logging.error(f"Error adding agent: {e}")
                return None
            finally:
                conn.close()



                
    def get_agent_by_id(self, agent_id):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "SELECT * FROM agents WHERE id=%s;"
                cursor.execute(query, (agent_id,))
                agent = cursor.fetchone()
                cursor.close()
                conn.close()
                return agent
        except Exception as e:
            print(e)
            return None

    def get_filtered_agents(self, search_query='', category_filter=None, industry_filter=None, pricing_filter=None, accessory_filter=None, sort_option='date_added'):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                
                query = "SELECT * FROM agents WHERE 1=1"
                params = []

                # Apply search filter
                if search_query:
                    query += " AND (name ILIKE %s OR description ILIKE %s)"
                    search_param = f"%{search_query}%"
                    params.extend([search_param, search_param])
                
                # Apply category filter
                if category_filter:
                    query += " AND category = ANY(%s)"
                    params.append(category_filter)
                
                # Apply industry filter
                if industry_filter:
                    query += " AND industry = ANY(%s)"
                    params.append(industry_filter)
                
                # Apply pricing model filter
                if pricing_filter:
                    query += " AND pricing_model = ANY(%s)"
                    params.append(pricing_filter)
                
                # Apply accessory model filter
                if accessory_filter:
                    query += " AND accessory_model = ANY(%s)"
                    params.append(accessory_filter)
                
                # Apply sorting
                if sort_option == 'name_asc':
                    query += " ORDER BY name ASC"
                elif sort_option == 'name_desc':
                    query += " ORDER BY name DESC"
                elif sort_option == 'oldest':
                    query += " ORDER BY date_added ASC"
                else:
                    query += " ORDER BY date_added DESC"

                cursor.execute(query, params)
                agents = cursor.fetchall()
                cursor.close()
                conn.close()
                return agents
        except Exception as e:
            print(e)
            return []

    def update_agent(self, agent_id, name, description, category, industry, pricing_model, accessory_model, website_url,email, tagline=None, likes=0, overview=None, key_features=None, use_cases=None, created_by=None, access=None, tags=None, preview_image=None, demo_video=None):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                UPDATE agents 
                SET name = %s, description = %s, category = %s, industry = %s, pricing_model = %s, accessory_model = %s, 
                    website_url = %s, email=%s,tagline = %s, likes = %s, overview = %s, key_features = %s, 
                    use_cases = %s, created_by = %s, access = %s, tags = %s, preview_image = %s, 
                    demo_video = %s
                WHERE id = %s;
                """
                cursor.execute(query, (
                    name, description, category, industry, pricing_model, accessory_model, website_url,email,
                    tagline, likes, overview, key_features, use_cases, created_by, access, tags,
                    preview_image, demo_video, agent_id
                ))
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
                agents = cursor.fetchall()
                cursor.close()
                conn.close()
                return agents
        except Exception as e:
            print(e)
            return []



    



if __name__ == "__main__":
    db = PostgreSQLDB(dbname='uibmogli', user='uibmogli', password='8ogImHfL_1G249lXtM3k2EAIWTRDH2mX')
    # db.table_creation()
    #db.drop_table()
    db.create_table()
    


   
