--DataBase
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
	dataNascita DATE CHECK (dataNascita < CURRENT_DATE)
);

--Istruttori
CREATE TABLE istruttori(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES utenti
);

--Altri
CREATE TABLE altri(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES utenti
);

--Clienti
CREATE TABLE clienti(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES utenti
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
	FOREIGN KEY(id) REFERENCES Clienti,
	FOREIGN KEY(abbonamento) REFERENCES abbonamenti,
	CHECK (datafineabbonamento > datainizioabbonamento)
);

--NonAbbonati
CREATE TABLE nonabbonati(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES clienti
);

--Stanze
CREATE TABLE stanze(
	id INT PRIMARY KEY,
	dimensione INT CHECK(dimensione > 0) --metri quadri
);

--SalePesi
CREATE TABLE salepesi(
	id INT PRIMARY KEY,
	dimensione INT CHECK(dimensione > 0) --metri quadri
);

--Corsi
CREATE TABLE corsi(
	id INT PRIMARY KEY,
	nome VARCHAR(100),
	iscrittimax INT CHECK(iscrittimax > 0),
	istruttore INT NOT NULL,
	stanza INT NOT NULL,
	FOREIGN KEY(istruttore) REFERENCES istruttori,
	FOREIGN KEY(stanza) REFERENCES stanze
);

--Sedute
CREATE TABLE sedute(
	id INT PRIMARY KEY,
	corso INT NOT NULL,
	dataseduta TIMESTAMP, --log persone per covid
	FOREIGN KEY(corso) REFERENCES corsi
);

--AbbonatiSedute
CREATE TABLE abbonatisedute(
	abbonato INT,
	seduta INT,
	PRIMARY KEY(abbonato,seduta),
	FOREIGN KEY(abbonato) REFERENCES abbonati,
	FOREIGN KEY(seduta) REFERENCES sedute
);

--Giorni
CREATE TABLE giorni(
	data DATE PRIMARY KEY
);

--Slot
CREATE TABLE slot(
	id INT PRIMARY KEY,
	personemax INT CHECK(personemax > 0),
	giorno DATE,
	orainizio TIMESTAMP,
	orafine TIMESTAMP,
	FOREIGN KEY(giorno) REFERENCES giorni,
	CHECK (orafine > orainizio) 
);

--CorsiSlot
CREATE TABLE corsislot(
	corso INT,
	slot INT,
	PRIMARY KEY(corso, slot),
	FOREIGN KEY(corso) REFERENCES corsi,
	FOREIGN KEY(slot) REFERENCES slot
);

--SalaPesiSlot
CREATE TABLE salapesislot(
	salapesi INT,
	slot INT,
	PRIMARY KEY(salapesi, slot),
	FOREIGN KEY(salapesi) REFERENCES salepesi,
	FOREIGN KEY(slot) REFERENCES slot
);

--Prenotazioni
CREATE TABLE prenotazioni( --AbbonatiSlot
	abbonato INT,
	slot INT,
	PRIMARY KEY(abbonato, slot),
	FOREIGN KEY(abbonato) REFERENCES abbonati,
	FOREIGN KEY(slot) REFERENCES slot
);