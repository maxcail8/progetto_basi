--infomazioni
INSERT INTO informazioni VALUES (4, 2, 30, 2);

INSERT INTO controlli VALUES (0);

--istruttori

--altri

--clienti X

--abbonamenti

INSERT INTO abbonamenti VALUES (0, 'sala_pesi', 30);
INSERT INTO abbonamenti VALUES (1, 'corsi', 40);
INSERT INTO abbonamenti VALUES (2, 'completo', 55);
INSERT INTO abbonamenti VALUES (3, 'prova', 10);

--abbonati X
--nonabbonati X


--stanze
INSERT INTO stanze VALUES (0, 'Stanza A', 20);
INSERT INTO stanze(nome, dimensione) VALUES ('Stanza B', 40);
INSERT INTO stanze(nome, dimensione) VALUES ('Stanza C', 60);
INSERT INTO stanze(nome, dimensione) VALUES ('Stanza D', 60);


--salepesi
/*INSERT INTO salepesi VALUES (0, 70, 70/2);
INSERT INTO salepesi(dimensione, iscrittimax) VALUES (80, 80/2);*/


--corsi
/*
INSERT INTO corsi VALUES (0, 'pilates', 10, 2, 0);
INSERT INTO corsi(nome, iscrittimax, istruttore, stanza) VALUES ('yoga', 20, 1, 1);
INSERT INTO corsi(nome, iscrittimax, istruttore, stanza) VALUES ('crossfit', 30, 2, 2);
INSERT INTO corsi(nome, iscrittimax, istruttore, stanza) VALUES ('power-lifting', 30, 1, 3);
*/

--sedute (SUBITO O DOPO)


--abbonatisedute (CALENDARIO)


--giorni (SUBITO)
CREATE PROCEDURE LoopGiorniSlot() AS $$
	DECLARE giorno DATE = CURRENT_DATE + 1;
	DECLARE pms INT;
	DECLARE oraIn TIME = '05:30:00';
	DECLARE oraFin TIME = '08:50:00';
	BEGIN
		SELECT personemaxslot INTO pms FROM informazioni;
		INSERT INTO giorni VALUES(CURRENT_DATE);
		INSERT INTO slot VALUES(0, pms, CURRENT_DATE, oraIn, oraFin);
		FOR i IN 0..29 LOOP
			INSERT INTO giorni VALUES(giorno);
			FOR j IN 0..5 LOOP
				INSERT INTO slot(personemax, giorno, orainizio, orafine) VALUES(pms, giorno, oraIn, oraFin);
				oraIn = oraFin + '00:10:00';
				oraFin = oraIn + '02:50:00';
			END LOOP;
			oraIn = '05:30:00';
			oraFin = '08:50:00';
			giorno = giorno + 1;
		END LOOP;
	END;
$$ LANGUAGE 'plpgsql';

CALL LoopGiorniSlot();


--slot (SUBITO)


--corsislot (SUBITO)


--salepesislot (SUBITO)


--prenotazioni (CALENDARIO)



/*
delete from corsi;
delete from salepesi;
delete from stanze;
delete from abbonamenti;
delete from altri;
delete from istruttori;
delete from clienti;
delete from utenti;
select * from prenotazioni p join slot s ON p.slot=s.id
*/