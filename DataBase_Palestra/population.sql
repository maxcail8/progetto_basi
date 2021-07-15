--istruttori

INSERT INTO utenti VALUES (1, 'maxcail8', 'p', 'Massimo', 'Cailotto', 'max@palestra.it', DATE '2000-01-07');
INSERT INTO istruttori VALUES (1);

INSERT INTO utenti VALUES (2, 'matteomin', 'p', 'Matteo', 'Minardi', 'matte@palestra.it', DATE '2000-10-04');
INSERT INTO istruttori VALUES (2);

--altri
INSERT INTO utenti VALUES (0, 'admin', 'admin', 'admin', 'admin', 'admin@palestra.it', DATE '1000-01-01');
INSERT INTO altri VALUES (0);

INSERT INTO utenti VALUES (3, 'antonio', 'p', 'Antonio', 'Marenguzzo', 'anto@palestra.it', DATE '1900-04-01');
INSERT INTO altri VALUES (3);

--clienti X

--abbonamenti

INSERT INTO abbonamenti VALUES (0, 'sala_pesi', 30);
INSERT INTO abbonamenti VALUES (1, 'corsi', 40);
INSERT INTO abbonamenti VALUES (2, 'completo', 55);
INSERT INTO abbonamenti VALUES (3, 'prova', 10);

--abbonati X
--nonabbonati X


--stanze
INSERT INTO stanze VALUES (0, 20);
INSERT INTO stanze VALUES (1, 40);
INSERT INTO stanze VALUES (2, 60);
INSERT INTO stanze VALUES (3, 60);


--salepesi
INSERT INTO salepesi VALUES (0, 70);
INSERT INTO salepesi VALUES (1, 80);


--corsi
INSERT INTO corsi VALUES (0, 'pilates', 10, 2, 0);
INSERT INTO corsi VALUES (1, 'yoga', 20, 1, 1);
INSERT INTO corsi VALUES (2, 'crossfit', 30, 2, 2);
INSERT INTO corsi VALUES (3, 'power-lifting', 30, 1, 3);


--sedute (SUBITO O DOPO)


--abbonatisedute (CALENDARIO)


--giorni (SUBITO)
CREATE PROCEDURE LoopGiorni() AS $$
	DECLARE giorno date = CURRENT_DATE;
	BEGIN
		FOR i IN 0..5 LOOP
			INSERT INTO giorni VALUES(giorno);
			giorno = giorno + 1;
		END LOOP;
	END;
$$ LANGUAGE 'plpgsql';

CALL LoopGiorni();


--slot (SUBITO)


--corsislot (SUBITO)


--salepesislot (SUBITO)


--prenotazioni (CALENDARIO)


--
/*
delete from corsi;
delete from salepesi;
delete from stanze;
delete from abbonamenti;
delete from altri;
delete from istruttori;
delete from clienti;
delete from utenti;
*/