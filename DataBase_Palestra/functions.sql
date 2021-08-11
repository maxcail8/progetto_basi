/*
Dato un corso (id) e il giorno della settimana in cui si deve svolgere, aggiungere alla tabella corslislot tutti i valori
necessari indicati dal parametro slot
*/
DROP PROCEDURE IF EXISTS aggiungi_corsi_slot(idcorso INT, giorno INT, slot TIME);
CREATE PROCEDURE aggiungi_corsi_slot(idcorso INT, giorno INT, slot TIME) AS $$
    DECLARE giorno_corrente DATE = CURRENT_DATE;
    DECLARE giorno_finale DATE = CURRENT_DATE + 30;
    DECLARE giorno_buffer DATE = CURRENT_DATE;
    DECLARE giorno_settimana INT;
    DECLARE slot_c INT;
    DECLARE seduta_c INT;
    BEGIN
        SELECT COALESCE(MAX(id),0) INTO seduta_c FROM sedute;
        WHILE giorno_buffer < giorno_finale LOOP
            SELECT EXTRACT(DOW FROM giorno_buffer) INTO giorno_settimana;
            IF (giorno_settimana = giorno) THEN
                SELECT s.id INTO slot_c FROM slot s WHERE s.giorno = giorno_buffer AND s.orainizio = slot;
                INSERT INTO corsislot VALUES (idcorso, slot_c);
                seduta_c = seduta_c + 1;
                INSERT INTO sedute(id, corso, dataseduta) VALUES(seduta_c, idcorso, giorno_buffer+slot);
                giorno_buffer = giorno_buffer + 7;
            ELSE 
                giorno_buffer = giorno_buffer + 1;
            END IF;
        END LOOP;
    END;
$$ LANGUAGE 'plpgsql';

CALL aggiungi_corsi_slot(1, 1, '05:30:00')






DROP TRIGGER IF EXISTS t_personemq ON informazioni CASCADE;
DROP FUNCTION IF EXISTS trigger_personemq();
CREATE FUNCTION trigger_personemq() RETURNS trigger AS $$
    BEGIN
        UPDATE corsi c SET c.iscrittimax = (SELECT s.dimensione
                                            FROM stanze s
                                            WHERE c.stanza=s.id) / NEW.personemq;
        UPDATE salepesi sp SET sp.iscrittimax = (sp.dimensione) / NEW.personemq;
        UPDATE slot s SET s.personemax = (SELECT SUM(iscrittimax) 
                                        FROM corsi c NATURAL JOIN corsislot cs ON c.id=cs.corso
                                        WHERE s.id=cs.slot)
                                        +
                                        (SELECT SUM(iscrittimax) 
                                        FROM salepesi sp NATURAL JOIN salapesislot ss ON sp.id=ss.salapesi
                                        WHERE s.id=ss.slot); 
        UPDATE informazioni SET personemaxslot = (SELECT MAX(personemax) FROM slot WHERE giorno >= CURRENT_DATE() - 3)
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_personemq AFTER UPDATE OF personemq ON informazioni
FOR EACH ROW
EXECUTE FUNCTION trigger_personemq();






DROP TRIGGER IF EXISTS t_personemaxslot ON informazioni CASCADE;
DROP FUNCTION IF EXISTS trigger_personemaxslot();
CREATE FUNCTION trigger_personemaxslot() RETURNS trigger AS $$
    DECLARE totale INT;
    DECLARE totale_corsi INT;
    DECLARE totale_sale INT;
    BEGIN
        SELECT SUM(iscrittimax) INTO totale_corsi FROM corsi;
        SELECT SUM(iscrittimax) INTO totale_sale FROM salepesi;
        totale = totale_corsi + totale_sale;
        WHILE totale > NEW.personemaxslot LOOP
        END LOOP;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_personemaxslot AFTER UPDATE OF personemaxslot ON informazioni
FOR EACH ROW
EXECUTE FUNCTION trigger_personemaxslot();






DROP TRIGGER IF EXISTS t_username_diversi_utenti ON utenti CASCADE;
DROP FUNCTION IF EXISTS trigger_username_diversi_utenti();
CREATE FUNCTION trigger_username_diversi_utenti() RETURNS trigger AS $$
    BEGIN
        IF (EXISTS (SELECT * FROM utenti u WHERE u.username=NEW.username)) THEN
            RETURN NULL;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_username_diversi_utenti BEFORE INSERT OR UPDATE ON utenti
FOR EACH ROW
EXECUTE FUNCTION trigger_username_diversi_utenti();







DROP TRIGGER IF EXISTS t_username_diversi_clienti ON clienti CASCADE;
DROP FUNCTION IF EXISTS trigger_username_diversi_clienti();
CREATE FUNCTION trigger_username_diversi_clienti() RETURNS trigger AS $$
    BEGIN
        IF (NOT EXISTS (SELECT * FROM utenti u WHERE u.id=NEW.id)) THEN
            RETURN NULL;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_username_diversi_clienti BEFORE INSERT OR UPDATE ON clienti
FOR EACH ROW
EXECUTE FUNCTION trigger_username_diversi_clienti();







DROP TRIGGER IF EXISTS t_insert_nonabbonati ON nonabbonati CASCADE;
DROP TRIGGER IF EXISTS t_insert_abbonati ON abbonati CASCADE;
DROP FUNCTION IF EXISTS trigger_insert_clienti();
CREATE FUNCTION trigger_insert_clienti() RETURNS trigger AS $$
    BEGIN
        IF (NOT EXISTS (SELECT * FROM clienti c WHERE c.id=NEW.id)) THEN
            RETURN NULL;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_insert_abbonati BEFORE INSERT OR UPDATE ON abbonati
FOR EACH ROW
EXECUTE FUNCTION trigger_insert_clienti();

CREATE TRIGGER t_insert_nonabbonati BEFORE INSERT OR UPDATE ON nonabbonati
FOR EACH ROW
EXECUTE FUNCTION trigger_insert_clienti();







DROP TRIGGER IF EXISTS check_data_fine_abbonamento ON controlli CASCADE;
DROP FUNCTION IF EXISTS trigger_check_data_fine_abbonamento();
CREATE FUNCTION trigger_check_data_fine_abbonamento() RETURNS trigger AS $$
    DECLARE giorno_tmp DATE;
	DECLARE pms INT;
	DECLARE oraIn TIME = '05:30:00';
	DECLARE oraFin TIME = '08:50:00';
    DECLARE idSlot INT;
    DECLARE idSedute INT;
    DECLARE c corsi%rowtype;
    DECLARE data_tmp TIMESTAMP;
    DECLARE data_buff TIMESTAMP;
    BEGIN
        --check_data_fine_abbonamento
        INSERT INTO nonabbonati (id) SELECT id FROM abbonati WHERE datafineabbonamento < CURRENT_DATE;
        DELETE FROM abbonati WHERE datafineabbonamento < CURRENT_DATE;
        --check_genera_giorno_e_slot
        SELECT personemaxslot INTO pms FROM informazioni;
        SELECT MAX(id) INTO idSlot FROM slot;
        idSlot = idSlot + 1;
        FOR i IN 1..30 LOOP
            giorno_tmp = CURRENT_DATE + i;
            IF (NOT EXISTS(SELECT * FROM giorni WHERE data = giorno_tmp)) THEN
                INSERT INTO giorni VALUES(giorno_tmp);
                FOR j IN 0..5 LOOP
                    INSERT INTO slot VALUES(idSlot, pms, giorno_tmp, oraIn, oraFin);
                    idSlot = idSlot + 1;
                    oraIn = oraFin + '00:10:00';
                    oraFin = oraIn + '02:50:00';
                END LOOP;
                oraIn = '05:30:00';
                oraFin = '08:50:00';
            END IF;
        END LOOP;
        --check_aggiungi_corsi_slot
        SELECT COALESCE(MAX(id),0) INTO idSedute FROM sedute;
        idSedute = idSedute + 1;
        FOR c IN SELECT * FROM corsi ORDER BY id LOOP
            FOR i IN 0..6 LOOP
                SELECT s.dataseduta INTO data_tmp FROM sedute s WHERE s.corso=c.id AND i=(SELECT EXTRACT(DOW FROM s.dataseduta));
                IF (data_tmp IS NOT NULL) THEN
                    FOR j IN 0..3 LOOP
                        IF (NOT EXISTS(SELECT * FROM sedute se WHERE se.corso=c.id AND se.dataseduta=(data_tmp + (INTERVAL '1 day' * 7*j)))) THEN
                            INSERT INTO sedute VALUES(idSedute, c.id, data_tmp + (INTERVAL '1 day' * 7*j)); 
                            SELECT dataseduta INTO data_buff FROM sedute WHERE id=idSedute;
                            SELECT id INTO idSlot FROM slot WHERE giorno=(data_buff::date);
                            INSERT INTO corsislot VALUES(c.id, idSlot);
                            idSedute = idSedute + 1;
                        END IF;
                    END LOOP; 
                END IF;
            END LOOP;    
        END LOOP;

        RETURN NEW;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER check_data_fine_abbonamento BEFORE UPDATE ON controlli
FOR EACH ROW
EXECUTE FUNCTION trigger_check_data_fine_abbonamento();
