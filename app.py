from flask import Flask, request, jsonify, make_response
import pyodbc
from datetime import datetime
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Function to connect to the SQL Server database
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=MUHAMMAD-HAMZA-;'  # Replace with your server name if needed
            'DATABASE=Matrix1;'
            'Trusted_Connection=yes;'
            'Connection Timeout=30;'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {str(e)}")
        raise

# Home route for testing
@app.route('/')
def home():
    return "Donation API is running!"

# Donation submission endpoint
@app.route('/api/donations', methods=['POST', 'OPTIONS'])
def handle_donations():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()

        # Required fields validation
        required_fields = ['BpName', 'ContactNumber', 'UserRole', 'DonationType']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Parse donation date or set current date
        try:
            donation_date = datetime.strptime(data.get('DonationDate', ''), '%Y-%m-%d')
        except (ValueError, TypeError):
            donation_date = datetime.now()

        # Insert into the database
        with get_db_connection() as conn:
            cursor = conn.cursor()

            sql = """
                INSERT INTO DonationEntry (
                    BpType, BpName, Cnic, ContactNumber, Email, Address, Country, City,
                    UserRole, DonationPurpose, ProjectId, DonationType, Amount,
                    MaterialId, Quantity, MaterialAmount, ServiceId, ServiceHours,
                    PaymentMethod, PaymentReference, DonationDate, Notes,
                    IsActive, CreatedOn, ModifiedOn, CreatedBy, ModifiedBy
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            values = (
                data.get('BpType'),
                data.get('BpName'),
                data.get('Cnic'),
                data.get('ContactNumber'),
                data.get('Email'),
                data.get('Address'),
                data.get('Country'),
                data.get('City'),
                data.get('UserRole'),
                data.get('DonationPurpose'),
                data.get('ProjectId'),
                data.get('DonationType'),
                float(data['Amount']) if data.get('Amount') else None,
                data.get('MaterialId'),
                int(data['Quantity']) if data.get('Quantity') else None,
                float(data['MaterialAmount']) if data.get('MaterialAmount') else None,
                data.get('ServiceId'),
                float(data['ServiceHours']) if data.get('ServiceHours') else None,
                data.get('PaymentMethod'),
                data.get('PaymentReference'),
                donation_date,
                data.get('Notes'),
                1,  # IsActive
                datetime.now(),  # CreatedOn
                datetime.now(),  # ModifiedOn
                'system',  # CreatedBy
                'system'   # ModifiedBy
            )

            cursor.execute(sql, values)
            conn.commit()

            cursor.execute("SELECT SCOPE_IDENTITY()")
            donation_id = cursor.fetchone()[0]

            return jsonify({
                'success': True,
                'message': 'Donation recorded successfully',
                'donationId': donation_id
            }), 201

    except pyodbc.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
