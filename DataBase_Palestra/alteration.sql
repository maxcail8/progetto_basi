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

--Modificare lunghezza password
ALTER TABLE utenti
ALTER COLUMN password TYPE VARCHAR(512);

ALTER TABLE utenti
ALTER COLUMN password TYPE BYTEA;

/*IF (NEW.personemaxslot <= (SELECT personemaxslot FROM informazioni)) THEN
            FOR s IN SELECT * FROM slot WHERE giorno > CURRENT_DATE ORDER BY giorno LOOP
                SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                totale = totale_corsi + totale_sale;
                WHILE totale > NEW.personemaxslot LOOP
                    FOR idcorso IN SELECT corso FROM corsislot LOOP
                        UPDATE corsislot SET iscrittimax = iscrittimax - 1 WHERE corso=idcorso AND slot=s.id AND iscrittimax > 1;
                    END LOOP;
                    FOR idsala IN SELECT salapesi FROM salapesislot LOOP
                        UPDATE salapesislot SET iscrittimax = iscrittimax - 1 WHERE salapesi=idsala AND slot=s.id AND iscrittimax > 1;
                    END LOOP;                    
                    SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                    SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                    totale = totale_corsi + totale_sale;
                END LOOP;
            END LOOP;  
        ELSE 
            FOR s IN SELECT * FROM slot WHERE giorno > CURRENT_DATE ORDER BY giorno LOOP
                SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                totale = totale_corsi + totale_sale;
                WHILE (totale < NEW.personemaxslot AND (guardia_corsi=TRUE OR guardia_salepesi=TRUE)) LOOP
                    IF (i%2=0 AND guardia_corsi=TRUE) THEN
                        UPDATE corsislot SET iscrittimax = iscrittimax + 1 WHERE slot=s.id;
                        SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                        SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                        totale = totale_corsi + totale_sale;
                        IF(totale >= NEW.personemaxslot) THEN
                            UPDATE corsislot SET iscrittimax = iscrittimax - 1 WHERE slot=s.id;
                            guardia_corsi = FALSE;
                        END IF;
                    ELSE 
                        IF (guardia_salepesi=TRUE) THEN
                            UPDATE salapesislot SET iscrittimax = iscrittimax + 1 WHERE slot=s.id;
                            SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                            SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                            totale = totale_corsi + totale_sale;
                            IF(totale >= NEW.personemaxslot) THEN
                                UPDATE salapesislot SET iscrittimax = iscrittimax - 1 WHERE slot=s.id;
                                guardia_salepesi = FALSE;
                            END IF;
                        ELSE 
                            guardia_corsi = FALSE;
                            guardia_salepesi = FALSE;
                        END IF;                        
                    END IF;
                    i = i + 1;
                END LOOP;
            END LOOP;  
        END IF;*/

/*SELECT personemaxslot INTO personemaxslot_buffer FROM informazioni;
UPDATE informazioni SET personemaxslot = personemaxslot_buffer;*/

select * from salapesislot sp join slot s on sp.slot=s.id order by s.giorno, s.orainizio;
select * from corsislot cs join slot s on cs.slot=s.id order by s.giorno, s.orainizio;

select cs.iscrittimax, s.personemax, sp.iscrittimax from corsislot cs join slot s on cs.slot=s.id join salapesislot sp on sp.slot=s.id;

delete from giorni where data > CURRENT_DATE + 7;
delete from sedutecorsi where id > 1;
delete from sedutesalepesi;