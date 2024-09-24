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
                    cursor.execute("DROP TABLE IF EXISTS agents CASCADE;")
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
                        pricing VARCHAR(20),
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
                        demo_video VARCHAR(500),
                        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_approved BOOLEAN DEFAULT FALSE
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


    def add_agent(self, name: Optional[str] = None, description: Optional[str] = None, 
              category: Optional[str] = None, industry: Optional[str] = None, 
              pricing: Optional[str] = None, accessory_model: Optional[str] = None, 
              website_url: Optional[str] = None, email: Optional[str] = None, 
              tagline: Optional[str] = None, likes: Optional[int] = 0, 
              overview: Optional[str] = None, key_features: Optional[List[str]] = None, 
              use_cases: Optional[List[str]] = None, created_by: Optional[str] = None, 
              access: Optional[str] = None, tags: Optional[List[str]] = None, 
              preview_image: Optional[str] = None, logo: Optional[str] = None, 
              demo_video: Optional[str] = None, is_approved: Optional[bool] = True) -> Optional[int]:
    
         conn = self.connect()
    
         if conn is not None:
            try:
                with conn.cursor() as cursor:
                # Define lists for query fields and values
                     fields = []
                     values = []
                
                # Add only non-null fields to the query
                     if name is not None:
                         fields.append("name")
                         values.append(name)
                     if description is not None:
                         fields.append("description")
                         values.append(description)
                     if category is not None:
                         fields.append("category")
                         values.append(category)
                     if industry is not None:
                         fields.append("industry")
                         values.append(industry)
                     if pricing is not None:
                          fields.append("pricing")
                          values.append(pricing)
                     if accessory_model is not None:
                         fields.append("accessory_model")
                         values.append(accessory_model)
                     if website_url is not None:
                         fields.append("website_url")
                         values.append(website_url)
                     if email is not None:
                         fields.append("email")
                         values.append(email)
                     if tagline is not None:
                         fields.append("tagline")
                         values.append(tagline)
                     if likes is not None:
                         fields.append("likes")
                         values.append(likes)
                     if overview is not None:
                         fields.append("overview")
                         values.append(overview)
                     if key_features is not None:
                         fields.append("key_features")
                         values.append(key_features)
                     if use_cases is not None:
                         fields.append("use_cases")
                         values.append(use_cases)
                     if created_by is not None:
                         fields.append("created_by")
                         values.append(created_by)
                     if access is not None:
                         fields.append("access")
                         values.append(access)
                     if tags is not None:
                         fields.append("tags")
                         values.append(tags)
                     if preview_image is not None:
                         fields.append("preview_image")
                         values.append(preview_image)
                     if logo is not None:
                         fields.append("logo")
                         values.append(logo)
                     if demo_video is not None:
                         fields.append("demo_video")
                         values.append(demo_video)

                # Add the is_approved field (default is False if not provided)
                         fields.append("is_approved")
                         values.append(is_approved)
                
                # Prepare the SQL query dynamically based on provided fields
                     if fields:  # Check if there are fields to insert
                         fields_str = ', '.join(fields)
                         placeholders_str = ', '.join(['%s'] * len(fields))
                
                         query = f"""
                    INSERT INTO agents ({fields_str})
                    VALUES({placeholders_str})
                    RETURNING id;
                    """
                    
                         cursor.execute(query, values)
                         new_id = cursor.fetchone()[0]  # Fetch the new ID
                         conn.commit()
                         return new_id
                     else:
                         logging.error("No fields to insert.")
                         return None
                
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

    def get_filtered_agents(self, search_query='', category_filter=None, industry_filter=None, pricing_filter=None, accessory_filter=None, sort_option='date_added', is_approved=True):
         try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()

            # Base query with is_approved filter
                query = "SELECT * FROM agents WHERE is_approved = %s"
                params = [is_approved]

            # Apply search filter
                if search_query:
                     query += " AND (name ILIKE %s OR description ILIKE %s)"
                     search_param = f"%{search_query}%"
                     params.extend([search_param, search_param])

            # Ensure category_filter is a list if provided
                if category_filter:
                # Convert comma-separated string to list if it's a string
                     if isinstance(category_filter, str):
                        category_filter = category_filter.split(',')

                     if isinstance(category_filter, list) and category_filter:
                         query += " AND category IN %s"
                         params.append(tuple(category_filter))  # Convert list to tuple for SQL IN clause

            # Ensure industry_filter is a list if provided
                if industry_filter:
                     if isinstance(industry_filter, str):
                         industry_filter = industry_filter.split(',')

                     if isinstance(industry_filter, list) and industry_filter:
                         query += " AND industry IN %s"
                         params.append(tuple(industry_filter))

            # Ensure pricing_filter is a list if provided
                if pricing_filter:
                     if isinstance(pricing_filter, str):
                         pricing_filter = pricing_filter.split(',')

                     if isinstance(pricing_filter, list) and pricing_filter:
                         query += " AND pricing IN %s"
                         params.append(tuple(pricing_filter))

            # Ensure accessory_filter is a list if provided
                if accessory_filter:
                     if isinstance(accessory_filter, str):
                         accessory_filter = accessory_filter.split(',')

                     if isinstance(accessory_filter, list) and accessory_filter:
                         query += " AND accessory_model IN %s"
                         params.append(tuple(accessory_filter))

            # Apply sorting
                if sort_option == 'name_asc':
                    query += " ORDER BY name ASC"
                elif sort_option == 'name_desc':
                    query += " ORDER BY name DESC"
                elif sort_option == 'oldest':
                    query += " ORDER BY date_added ASC"
                else:
                    query += " ORDER BY date_added DESC"

            # Execute the query with parameters
                cursor.execute(query, params)
                agents = cursor.fetchall()

                cursor.close()
                conn.close()
                return agents

         except Exception as e:
             print(f"Error: {e}")
             return []


    def update_agent(self, agent_id, name=None, description=None, category=None, industry=None, pricing=None, 
                 accessory_model=None, website_url=None, email=None, tagline=None, likes=0, overview=None, 
                 key_features=None, use_cases=None, created_by=None, access=None, tags=None, 
                 preview_image=None, logo=None, demo_video=None, is_approved=None):
        try:
            conn = self.connect()
            if conn is not None:
                 cursor = conn.cursor()
            
               # Check if the agent exists
                 cursor.execute("SELECT is_approved FROM agents WHERE id = %s;", (agent_id,))
                 agent_data = cursor.fetchone()
            
                 if not agent_data:
                     return f"Agent with ID {agent_id} not found."
            
                 current_is_approved = agent_data[0]
                 if not current_is_approved and is_approved is None:
                     return f"Agent with ID {agent_id} is not approved and cannot be updated."
            
            # Build the query dynamically based on provided parameters
                 fields_to_update = []
                 values = []
            
                 if name:
                     fields_to_update.append("name = %s")
                     values.append(name)
                 if description:
                     fields_to_update.append("description = %s")
                     values.append(description)
                 if category:
                     fields_to_update.append("category = %s")
                     values.append(category)
                 if industry:
                     fields_to_update.append("industry = %s")
                     values.append(industry)
                 if pricing:
                    fields_to_update.append("pricing = %s")
                    values.append(pricing)
                 if accessory_model:
                     fields_to_update.append("accessory_model = %s")
                     values.append(accessory_model)
                 if website_url:
                     fields_to_update.append("website_url = %s")
                     values.append(website_url)
                 if email:
                     fields_to_update.append("email = %s")
                     values.append(email)
                 if tagline:
                     fields_to_update.append("tagline = %s")
                     values.append(tagline)
                 if likes is not None:
                     fields_to_update.append("likes = %s")
                     values.append(likes)
                 if overview:
                     fields_to_update.append("overview = %s")
                     values.append(overview)
                 if key_features:
                     fields_to_update.append("key_features = %s")
                     values.append(key_features)
                 if use_cases:
                     fields_to_update.append("use_cases = %s")
                     values.append(use_cases)
                 if created_by:
                     fields_to_update.append("created_by = %s")
                     values.append(created_by)
                 if access:
                     fields_to_update.append("access = %s")
                     values.append(access)
                 if tags:
                     fields_to_update.append("tags = %s")
                     values.append(tags)
                 if preview_image:
                     fields_to_update.append("preview_image = %s")
                     values.append(preview_image)
                 if logo:
                     fields_to_update.append("logo = %s")
                     values.append(logo)
                 if demo_video:
                     fields_to_update.append("demo_video = %s")
                     values.append(demo_video)
            
            # Add is_approved field if it's provided
                 if is_approved is not None:
                    fields_to_update.append("is_approved = %s")
                    values.append(is_approved)
            
            # If there are fields to update, proceed
                 if fields_to_update:
                     query = f"""
                UPDATE agents 
                SET {', '.join(fields_to_update)}
                WHERE id = %s;
                """
                     values.append(agent_id)  # Add agent_id as the last value
                
                     cursor.execute(query, values)
                     conn.commit()
                     cursor.close()
                     conn.close()
                     return f"Agent with ID {agent_id} updated successfully."
            else:
                return "No fields to update."
    
        except Exception as e:
             print(f"Error updating agent: {e}")
             return "An error occurred while updating the agent."


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
    
    #print(db.get_agent_by_id(2))
    # print(db.get_agent_by_id(3))
    

    
    
    

   
