import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# Configura l'accesso a Google Sheets
def init_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open("Nome del Tuo Google Sheet").sheet1  # Sostituisci con il nome del tuo Google Sheet

# Inizializza Google Sheet
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
    {"frase": "Apple Inc. (AAPL): Il titolo in data 2023-03-15 era più alto rispetto alla data 2023-03-10.", "corretta": True},
    {"frase": "Microsoft Corp. (MSFT): Il titolo in data 2023-06-21 era più basso rispetto alla data 2023-06-20.", "corretta": False},
    # Aggiungi le altre 28 frasi di test con 'corretta': True/False
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