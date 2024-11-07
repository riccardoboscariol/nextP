import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import random

# Funzione per l'inizializzazione e autenticazione di Google Sheets
def init_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds_dict = st.secrets["google_sheets"]["credentials_json"]
    if isinstance(creds_dict, str):  # Se è una stringa, convertila in dizionario
        creds_dict = json.loads(creds_dict)
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    
    client = gspread.authorize(creds)
    return client.open("Dati Partecipanti").sheet1

# Inizializza Google Sheet
sheet = init_google_sheet()

# Definizione delle frasi target e di controllo
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

# Definizione delle frasi di test con 15 frasi vere e 15 frasi false
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

# Funzione per salvare i risultati di una singola risposta
def save_single_response(participant_id, email, frase, risposta, feedback):
    sheet.append_row([participant_id, email, frase, risposta, feedback])

# Funzione principale dell'app
def main():
    st.title("Test di Valutazione delle Frasi")

    # Input per l'ID partecipante e l'email
    participant_id = st.text_input("Inserisci il tuo ID partecipante")
    email = st.text_input("Inserisci la tua email")

    if participant_id and email and st.button("Inizia il Test"):
        # Imposta le variabili session_state per iniziare il test
        st.session_state.participant_id = participant_id
        st.session_state.email = email
        st.session_state.all_phrases = target_phrases + control_phrases + test_phrases
        random.shuffle(st.session_state.all_phrases)
        st.session_state.current_index = 0
        st.session_state.total_correct = 0
        st.experimental_rerun()

    # Verifica se il test è iniziato
    if "all_phrases" in st.session_state:
        # Seleziona la frase corrente
        current_phrase = st.session_state.all_phrases[st.session_state.current_index]
        
        # Mostra la domanda senza risposta di default
        risposta = st.radio("La frase è:", ("Seleziona", "Vera", "Falsa"), index=0, key=f"response_{st.session_state.current_index}")
        
        # Mostra la frase nascosta e richiede una risposta
        st.write("La frase è nascosta dietro un pannello nero.")
        st.write("Rispondi se pensi che sia vera o falsa:")

        if risposta != "Seleziona":
            # Verifica la correttezza e genera feedback
            if "corretta" in current_phrase:  # Frase di test
                is_correct = (risposta == "Vera") == current_phrase["corretta"]
                feedback = "Giusto" if is_correct else "Sbagliato"
                if is_correct:
                    st.session_state.total_correct += 1
            else:  # Frase target o di controllo
                feedback = current_phrase["feedback"]

            # Salva la risposta per la frase corrente
            save_single_response(st.session_state.participant_id, st.session_state.email, current_phrase["frase"], risposta, feedback)
            st.write(feedback)

            # Passa alla domanda successiva
            st.session_state.current_index += 1
            
            # Se tutte le domande sono state completate
            if st.session_state.current_index >= len(st.session_state.all_phrases):
                st.write("Test completato!")
                st.write(f"Risposte corrette (test): {st.session_state.total_correct} su {len(test_phrases)}")
                st.stop()
            else:
                st.experimental_rerun()

if __name__ == "__main__":
    main()

