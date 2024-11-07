import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import random 

def init_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # Usa le credenziali JSON dai secrets di Streamlit e assicuriamoci che sia un dizionario
    creds_dict = st.secrets["google_sheets"]["credentials_json"]
    if isinstance(creds_dict, str):  # Se è una stringa, convertiamola in un dizionario
        creds_dict = json.loads(creds_dict)
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # Nome del foglio Google specificato per il progetto
    return client.open("Dati Partecipanti").sheet1  # Assicurati che il nome del foglio sia corretto

# Inizializza il Google Sheet
sheet = init_google_sheet()


# Definizione delle frasi
target_phrases = [
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2025-05-13 sarà più basso rispetto alla data 2025-04-27.", "feedback": "Di questa frase non sappiamo se è vera o falsa"},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2025-05-11 sarà più basso rispetto alla data 2025-05-12.", "feedback": "Di questa frase non sappiamo se è vera o falsa"},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2025-02-01 sarà più alto rispetto alla data 2025-01-28.", "feedback": "Di questa frase non sappiamo se è vera o falsa"}
]

control_phrases = [
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2025-04-27 sarà più basso rispetto alla data 2025-05-13.", "feedback": "Di questa frase non sappiamo se è vera o falsa"},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2025-05-11 sarà più alto rispetto alla data 2025-05-15.", "feedback": "Di questa frase non sappiamo se è vera o falsa"},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2025-01-28 sarà più alto rispetto alla data 2025-02-01.", "feedback": "Di questa frase non sappiamo se è vera o falsa"}
]

test_phrases = [
    # Frasi di Test Vere
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2023-03-15 era più alto rispetto alla data 2023-03-10.", "corretta": True},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2023-06-20 era più basso rispetto alla data 2023-06-21.", "corretta": True},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2022-12-01 era più basso rispetto alla data 2022-12-05.", "corretta": True},
    {"frase": "Tesla Inc. (TSLA): Il titolo in data 2022-09-14 era più alto rispetto alla data 2022-09-12.", "corretta": True},
    {"frase": "Alphabet Inc. (GOOGL): Il titolo in data 2023-02-20 era più alto rispetto alla data 2023-02-18.", "corretta": True},
    {"frase": "Meta Platforms Inc. (META): Il titolo in data 2023-01-15 era più basso rispetto alla data 2023-01-18.", "corretta": True},
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2022-11-22 era più basso rispetto alla data 2022-11-25.", "corretta": True},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2022-07-10 era più alto rispetto alla data 2022-07-08.", "corretta": True},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2023-04-12 era più basso rispetto alla data 2023-04-15.", "corretta": True},
    {"frase": "Tesla Inc. (TSLA): Il titolo in data 2022-10-01 era più alto rispetto alla data 2022-09-28.", "corretta": True},
    {"frase": "Alphabet Inc. (GOOGL): Il titolo in data 2022-08-30 era più basso rispetto alla data 2022-08-31.", "corretta": True},
    {"frase": "Meta Platforms Inc. (META): Il titolo in data 2023-05-01 era più alto rispetto alla data 2023-04-28.", "corretta": True},
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2022-06-18 era più basso rispetto alla data 2022-06-20.", "corretta": True},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2023-03-05 era più alto rispetto alla data 2023-03-03.", "corretta": True},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2022-11-30 era più basso rispetto alla data 2022-12-01.", "corretta": True},
    
    # Frasi di Test False
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2023-03-10 era più alto rispetto alla data 2023-03-15.", "corretta": False},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2023-06-21 era più basso rispetto alla data 2023-06-20.", "corretta": False},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2022-12-05 era più basso rispetto alla data 2022-12-01.", "corretta": False},
    {"frase": "Tesla Inc. (TSLA): Il titolo in data 2022-09-12 era più alto rispetto alla data 2022-09-14.", "corretta": False},
    {"frase": "Alphabet Inc. (GOOGL): Il titolo in data 2023-02-18 era più alto rispetto alla data 2023-02-20.", "corretta": False},
    {"frase": "Meta Platforms Inc. (META): Il titolo in data 2023-01-18 era più basso rispetto alla data 2023-01-15.", "corretta": False},
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2022-11-25 era più basso rispetto alla data 2022-11-22.", "corretta": False},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2022-07-08 era più alto rispetto alla data 2022-07-10.", "corretta": False},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2023-04-15 era più basso rispetto alla data 2023-04-12.", "corretta": False},
    {"frase": "Tesla Inc. (TSLA): Il titolo in data 2022-09-28 era più alto rispetto alla data 2022-10-01.", "corretta": False},
    {"frase": "Alphabet Inc. (GOOGL): Il titolo in data 2022-08-31 era più basso rispetto alla data 2022-08-30.", "corretta": False},
    {"frase": "Meta Platforms Inc. (META): Il titolo in data 2023-04-28 era più alto rispetto alla data 2023-05-01.", "corretta": False},
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2022-06-20 era più basso rispetto alla data 2022-06-18.", "corretta": False},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2023-03-03 era più alto rispetto alla data 2023-03-05.", "corretta": False},
    {"frase": "Amazon.com Inc. (AMZN): Il titolo in data 2022-12-01 era più basso rispetto alla data 2022-11-30.", "corretta": False}
]


# Funzione per registrare i risultati su Google Sheet
def save_results(participant_id, email, responses, total_correct):
    row = [participant_id, email]  # Aggiungi l'email nella prima posizione del foglio
    for response in sorted(responses, key=lambda x: x["frase"]):  # Ordina alfabeticamente le frasi
        row.append(response["frase"])
        row.append(response["risposta"])
        row.append(response["feedback"])
    row.append(total_correct)
    sheet.append_row(row)

# Funzione principale dell'app
def main():
    st.title("Test di Valutazione delle Frasi")
    participant_id = st.text_input("Inserisci il tuo ID partecipante")
    email = st.text_input("Inserisci la tua email")  # Casella per inserire l'email
    
    if participant_id and email:
        # Mescola le frasi
        all_phrases = target_phrases + control_phrases + test_phrases
        random.shuffle(all_phrases)
        
        responses = []
        total_correct = 0

        # Ciclo per mostrare ciascuna frase
        for phrase in all_phrases:
            st.write("La frase è nascosta dietro un pannello nero.")
            st.write("Rispondi se pensi che sia vera o falsa:")
            
            if "corretta" in phrase:  # Frase di test
                risposta = st.radio("La frase è:", ("Vera", "Falsa"))
                is_correct = (risposta == "Vera") == phrase["corretta"]
                feedback = "Giusto" if is_correct else "Sbagliato"
                responses.append({"frase": phrase["frase"], "risposta": risposta, "feedback": feedback})
                if is_correct:
                    total_correct += 1
                st.write(feedback)
            else:  # Frase target o di controllo
                risposta = st.radio("La frase è:", ("Vera", "Falsa"))
                responses.append({"frase": phrase["frase"], "risposta": risposta, "feedback": phrase["feedback"]})
                st.write(phrase["feedback"])

        # Salva i risultati alla fine della sessione
        if st.button("Termina e salva risultati"):
            save_results(participant_id, email, responses, total_correct)
            st.write("Risultati salvati con successo!")

if __name__ == "__main__":
    main()
