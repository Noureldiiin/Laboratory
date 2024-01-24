from flask import Flask, render_template, request, redirect, url_for
import redis
import uuid

app = Flask(__name__)
redis_client = redis.StrictRedis(host='redis-18276.c304.europe-west1-2.gce.cloud.redislabs.com',
                                port=18276, password='123456', decode_responses=True)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/patient_list')
def index():
    return render_template('patient_list.html', patients=get_all_patients())

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        patient_details = request.form['patient_details']
        add_patient(patient_name, patient_details)
        return redirect(url_for('index'))
    return render_template('add_patient.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        matching_patients = search_patients(search_term)
        return render_template('patient_list.html', patients=matching_patients, search_term=search_term)
    return redirect(url_for('index'))

@app.route('/reset_search')
def reset_search():
    return redirect(url_for('index'))

# Helper functions
def add_patient(patient_name, patient_details):
    patient_id = str(uuid.uuid4())
    key = f'patient:{patient_id}'
    redis_client.hmset(key, {'name': patient_name, 'details': patient_details})

def get_all_patients():
    keys = redis_client.keys('patient:*')
    patients = []
    for key in keys:
        patient = redis_client.hgetall(key)
        patients.append({'id': key.split(':')[-1], 'name': patient['name'], 'details': patient['details']})
    return patients

def search_patients(search_term):
    keys = redis_client.keys('patient:*')
    matching_patients = []
    for key in keys:
        patient = redis_client.hgetall(key)
        if search_term.lower() in patient['name'].lower() or search_term.lower() in patient['details'].lower():
            matching_patients.append({'id': key.split(':')[-1], 'name': patient['name'], 'details': patient['details']})
    return matching_patients

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
