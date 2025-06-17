import speech_recognition as sr
import re
from gpt4all import GPT4All


def clean_transcription(text):
    text = re.sub(r"\bat[\s\-]*the[\s\-]*rate\b", "@", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*@\s*", "@", text)
    return text

def listen_and_transcribe(prompt="🎙️ Speak now:"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print(prompt)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... (you have up to 10 seconds)")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    try:
        raw_text = recognizer.recognize_google(audio)
        return clean_transcription(raw_text)
    except sr.UnknownValueError:
        return "[Could not understand audio]"
    except sr.RequestError as e:
        return f"[Error with speech recognition service: {e}]"


model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")  # auto-loads

def generate_questions(job_desc):
    prompt = f"""
    You are an expert interviewer. Generate 5 concise, job-specific interview questions for: "{job_desc}".
    """
    response = model.generate(prompt, max_tokens=300)
    return [line.strip("- ") for line in response.split("\n") if line.strip()]

def assess_fit(job_desc, qa_pairs):
    qa_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_pairs])
    prompt = f"""
    You are a strict and analytical hiring expert. Based on the following job description and the candidate's responses to the interview questions, assess the candidate's suitability strictly based on their answers.

    Job Description:
    {job_desc}

    Interview Transcript:
    {qa_text}

    Provide a rating from 1 to 10 for job fit and a brief explanation focusing only on relevant qualifications, experience, and alignment with job expectations. Do not infer or assume any missing information.
    """
    return model.generate(prompt, max_tokens=300)


def virtual_interview():
    print("👋 Welcome to the Virtual Interview Assistant\n")
    print("🎯 Please describe the job you're applying for...")
    job_description = listen_and_transcribe("🎙️ Say the job description:")

    print(f"\n📌 Job Description captured: {job_description}")

    # Personal info questions (first)
    personal_questions = [
        "name:",
        "address:",
        "number:",
        "email:"
    ]
    personal_info = {}

    for q in personal_questions:
        print(f"\n🧾 {q}")
        a = listen_and_transcribe("🎙️ Your answer:")
        print(f"✅ You said: {a}")
        personal_info[q.strip(':')] = a

    # Interview questions
    base_questions = [f"What interests you about the role of {job_description}?"]
    job_questions = generate_questions(job_description)
    all_questions = base_questions + job_questions

    answers = []
    for i, question in enumerate(all_questions, 1):
        print(f"\n🧠 Question {i}: {question}")
        answer = listen_and_transcribe("🎙️ Your answer:")
        print(f"✅ You said: {answer}")
        answers.append((question, answer))

    print("\n📄 Interview Transcript:")
    for i, (q, a) in enumerate(answers, 1):
        print(f"\n{i}. Q: {q}\n   A: {a}")

    print("\n🔍 Assessing candidate fit...\n")
    report = assess_fit(job_description, answers)

    # Print personal info with assessment
    print("\n🧾 Candidate Details:")
    for k, v in personal_info.items():
        print(f"{k.capitalize()}: {v}")

    print("\n📊 Candidate Assessment:\n")
    print(report)

if __name__ == "__main__":
    virtual_interview()