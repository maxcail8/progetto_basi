--DataBase 'progetto_palestra'
--Creazione
ALTER USER postgres PASSWORD 'postgres';

--Utenti
CREATE TABLE utenti(
	id INT PRIMARY KEY,
	username VARCHAR(50),
	password VARCHAR(16),
	nome VARCHAR(100),
	cognome VARCHAR(100),
	email VARCHAR(100),
	datanascita DATE CHECK (datanascita < CURRENT_DATE)
);

--Istruttori
CREATE TABLE istruttori(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES utenti ON DELETE CASCADE
);

--Altri
CREATE TABLE altri(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES utenti ON DELETE CASCADE
);

--Clienti
CREATE TABLE clienti(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES utenti ON DELETE CASCADE
);

--Abbonamenti
CREATE TABLE abbonamenti( --controllare
	id INT PRIMARY KEY,
	tipo VARCHAR(10),
	costo REAL CHECK(costo > 0)
);

--Abbonati
CREATE TABLE abbonati(
	id INT PRIMARY KEY,
	abbonamento INT NOT NULL,
	datainizioabbonamento DATE,
	datafineabbonamento DATE,
	durata INT CHECK(durata > 0), --giorni di durata
	FOREIGN KEY(id) REFERENCES clienti ON DELETE CASCADE,
	FOREIGN KEY(abbonamento) REFERENCES abbonamenti ON DELETE CASCADE,
	CHECK (datafineabbonamento > datainizioabbonamento)
);

--NonAbbonati
CREATE TABLE nonabbonati(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES clienti ON DELETE CASCADE
);

--Stanze
CREATE SEQUENCE stanze_id_seq;
CREATE TABLE stanze(
	id smallint NOT NULL DEFAULT nextval('stanze_id_seq'),
	nome VARCHAR(100),
	dimensione INT CHECK(dimensione > 0), --metri quadri
	PRIMARY KEY(id)
);
ALTER SEQUENCE stanze_id_seq OWNED BY stanze.id;

--SalePesi
CREATE SEQUENCE salepesi_id_seq;
CREATE TABLE salepesi(
	id smallint NOT NULL DEFAULT nextval('salepesi_id_seq'),	
	dimensione INT CHECK(dimensione > 0), --metri quadri
	iscrittimax INT CHECK(iscrittimax > 0),
	PRIMARY KEY(id)
);
ALTER SEQUENCE salepesi_id_seq OWNED BY salepesi.id;

--Corsi
CREATE SEQUENCE corsi_id_seq;
CREATE TABLE corsi(
	id smallint NOT NULL DEFAULT nextval('corsi_id_seq'),
	nome VARCHAR(100),
	iscrittimax INT CHECK(iscrittimax > 0),
	istruttore INT NOT NULL,
	stanza INT NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(istruttore) REFERENCES istruttori ON DELETE SET NULL,
	FOREIGN KEY(stanza) REFERENCES stanze ON DELETE CASCADE
);
ALTER SEQUENCE corsi_id_seq OWNED BY corsi.id;

--Sedute
CREATE TABLE sedute(
	id INT PRIMARY KEY,
	corso INT NOT NULL,
	dataseduta TIMESTAMP, --log persone per covid
	FOREIGN KEY(corso) REFERENCES corsi ON DELETE CASCADE
);

--AbbonatiSedute
CREATE TABLE abbonatisedute(
	abbonato INT,
	seduta INT,
	PRIMARY KEY(abbonato,seduta),
	FOREIGN KEY(abbonato) REFERENCES abbonati ON DELETE CASCADE,
	FOREIGN KEY(seduta) REFERENCES sedute ON DELETE CASCADE
);

--Giorni
CREATE TABLE giorni(
	data DATE PRIMARY KEY
);

--Slot
CREATE SEQUENCE slot_id_seq;
CREATE TABLE slot(
	id smallint NOT NULL DEFAULT nextval('slot_id_seq'),
	personemax INT CHECK(personemax > 0),
	giorno DATE,
	orainizio TIME,
	orafine TIME,
	PRIMARY KEY(id),
	FOREIGN KEY(giorno) REFERENCES giorni ON DELETE CASCADE,
	CHECK (orafine > orainizio) 
);
ALTER SEQUENCE slot_id_seq OWNED BY slot.id;

--CorsiSlot
CREATE TABLE corsislot(
	corso INT,
	slot INT,
	iscrittimax INT,
	PRIMARY KEY(corso, slot),
	FOREIGN KEY(corso) REFERENCES corsi ON DELETE CASCADE,
	FOREIGN KEY(slot) REFERENCES slot ON DELETE CASCADE
);

--SalaPesiSlot
CREATE TABLE salapesislot(
	salapesi INT,
	slot INT,
	iscrittimax INT,
	PRIMARY KEY(salapesi, slot),
	FOREIGN KEY(salapesi) REFERENCES salepesi ON DELETE CASCADE,
	FOREIGN KEY(slot) REFERENCES slot ON DELETE CASCADE
);

--Prenotazioni
CREATE TABLE prenotazioni( --AbbonatiSlot
	abbonato INT,
	slot INT,
	PRIMARY KEY(abbonato, slot),
	FOREIGN KEY(abbonato) REFERENCES abbonati ON DELETE CASCADE,
	FOREIGN KEY(slot) REFERENCES slot ON DELETE CASCADE
);

--Informazioni
CREATE TABLE informazioni(
	accessisettimana INT CHECK(accessisettimana > 0),
	slotgiorno INT CHECK(slotgiorno > 0 AND slotgiorno < 6),
	personemaxslot INT CHECK(personemaxslot > 0),
	personemq INT CHECK(personemq > 0),
	PRIMARY KEY(accessisettimana, slotgiorno, personemaxslot, personemq)
);

CREATE TABLE controlli(
	controllo INT CHECK(controllo >= 0),
	PRIMARY KEY(controllo)
);