import importlib
from itertools import product

import pandas as pd
import requests
import transformers
# from transformers import AutoModelForCausalLM
from bs4 import BeautifulSoup


# Define a function to scrape financial reports from a website
def scrape_financial_reports(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find and extract relevant data
    financial_data = {}
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                financial_data[key] = value

    return financial_data

# Scrape financial reports from a list of URLs
financial_reports = []
urls = ['https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm']
total_urls = len(urls)
for i, url in enumerate(urls):
    print(f"Scraping financial report {i+1}/{total_urls} ({(i+1)/total_urls*100:.2f}%): {url}")
    financial_reports.append(scrape_financial_reports(url))

# Convert the scraped data to a pandas DataFrame
print("Converting scraped data to pandas DataFrame...")
financial_data = pd.DataFrame(financial_reports)

# Load pre-trained model
# model_name = "anon8231489123/vicuna-13b-GPTQ-4bit-128g"
# model_name = "decapoda-research/llama-7b-hf"
model_name = "maciek-pioro/llama-fixed-tokenizer"
print(f"Loading pre-trained model: {model_name}...")
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
model = transformers.AutoModelForCausalLM.from_pretrained(model_name)

# Fine-tune model on financial data
print("Fine-tuning model on financial data...")
input_ids = tokenizer.encode(financial_data['text'], return_tensors='pt')
outputs = model(input_ids, labels=input_ids)
loss = outputs.loss
loss.backward()

def generate_summary(financial_data, model):
    input_text = f"Generate a summary of the following financial data: {financial_data}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    outputs = model.generate(input_ids, max_length=200, do_sample=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

# Generate summaries and analysis for each financial report
total_reports = len(financial_reports)
print("Generating summaries and analysis for financial reports...")
for i, report in enumerate(financial_reports):
    print(f"Processing report {i+1}/{total_reports} ({(i+1)/total_reports*100:.2f}%)")
    summary = generate_summary(report, model)
    print(summary)
