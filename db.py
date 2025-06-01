def init_db(app):
    app.config['SQL_SERVER'] = os.getenv('DB_SERVER')
    app.config['SQL_DATABASE'] = os.getenv('DB_NAME')
    
    @app.before_request
    def connect_db():
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};" \
                   f"SERVER={app.config['SQL_SERVER']};" \
                   f"DATABASE={app.config['SQL_DATABASE']};" \
                   "Trusted_Connection=yes;"
        g.db = pyodbc.connect(conn_str)
        g.cursor = g.db.cursor()