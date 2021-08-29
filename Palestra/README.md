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

# Modifiche DataBase postgresSQL
# Installazioni ....
Run `flask db init` solo la prima volta, per la creazione della directory migrations.
Run `flask db stamp head` +
Run `flask db migrate` per visualizzare le modifiche che verranno effettuate.
Infine run `flask db upgrade` per confermare le modifiche che verranno effettuate sul database.