--Aggiungere durata agli abbonamenti
ALTER TABLE abbonamenti ADD durata INT NULL CHECK(durata>0);

--Errore: mettere la durata in abbonati
ALTER TABLE abbonamenti DROP durata;
ALTER TABLE abbonati ADD durata INT NULL CHECK(durata>0);

--Cambio TIMESTAMP in TIME slot
ALTER TABLE slot
ALTER COLUMN orainizio TYPE TIME,
ALTER COLUMN orafine TYPE TIME;

--Aggiunta nome stanze
ALTER TABLE stanze ADD nome VARCHAR(100);

--Aggiungere personemq
ALTER TABLE informazioni ADD personemq INT CHECK(personemq > 0);