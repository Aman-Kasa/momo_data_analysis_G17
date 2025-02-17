import flask
from flask_cors import CORS
from flask import request, jsonify
import subprocess
import os
import dotenv
import MySQLdb
import json
from datetime import timedelta

# Load environment variables from a .env file
dotenv.load_dotenv()

app = flask.Flask(__name__)
CORS(app)

@app.route('/file', methods=['POST'])
def file():
    try:
        file = request.data.decode('utf-8')
        print(file)
        if file:
            with open('modified_sms_v2.xml', 'w') as f:
                f.write(file)
            list_of_subprocesses = [
                "sh prepare_me.sh",
                "python3 Categorizer.py",
                "python3 Cleaner.py",
                "python3 Db_saver.py"
            ]

            for subprocess_command in list_of_subprocesses:
                print(subprocess_command)
                result = subprocess.run(subprocess_command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Error running {subprocess_command}: {result.stderr}")
                    return jsonify({"error": f"Error running {subprocess_command}: {result.stderr}"}), 500
            print("Done")
            return jsonify({"message": "File processed successfully"}), 200
        else:
            print("No file uploaded")
            return jsonify({"error": "No file uploaded"}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/database_return', methods=['GET'])
def db_return():
    try:
        # Check if required environment variables are set
        required_env_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWD', 'DB']
        for var in required_env_vars:
            if not os.getenv(var):
                raise ValueError(f"Environment variable {var} is not set")

        # Connect to the MySQL database
        conn = MySQLdb.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            passwd=os.getenv('MYSQL_PASSWD'),
            db=os.getenv('DB')
        )
        cursor = conn.cursor()
        sql_statements = [
            "SELECT * FROM airtime",
            "SELECT * FROM bundles",
            "SELECT * FROM cashpower",
            "SELECT * FROM codeholders",
            "SELECT * FROM deposit",
            "SELECT * FROM failedtransactions",
            "SELECT * FROM incomingmoney",
            "SELECT * FROM nontransaction",
            "SELECT * FROM payments",
            "SELECT * FROM reversedtransactions",
            "SELECT * FROM thirdparty",
            "SELECT * FROM transfer",
            "SELECT * FROM withdraw"
        ]

        results = {}
        for statement in sql_statements:
            cursor.execute(statement)
            table_name = statement.split()[3]
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            rows = [
                {columns[i]: str(item) if isinstance(item, timedelta) else item for i, item in enumerate(row)}
                for row in rows
            ]
            results[table_name] = rows

        cursor.close()
        conn.close()
        return jsonify({"data": results}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)