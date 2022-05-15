import sqlite3

############# IMPORTANT FUNCTIONS #############

def update_db(job_title, job_employer, job_location, job_lang, job_exp_req,job_link):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)",(job_title, job_employer, job_location, job_lang, job_exp_req, job_link))
    conn.commit()
    conn.close()

def parse_data(job_description):
    job_description = job_description.lower()

    job_lang = ""
    language = ["python","sql","html","css","javascript","typescript","c++","c#"]
    for item in language:
        if item in job_description:
            job_lang = job_lang + item + ", "
    
    job_exp_req = ""
    descrip_sentences = (job_description.split('\n'))
    for sentence,i in zip(descrip_sentences, range(len(descrip_sentences))):
        if ('experience' or 'year') in sentence:
            job_exp_req = sentence.strip() + descrip_sentences[i+1] + descrip_sentences[i+2]
    return job_lang, job_exp_req


# ########### SETUP/RESET CODE #############
# conn = sqlite3.connect('jobs.db')
# c = conn.cursor()

# c.execute("DROP TABLE jobs")

# c.execute("""CREATE TABLE jobs(
#     title text,
#     employer text,
#     location text,
#     language text,
#     required_experience text,
#     link text,
#     UNIQUE(link) ON CONFLICT IGNORE
# )""")

# conn.commit()
# conn.close()