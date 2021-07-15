--Aggiungere durata agli abbonamenti
ALTER TABLE Abbonamenti ADD durata INT NULL CHECK(durata>0);

