import json
from pprint import pprint

import openai
import numpy as np

from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


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

	json_string = response[response.find("{") : response.rfind("}") + 1]
	explanation_json = json.loads(json_string)
	qualifications = explanation_json.get('candidate_qualifications', [])
	return qualifications

def summarize_resume(resume):
	prompt = read_txt('./src/prompts/resume_summary.txt')
	prompt = prompt.replace("CANDIDATE_RESUME", resume)
	resume_summary = chatgpt(query=prompt, model='gpt-3.5-turbo')
	return resume_summary

def read_txt(path):
	with open(path, 'r') as file:
		text = file.read()
	return text

def write_txt(text, path):
	with open(path, "w") as file:  # Open the file in write mode
		file.write(text)

def write_to_json(data, path):
	with open(path, "w") as json_file:
	    json.dump(data, json_file, indent=4)

def chatgpt(query: str, model="gpt-4-turbo", max_tokens=None):
    # select model from ['gpt-4o', 'gpt-3.5-turbo', 'gpt-3.5-turbo-instruct', 'gpt-4', 'gpt-4-turbo-preview', 'gpt-4-32k', 'gpt-4-1106-preview']
    completion = openai_client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,  # 4000
        messages=[{"role": "user", "content": query}],
    )
    response = completion.choices[0].message.content
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response


def get_job_title(employees: list[str]):
	for i,_ in enumerate(employees):
		print(f"{i}/{len(employees)}")
		path = employees[i]['description']
		resume = read_txt(path)

		prompt = f"Based on the following resume, what is the person's most recent job title? Only provide the job title in your response.\n\n RESUME:\n{resume}"
		job_title = chatgpt(query=prompt)
		employees[i]['job_title'] = job_title

	return employees

def word_embedding(string):
	response = openai_client.embeddings.create(
		input=string, 
		model="text-embedding-3-large",
		#dimensions=50
		)
	return response.data[0].embedding

def similarity_score(embedding_1, embedding_2):
	similarity = np.dot(embedding_1, embedding_2)
	return similarity

def get_job_listing_info(job_listing: str):
	prompt = f"Based on the following job posting, what is the title of the role being hired. Only return the title in your response.\n\nJOB POSTING:\n'{job_listing}'"
	job_title = chatgpt(query=prompt)

	prompt = f"Create a concise, one paragraph summary of the following job posting.\n\nJOB POSTING:\n'{job_listing}'"
	summary = chatgpt(query=prompt)

	job_info = {
		"title": job_title,
		"overview": summary
	}
	return job_info

def get_employee_embeddings(employees):
	# Get embeddings for employee experiences
	embeddings = []
	for i,_ in enumerate(employees):
		print(f"Getting embedding #{i}")
		txt_file = employees[i]['description']
		experience = read_txt(path=txt_file)
		embedding = word_embedding(string=experience)
		embeddings.append(embedding)

	embeddings = np.array(embeddings)
	save_path = './data/embeddings.npy'
	np.save(save_path, embeddings)
	print(f'Data was saved to {save_path}.')
	return embeddings


"""
TODO:
1. Scrape names for each profile.
2. Generate short description for each profile.

"""

def exhaustive_search(target, embeddings: list):
	scores = []
	for i,_ in enumerate(embeddings):
		similarity = similarity_score(embedding_1=target, embedding_2=embeddings[i])
		data = {
			"id": i,
			"similarity": similarity
		}
		scores.append(data)
	sorted_data = sorted(scores, key=lambda x: x['similarity'], reverse=True)
	return sorted_data

if __name__ == "__main__":
	with open('./data/data_2.json', 'r') as json_file:
		data = json.load(json_file)
		employees = data['employees']

	for i,_ in enumerate(employees):
		print(i)
		resume = read_txt(employees[i]['description'])
		resume_summary = summarize_resume(resume=resume)
		summary_path = f"./data/career_summary/{i}.txt"
		write_txt(text=resume_summary, path=summary_path)
		employees[i]['resume_summary'] = summary_path

	data = {
		"employees": employees
	}
	write_to_json(data=data, path='./data/data_2.json')
	print(f"Data saved to data/career_summary/")
	exit()


	# for employee in employees:
	# 	resume_file = employee["description"]
	# 	resume = read_txt(resume_file)



	# JD = read_txt(path='./data/job_description.txt')
	# job_listing_info = get_job_listing_info(job_listing=JD)
	# job_embedding = word_embedding(string=JD)

	# print('')
	# print(f'{job_listing_info["title"].upper()}:')
	# print(job_listing_info['overview'], '\n')

	# # Load embeddings for employee resumes
	# embeddings = np.load('./data/embeddings.npy')

	# print('ALERT:\nRanking employees for best fit to job description.\n')
	# sorted_data = exhaustive_search(target=job_embedding, samples=embeddings)

	# # Explain why the person is a good fit
	# #prompt = f"Given this the following job description and employee resume, would the employee be a good fit for the job? Explain why or why not in a concise, one paragraph response."
	# prompt = f"Given this the following job description and employee resume, create a bulleted checklist of the job skills and requirements that the employee does and does not have."
	# prompt = f"{prompt}\n\n#JOB DESCRIPTION:\n {JD}"
	# idx = sorted_data[0]['id']
	# print(f'CANDIDATE FOUND:\nCandidate #{idx} is the best fit for the job.\n')

	# # Generate explanation of why the candidate is a good fit.
	# best_profile = read_txt(employees[idx]['description'])
	# prompt = f"{prompt}\n\n#CANDIDATE PROFILE:\n {best_profile}"
	# response = chatgpt(query=prompt)

	# print('EXPLANATION:')
	# print(response, '\n')







