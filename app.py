import pandas as pd
import networkx as nx
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

app = Flask(__name__)
app.secret_key = 'PoojyaBhavyaDikshita'

# Load the Excel file containing disease information
df = pd.read_excel(r"Website Codes\Cow Diseases.xlsx", sheet_name="All in one")

# Check if the required columns are present in the dataframe
required_columns = ['Disease', 'Treatment', 'Prevention', 'Causes']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"The '{col}' column is not present in the Excel file.")

# Drop rows where 'Disease' column is NaN
df = df.dropna(subset=['Disease'])

# Collect all symptom columns
symptom_columns = [col for col in df.columns if col.startswith('Symptom')]

# Create a bipartite graph
G = nx.Graph()

# Add nodes and edges from the dataframe to the bipartite graph
for index, row in df.iterrows():
    disease = row['Disease']
    symptoms = row[symptom_columns].dropna().tolist()
    for symptom in symptoms:
        G.add_node(disease, bipartite=0)
        G.add_node(symptom, bipartite=1)
        G.add_edge(disease, symptom)

# Create a dictionary to hold treatment, prevention, symptoms, and causes info
disease_info_dict = df.set_index('Disease')[['Treatment', 'Prevention', 'Causes'] + symptom_columns].to_dict('index')

def diagnose_disease(input_symptoms):
    """
    Diagnose the disease based on input symptoms.
    """
    disease_count = {}
    symptom_matches = {}

    for symptom in input_symptoms:
        if symptom in G:
            connected_diseases = [n for n in G.neighbors(symptom) if G.nodes[n]['bipartite'] == 0]
            for disease in connected_diseases:
                if disease in disease_count:
                    disease_count[disease] += 1
                    symptom_matches[disease].add(symptom)
                else:
                    disease_count[disease] = 1
                    symptom_matches[disease] = {symptom}

    sorted_diseases = sorted(disease_count.items(), key=lambda x: x[1], reverse=True)

    # Calculate accuracy scores for all sorted diseases
    accuracy_scores = {}
    for disease, count in sorted_diseases:
        total_symptoms = sum(pd.notna(df[df['Disease'] == disease][col].values[0]) for col in symptom_columns)
        accuracy_scores[disease] = round((count / total_symptoms) * 100)

    # Find diseases with the highest accuracy score above the threshold
    filtered_diseases = {disease: score for disease, score in accuracy_scores.items() if score > 40}
    highest_accuracy_score = max(filtered_diseases.values(), default=None)
    most_likely_diseases = [disease for disease, score in filtered_diseases.items() if score == highest_accuracy_score]

    return most_likely_diseases, highest_accuracy_score, filtered_diseases

@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('index.html')

@app.route('/symptoms1', methods=['GET', 'POST'])
def symptoms1():
    """
    Handle the symptoms1 form.
    """
    if request.method == 'POST':
        input_symptoms = request.form.getlist('symptoms')
        session['symptoms'] = input_symptoms
        return redirect(url_for('symptoms2'))
    return render_template('symptom1.html')

@app.route('/symptoms2', methods=['GET', 'POST'])
def symptoms2():
    """
    Handle the symptoms2 form.
    """
    if request.method == 'POST':
        input_symptoms = request.form.getlist('symptoms')
        session['symptoms'] = session.get('symptoms', []) + input_symptoms
        return redirect(url_for('symptoms3'))
    return render_template('symptom2.html')

@app.route('/symptoms3', methods=['GET', 'POST'])
def symptoms3():
    """
    Handle the symptoms3 form.
    """
    if request.method == 'POST':
        input_symptoms = request.form.getlist('symptoms')
        session['symptoms'] = session.get('symptoms', []) + input_symptoms
        return redirect(url_for('disease'))

    remaining_symptoms = get_remaining_symptoms()
    return render_template('symptom3.html', remaining_symptoms=remaining_symptoms)

def get_remaining_symptoms():
    """
    Get remaining symptoms for the symptom3 form.
    """
    selected_symptoms = {
        "Foot swelling", "Shoulder swelling", "Neck swelling", "Intestine swelling",
        "Throat swelling", "Peripheral Lymph node swelling", "Chest swelling", "Mouth swelling",
        "Vulva swelling", "Nose swelling", "Hoof swelling", "Udder swelling",
        "Teats swelling", "Uterus swelling", "Left side swelling", "Difficulty standing",
        "Difficulty walking", "Difficulty breathing", "Difficulty in milking", "Reduced milk yield", "Reduced milk quality",
        "Reduced fertility", "Reduced working capacity","Reduced immunity", "Loss of appetite", "Weight loss",
        "Fever", "Weakness", "Bloating", "Aggression", "Lesions", "Lethargy",
        "Nasal discharge", "Blood discharge from openings", "Foul-Smelling Discharge",
        "Eyes discharge", "Foot pain", "Udder pain", "Pain while breast-feeding",
        "Foot redness", "Udder redness", "Wedge shaped skin redness", "Jaundice",
        "Diarrhea", "High heart rate", "Depression", "Udder warmth", "Abortion",
        "Restlessness", "Salivation", "Lack of balance (Ataxia)", "Cold extremities",
        "Weak Pulse", "Uncontrolled body shaking (Seizures)", "Dark red or brown urine",
        "Abnormal milk"
    }
    remaining_symptoms = set()
    for col in symptom_columns:
        remaining_symptoms.update(df[col].dropna().unique())
    remaining_symptoms -= selected_symptoms
    return sorted(remaining_symptoms)

@app.route('/disease')
def disease():
    """
    Diagnose disease based on the symptoms provided.
    """
    input_symptoms = session.get('symptoms', [])
    most_likely_diseases, highest_accuracy_score, filtered_diseases = diagnose_disease(input_symptoms)

    if most_likely_diseases:
        if highest_accuracy_score >= 85:
            top_disease = most_likely_diseases[0]
            diseases_with_scores = [(top_disease, highest_accuracy_score)]
        else:
            sorted_diseases_with_scores = sorted(filtered_diseases.items(), key=lambda x: x[1], reverse=True)[:3]
            disease_names = [disease for disease, score in sorted_diseases_with_scores]
            accuracy_scores = [score for disease, score in sorted_diseases_with_scores]
            diseases_with_scores = zip(disease_names, accuracy_scores)
        
        return render_template('disease.html', diseases_with_scores=diseases_with_scores)
    else:
        return render_template('disease.html', error_message='No disease matched the given symptoms.')

@app.route('/disease_info/<disease_name>')
def disease_info(disease_name):
    """
    Retrieve and display detailed information about a specific disease.
    """
    info = disease_info_dict.get(disease_name)
    if info:
        symptoms = [info[symptom] for symptom in symptom_columns if pd.notna(info[symptom])]
        causes = info['Causes'].split('\n') if pd.notna(info['Causes']) else []
        treatment = info['Treatment'].split('\n') if pd.notna(info['Treatment']) else []
        prevention = info['Prevention'].split('\n') if pd.notna(info['Prevention']) else []
        return render_template('disease_info.html', disease=disease_name, symptoms=symptoms, causes=causes, treatment=treatment, prevention=prevention)
    else:
        return render_template('disease.html', error_message='Disease information not found.')

@app.route('/search_disease', methods=['GET'])
def search_disease():
    """
    Search for diseases based on a query string.
    """
    query = request.args.get('q', '').lower()
    matching_diseases = [disease for disease in df['Disease'] if query in disease.lower()]
    return jsonify(matching_diseases)

@app.route('/all_diseases')
def all_diseases():
    """
    Display all diseases grouped by their first letter.
    """
    return render_template('all_diseases.html')

if __name__ == '__main__':
    app.run(debug=True)
