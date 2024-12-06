import streamlit as st
import openai
import json
import pandas as pd

st.markdown("""
    <style>
    .stApp 
    {
        font-family: sans-serif;
        font-color: #FFFFFF;             
    }
            
    .stTextArea textarea {
        background-color: #FFFFFF;  
        color: #333333;  
        border: 2px solid #1E90FF; 
        border-radius: 8px;  
        padding: 10px;  
        font-size: 16px; 
    }
            
    .stTextArea label {
        color: #FFFFFF; 
        font-size: 18px;  
        font-weight: bold;  
    }  
       

    .main-title {
        color: #FFFFFF;
        text-align: center;
        font-size: 48px;
        margin-bottom: 20px;
    }
    .description {
        text-align: center;
        color: #FFFFFF;
        margin-bottom: 40px;
        font-size: 18px;
    }
    .input-area textarea {
        font-size: 16px;
    }
    .output-section {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    .response-title {
        color: #FFFFFF;
        font-weight: bold;
    }
            
    .stButton > button {
        background-color: #FFFFFF;  
        color: #0e1117; 
        border-radius: 8px; 
        font-size: 16px; 
        padding: 10px 20px;  
        border-color: #ADD8E6;
    }
    .stButton > button:hover {
        background-color: #0e1117; 
        color: #FFFFFF; 
        border-color: white;
        
    }

    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
<style>
.css-nzvw1x {
    background-color: #061E42 !important;
    background-image: none !important;
}
.css-1aw8i8e {
    background-image: none !important;
    color: #FFFFFF !important
}
.css-ecnl2d {
    background-color: #496C9F !important;
    color: #496C9F !important
}
.css-15zws4i {
    background-color: #496C9F !important;
    color: #FFFFFF !important
}
</style>
""",
    unsafe_allow_html=True
)



user_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API key", type="password")
st.sidebar.markdown("💡 **Hint**: You can get your OpenAI API key from [OpenAI](https://openai.com).")


st.markdown('<h1 class="main-title">Learn Japanese From Passage</h1>', unsafe_allow_html=True)
st.markdown('<p class="description">Input a Japanese passage to get its Thai translation and interesting Japanese words.</p>', unsafe_allow_html=True)


st.markdown('<div class="input-area">', unsafe_allow_html=True)
user_input = st.text_area("📩 Enter your Japanese passage below:", "Your passage here")

if st.button('Submit ✨'):
    if not user_api_key:
        st.error("⚠️ Please enter your OpenAI API key to proceed.")
    else:
        
        client = openai.OpenAI(api_key=user_api_key)
        prompt = """Act as an AI Japanese Teacher. You will receive a 
                    passage and you should translate it into Thai.Then list some intersting words from that passage.
                    
                    Return me JSON array that has 3 fields :
                    1. "Thai translation" - the Thai message that translate form the Japanese message
                    2. "Words" - the list of intersting words from message, in this field each word will have 7 fields :
                    - "Vocabulary" - Japanese vocabulary
                    - "Furigana" - the furigana of that words
                    - "Part of Speech" - the part of speech of that words such as VT, VI, Noun, Adv, Adj
                    - "Meaning" - Meaning of that word in Thai
                    - "Level" - Which JLPT level the word in from JLPT N5 to JLPT N1
                    - "Synonym" - A synonym of that word if it does not have put '-' instead
                    - "Antonym" - An antonym of that word, if it does not have put '-' instead

                    3. "Exams" - make a list of fill-in exams from words in passage. Each exam has only one sentence and not choice exam in this field, it contains 2 fields :
                    - "Exam" - A fill-in exam sentence
                    - "Key" - That answer of the exam

                    Don't say anything at first. Wait for the user to say something.
                """
        
        messages_so_far = [
            {"role": "system", "content": prompt},
            {'role': 'user', 'content': user_input},
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_so_far
        )

        suggestion_dictionary = response.choices[0].message.content
        sd = json.loads(suggestion_dictionary)
        thai_text = sd["Thai translation"]          

        #Thai Translation
        st.markdown('</div>', unsafe_allow_html=True)   
        st.markdown('<h3 class="response-title">คำแปลภาษาไทย:</h3>', unsafe_allow_html=True)
        st.markdown(f"<p>{thai_text}</p>", unsafe_allow_html=True)

        #Vocabularies Table
        st.markdown('</div>', unsafe_allow_html=True)   
        st.markdown('<h3 class="response-title">คำศัพท์:</h3>', unsafe_allow_html=True)
        suggestion_df = pd.DataFrame.from_dict(sd['Words'])
        st.table(suggestion_df)
        st.markdown('</div>', unsafe_allow_html=True)

        #Exam
        st.markdown('<h3 class="response-title">คำถามจากคำศัพท์:</h3>', unsafe_allow_html=True)
        exams = sd['Exams']
        exam_num = 1
        for exam in exams:
            st.write(f"{exam_num}. " + exam['Exam'])
            exam_num += 1
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


        #Key Answer
        st.markdown('<h3 class="response-title">เฉลย:</h3>', unsafe_allow_html=True)
        exams = sd['Exams']
        exam_num = 1
        for exam in exams:
            st.write(f"{exam_num}. " + exam['Key'])
            exam_num += 1
        
        st.markdown('</div>', unsafe_allow_html=True)



        
