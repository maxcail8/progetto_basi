# Developed by
Massimo Cailotto, Matteo Minardi

# Settaggio parametri applicazione
Parametri USER
utente: 'postgres'
password: 'postgres'

# Run applicazione
# Installazioni ....
Run `set FLASK_APP=project.py` per settare la flask-app.
Run `flask run` per eseguire l'applicazione. Navigare a `http://localhost:5000/` (equivalentemente `http://127.0.0.1:5000/`).

Eseguire il progetto con:
	set FLASK_APP=project.py
seguito da:
	flask run


I file SQL contenenti la creazione delle tabelle, dei triggers e della popolazione iniziale sono contenuti nella cartella “pgadmin_file”.
Oltre a creare le tabelle della base di dati ed ad inserire i vari triggers e le relative funzioni in pgadmin, permettono di aggiungere, tra le varie cose, alcune informazioni, abbonamenti e stanze utili per avere qualche dato iniziare per l’utilizzo dell’applicazione.
Consigliamo di aggiungere immediatamente dei corsi, con i relativi istruttori, e delle sale pesi in modo da poter avere delle attività a cui i clienti potranno iscriversi. 

Inoltre bisognerebbe eseguire i trigger della pagina di amministrazione in questo ordine: 
	1. Controlli giornalieri, meno utile al primo avvio perchè i dati vengono tutti generati 
                                               alla generazione delle varie attività ma diventa fondamentale in 
                                               futuro per mantenere le diverse funzionalità attive
            2.  Modifica mq minimi, in modo che automaticamente si generino dei limiti dentro i 
                                                  quali è garantita la sicurezza per gli utenti della palestra
            3.  Modifica persone massime slot, se si vuole inserire un numero diverso da quello 
                                                                    generato precedentemente in automatico
Gli altri due trigger riguardanti il numero massimo di accessi giornalieri e settimanali possono essere eseguiti in ordine qualsiasi.

# Modifiche DataBase postgresSQL
# Installazioni
Run `flask db init` solo la prima volta, per la creazione della directory migrations.
Run `flask db stamp head` +
Run `flask db migrate` per visualizzare le modifiche che verranno effettuate.
Infine run `flask db upgrade` per confermare le modifiche che verranno effettuate sul database.