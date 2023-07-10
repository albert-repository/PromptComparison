# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import os
import json


# Set your OpenAI API key
openai.api_key = st.secrets['OPENAI_API_KEY']

def bs_gpt_method(url, input_prompt, model):
    # Download the webpage content
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all text from the webpage
    website_text = soup.get_text().strip().replace('\n\n','')

    # Concatenate website text with the rest of the prompt
    full_prompt = website_text + '\n' + input_prompt

    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
            temperature = 0.7,
            model= model,
            messages=[
                {
                    "role": "user",
                    "content": f"{full_prompt}"
                }
            ]
        )

    # Extract the assistant's reply
    reply = response['choices'][0]['message']['content']
    return reply

def clarity_method(url, input_prompt,model):
    # Download the webpage content
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    prompt = "Provide a 2-3 sentence answer to the query based on the following sources. Be original, concise, accurate, and helpful. Cite sources as [1] or [2] or [3] after each sentence (not just the very end) to back up your answer (Ex: Correct: [1], Correct: [2][3], Incorrect: [1, 2])"
    # Get all text from the webpage
    website_text = soup.get_text().strip().replace('\n\n','')

    # Concatenate website text with the rest of the prompt
    full_prompt = website_text + '\n' + input_prompt + '\n' + prompt

    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
            temperature = 0.7,
            model= model,
            messages=[
                {
                    "role": "user",
                    "content": f"{full_prompt}"
                }
            ]
        )

    # Extract the assistant's reply
    reply = response['choices'][0]['message']['content']
    return reply

def webpilot_method(website, input_prompt):
    url = 'https://preview.webpilotai.com/api/v1/watt'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 5f4f1401dd3f4a559a5f1ff98f6f80c2',  # replace <WebPilot_Issued_Token> with your actual token
    }
    data = {
        "Content": f"{input_prompt} {website}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return(response.json()['content'])

# Create a text area for input and a button
st.title('Comparison Platform')
website = st.text_area("Input website URL", placeholder="https://example.com")
input_prompt = st.text_area("Input prompt", 'What is the summary of the content from example.com?')
generate_button = st.button('Generate Response')

if generate_button:
    with st.spinner("Running Prompts..."):    
        gpt3 = bs_gpt_method(website, input_prompt, 'gpt-3.5-turbo')
        gpt4 = bs_gpt_method(website, input_prompt, 'gpt-4-0314')
        webpilot = webpilot_method(website, input_prompt)
        clarity = clarity_method(website, input_prompt, 'gpt-4-0314')
        
    # Display the reply    

    st.subheader("Results")
    gpt_col1, gpt_col2 = st.columns(2)
    with gpt_col1:
        st.text_area("GPT 3.5 Method Result", gpt3, height = 400)
    with gpt_col2:
        st.text_area("GPT 4 Method Result", gpt4, height = 400)
    bard_col, clarity_col = st.columns(2)
    with bard_col:
        st.text_area("WebPilot API Result", webpilot, height = 400)
    with clarity_col:
        st.text_area("Clarity Method Result", clarity, height = 400)
        


