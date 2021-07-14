--DataBase

--Creazione

--Utenti
CREATE TABLE Utenti(
	id INT PRIMARY KEY,
	username VARCHAR(50),
	password VARCHAR(16),
	nome VARCHAR(100),
	cognome VARCHAR(100),
	email VARCHAR(100),
	dataNascita DATE CHECK (dataNascita < CURRENT_DATE)
);

--Istruttori
CREATE TABLE Istruttori(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES Utenti
);

--Altri
CREATE TABLE Altri(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES Utenti
);

--Clienti
CREATE TABLE Clienti(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES Utenti
);

--Abbonamenti
CREATE TABLE Abbonamenti( --controllare
	id INT PRIMARY KEY,
	tipo VARCHAR(10),
	costo REAL CHECK(costo > 0)
);

--Abbonati
CREATE TABLE Abbonati(
	id INT PRIMARY KEY,
	abbonamento INT NOT NULL,
	dataInizioAbbonamento DATE,
	dataFineAbbonamento DATE,
	FOREIGN KEY(id) REFERENCES Clienti,
	FOREIGN KEY(abbonamento) REFERENCES Abbonamenti,
	CHECK (dataFineAbbonamento > dataInizioAbbonamento)
);

--NonAbbonati
CREATE TABLE NonAbbonati(
	id INT PRIMARY KEY,
	FOREIGN KEY(id) REFERENCES Clienti
);

--Stanze
CREATE TABLE Stanze(
	id INT PRIMARY KEY,
	dimensione INT CHECK(dimensione > 0) --metri quadri
);

--SalePesi
CREATE TABLE SalePesi(
	id INT PRIMARY KEY,
	dimensione INT CHECK(dimensione > 0) --metri quadri
);

--Corsi
CREATE TABLE Corsi(
	id INT PRIMARY KEY,
	nome VARCHAR(100),
	iscrittiMax INT CHECK(iscrittiMax > 0),
	istruttore INT NOT NULL,
	stanza INT NOT NULL,
	FOREIGN KEY(istruttore) REFERENCES Istruttori,
	FOREIGN KEY(stanza) REFERENCES Stanze
);

--Sedute
CREATE TABLE Sedute(
	id INT PRIMARY KEY,
	corso INT NOT NULL,
	dataSeduta TIMESTAMP, --log persone per covid
	FOREIGN KEY(corso) REFERENCES Corsi
);

--AbbonatiSedute
CREATE TABLE AbbonatiSedute(
	abbonato INT,
	seduta INT,
	PRIMARY KEY(abbonato,seduta),
	FOREIGN KEY(abbonato) REFERENCES Abbonati,
	FOREIGN KEY(seduta) REFERENCES Sedute
);

--Giorni
CREATE TABLE Giorni(
	data DATE PRIMARY KEY
);

--Slot
CREATE TABLE Slot(
	id INT PRIMARY KEY,
	personeMax INT CHECK(personeMax > 0),
	giorno DATE,
	oraInizio TIMESTAMP,
	oraFine TIMESTAMP,
	FOREIGN KEY(giorno) REFERENCES Giorni,
	CHECK (oraFine > oraInizio) 
);

--CorsiSlot
CREATE TABLE CorsiSlot(
	corso INT,
	slot INT,
	PRIMARY KEY(corso, slot),
	FOREIGN KEY(corso) REFERENCES Corsi,
	FOREIGN KEY(slot) REFERENCES Slot
);

--SalaPesiSlot
CREATE TABLE SalaPesiSlot(
	salapesi INT,
	slot INT,
	PRIMARY KEY(salapesi, slot),
	FOREIGN KEY(salapesi) REFERENCES SalePesi,
	FOREIGN KEY(slot) REFERENCES Slot
);

--Prenotazioni
CREATE TABLE Prenotazioni( --AbbonatiSlot
	abbonato INT,
	slot INT,
	PRIMARY KEY(abbonato, slot),
	FOREIGN KEY(abbonato) REFERENCES Abbonati,
	FOREIGN KEY(slot) REFERENCES Slot
);