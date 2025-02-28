from django.apps import AppConfig
import os
from django.db import connection

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    
    def ready(self):
        self.load_sql_from_file()

    def load_sql_from_file(self):
        sql_file_path = os.path.join(os.path.dirname(__file__), 'sql\\ui_item_rows.sql')
        if os.path.exists(sql_file_path):
            with open(sql_file_path, 'r') as f:
                sql_script = f.read()

            with connection.cursor() as cursor:
                try:
                    # Execute the SQL directly
                    cursor.execute(sql_script)
                    print("SQL executed successfully")
                except Exception as e:
                    print(f"Error executing SQL: {e}")
        else:
            print("SQL file 'ui_items_rows.sql' not found")
