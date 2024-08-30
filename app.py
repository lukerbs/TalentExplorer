from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
from embedding import get_job_listing_info, word_embedding, exhaustive_search, read_txt, chatgpt
import numpy as np
import json
from pprint import pprint

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Load data
with open('./data/data_2.json', 'r') as json_file:
    data = json.load(json_file)
    employees = data['employees']

profile_urls = [f"{i}: {employees[i]['job_title']}" for i, _ in enumerate(employees)]

JD = read_txt(path='./data/job_description.txt')
job_listing_info = get_job_listing_info(job_listing=JD)
job_embedding = word_embedding(string=JD)

embeddings = np.load('./data/embeddings.npy')

def adjusted_similarity(similarity):
    max_score = 0.60
    if similarity >= max_score:
        similarity = 1.0
    else:
        similarity = similarity/max_score
    similarity = round(similarity,2)
    return similarity

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    job_description = data['job_description']
    job_embedding = word_embedding(string=job_description)

    results = exhaustive_search(target=job_embedding, embeddings=embeddings)
    pprint(results)

    ranked_resumes = []
    for i, _ in enumerate(results):
        if results[i]['similarity'] >= 0.4:
            similarity = adjusted_similarity(similarity=results[i]['similarity'])
            result = {
                "name": employees[results[i]['id']]['name'],
                "photo": employees[results[i]['id']]['pfp'].split('/')[-1],
                "resume": employees[results[i]['id']]['job_title'],
                "id": results[i]['id'],
                "similarity": similarity
            }
            ranked_resumes.append(result)

    if len(ranked_resumes) > 10:
        ranked_resumes = ranked_resumes[:10]

    response = jsonify(ranked_resumes)
    return response

def explaination_prompt(job_description, resume):
    prompt = read_txt('./src/prompts/explanation.txt')
    prompt = prompt.replace("JOB_DESCRIPTION", job_description)
    prompt = prompt.replace("CANDIDATE_RESUME", resume)
    explanation = chatgpt(query=prompt, model='gpt-3.5-turbo')
    return explanation

def qualifications_prompt(job_description, resume):
    prompt = read_txt('./src/prompts/job_qualifications_list.txt')
    prompt = prompt.replace("JOB_DESCRIPTION", job_description)
    prompt = prompt.replace("CANDIDATE_RESUME", resume)
    response = chatgpt(query=prompt, model="gpt-4-turbo")
    json_string = response[response.find("{"):response.rfind("}")+1]
    explanation_json = json.loads(json_string)
    qualifications = explanation_json.get('candidate_qualifications', [])
    return qualifications

@app.route('/api/explain', methods=['POST'])
def explain():
    data = request.get_json()
    idx = data['id']
    job_description = data['job_description']
    resume = read_txt(employees[idx]['description'])

    # Use ThreadPoolExecutor to run both functions concurrently
    with ThreadPoolExecutor() as executor:
        future_qualifications = executor.submit(qualifications_prompt, job_description, resume)
        future_explanation = executor.submit(explaination_prompt, job_description, resume)

        qualifications = future_qualifications.result()
        explanation = future_explanation.result()

    return jsonify({'qualifications': qualifications, 'explanation': explanation})

if __name__ == '__main__':
    app.run(debug=True)