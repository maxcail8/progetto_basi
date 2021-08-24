/*
Dato un corso (id) e il giorno della settimana in cui si deve svolgere, aggiungere alla tabella corslislot tutti i valori
necessari indicati dal parametro slot
*/
DROP PROCEDURE IF EXISTS aggiungi_corsi_slot(idcorso INT, giorno INT, slot TIME);
CREATE PROCEDURE aggiungi_corsi_slot(idcorso INT, giorno INT, slot TIME) AS $$
    DECLARE giorno_finale DATE = CURRENT_DATE + 30;
    DECLARE giorno_buffer DATE = CURRENT_DATE + 1;
    DECLARE giorno_settimana INT;
    DECLARE slot_c INT;
    DECLARE seduta_c INT;
    DECLARE cs_iscrittimax INT;
    BEGIN
        SELECT COALESCE(MAX(id),0) INTO seduta_c FROM sedutecorsi;
        SELECT iscrittimax INTO cs_iscrittimax FROM corsi where id=idcorso;
        WHILE giorno_buffer < giorno_finale LOOP
            SELECT EXTRACT(DOW FROM giorno_buffer) INTO giorno_settimana;
            IF (giorno_settimana = giorno) THEN
                SELECT s.id INTO slot_c FROM slot s WHERE s.giorno = giorno_buffer AND s.orainizio = slot;
                INSERT INTO corsislot VALUES (idcorso, slot_c, cs_iscrittimax);
                seduta_c = seduta_c + 1;
                INSERT INTO sedutecorsi(id, corso, dataseduta) VALUES(seduta_c, idcorso, giorno_buffer+slot);
                giorno_buffer = giorno_buffer + 7;
            ELSE 
                giorno_buffer = giorno_buffer + 1;
            END IF;
        END LOOP;
    END;
$$ LANGUAGE 'plpgsql';







DROP PROCEDURE IF EXISTS aggiungi_salapesi_slot(idsala INT);
CREATE PROCEDURE aggiungi_salapesi_slot(idsala INT) AS $$
    DECLARE giorno_finale DATE = CURRENT_DATE + 30;
    DECLARE giorno_buffer DATE = CURRENT_DATE + 1;
    DECLARE slot_sp INT;
    DECLARE seduta_sp INT;
    DECLARE sp_iscrittimax INT;
    DECLARE slot_s TIME = '05:30:00';
    DECLARE s slot%rowtype;
    BEGIN
        SELECT COALESCE(MAX(id),0) INTO seduta_sp FROM sedutesalepesi;
        SELECT iscrittimax INTO sp_iscrittimax FROM salepesi where id=idsala;
        WHILE giorno_buffer < giorno_finale LOOP
            FOR s IN SELECT * FROM slot WHERE giorno = giorno_buffer LOOP
                INSERT INTO salapesislot VALUES (idsala, s.id, sp_iscrittimax);
                seduta_sp = seduta_sp + 1;
                INSERT INTO sedutesalepesi(id, salapesi, dataseduta) VALUES(seduta_sp, idsala, giorno_buffer+s.orainizio);
            END LOOP;
            giorno_buffer = giorno_buffer + 1;
        END LOOP;
    END;
$$ LANGUAGE 'plpgsql';








DROP TRIGGER IF EXISTS t_personemq ON informazioni CASCADE;
DROP FUNCTION IF EXISTS trigger_personemq();
CREATE FUNCTION trigger_personemq() RETURNS trigger AS $$
    BEGIN
        UPDATE corsi c SET iscrittimax = (SELECT s.dimensione
                                            FROM stanze s
                                            WHERE c.stanza=s.id) / NEW.personemq;
        UPDATE salepesi sp SET iscrittimax = (sp.dimensione) / NEW.personemq;
        UPDATE slot s SET personemax = 1 + (SELECT COALESCE(SUM(c.iscrittimax),0) 
                                        FROM corsi c JOIN corsislot cs ON c.id=cs.corso
                                        WHERE s.id=cs.slot)
                                        +
                                        (SELECT COALESCE(SUM(sp.iscrittimax),0) 
                                        FROM salepesi sp JOIN salapesislot ss ON sp.id=ss.salapesi
                                        WHERE s.id=ss.slot); 
        UPDATE salapesislot ps SET iscrittimax = (SELECT sp.iscrittimax FROM salepesi sp WHERE sp.id=ps.salapesi);
        UPDATE corsislot cs SET iscrittimax = (SELECT c.iscrittimax FROM corsi c WHERE c.id=cs.corso);
        UPDATE informazioni SET personemaxslot = (SELECT COALESCE(MAX(personemax),0) FROM slot WHERE giorno > CURRENT_DATE);
        RETURN NULL;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_personemq AFTER UPDATE OF personemq ON informazioni
FOR EACH ROW
EXECUTE FUNCTION trigger_personemq();








DROP TRIGGER IF EXISTS t_iscrittimax_corso_stanza ON corsi CASCADE;
DROP FUNCTION IF EXISTS trigger_iscrittimax_corso_stanza();
CREATE FUNCTION trigger_iscrittimax_corso_stanza() RETURNS trigger AS $$
    DECLARE pmq INT;
    BEGIN
        SELECT personemq INTO pmq FROM informazioni;
        UPDATE corsi c SET iscrittimax = (SELECT s.dimensione
                                            FROM stanze s
                                            WHERE c.stanza=s.id) / pmq;
        RETURN NULL;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_iscrittimax_corso_stanza AFTER INSERT ON corsi
FOR EACH ROW
EXECUTE FUNCTION trigger_iscrittimax_corso_stanza();









DROP TRIGGER IF EXISTS t_personemaxslot ON informazioni CASCADE;
DROP FUNCTION IF EXISTS trigger_personemaxslot();
CREATE FUNCTION trigger_personemaxslot() RETURNS trigger AS $$
    DECLARE totale INT;
    DECLARE totale_corsi INT;
    DECLARE totale_sale INT;
    DECLARE s slot%rowtype;
    DECLARE i INT = 0;
    DECLARE guardia_corsi BOOLEAN = TRUE;
    DECLARE guardia_salepesi BOOLEAN = TRUE;
    BEGIN
        IF (NEW.personemaxslot <= (SELECT personemaxslot FROM informazioni)) THEN
            FOR s IN SELECT * FROM slot WHERE giorno > CURRENT_DATE ORDER BY giorno LOOP
                SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                totale = totale_corsi + totale_sale;
                WHILE totale > NEW.personemaxslot LOOP
                    UPDATE corsislot SET iscrittimax = iscrittimax - 1 WHERE slot=s.id;
                    UPDATE salapesislot SET iscrittimax = iscrittimax - 1 WHERE slot=s.id;
                    SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                    SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                    totale = totale_corsi + totale_sale;
                END LOOP;
                UPDATE slot SET personemax = 1 + (SELECT COALESCE(SUM(iscrittimax),0) 
                                            FROM corsislot WHERE slot=s.id) 
                                            + 
                                            (SELECT COALESCE(SUM(iscrittimax),0)
                                            FROM salapesislot WHERE slot=s.id) 
                            WHERE id=s.id;
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
                        IF (i%2=1 AND guardia_salepesi=TRUE) THEN
                            UPDATE salapesislot SET iscrittimax = iscrittimax + 1 WHERE slot=s.id;
                            SELECT COALESCE(SUM(iscrittimax),0) INTO totale_corsi FROM corsislot WHERE slot=s.id;
                            SELECT COALESCE(SUM(iscrittimax),0) INTO totale_sale FROM salapesislot WHERE slot=s.id;
                            totale = totale_corsi + totale_sale;
                            IF(totale >= NEW.personemaxslot) THEN
                                UPDATE salapesislot SET iscrittimax = iscrittimax - 1 WHERE slot=s.id;
                                guardia_salepesi = FALSE;
                            END IF;
                        ELSE 
                            totale = NEW.personemaxslot;
                            guardia_corsi = FALSE;
                            guardia_salepesi = FALSE;
                        END IF;                        
                    END IF;
                    i = i + 1;
                END LOOP;
                UPDATE slot SET personemax =(SELECT COALESCE(SUM(iscrittimax),0) 
                                            FROM corsislot WHERE slot=s.id) 
                                            + 
                                            (SELECT COALESCE(SUM(iscrittimax),0)
                                            FROM salapesislot WHERE slot=s.id) 
                            WHERE id=s.id;
            END LOOP;  
        END IF;

        RETURN NEW;      
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER t_personemaxslot BEFORE UPDATE OF personemaxslot ON informazioni
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
    DECLARE sp salepesi%rowtype;
    DECLARE s slot%rowtype;
    DECLARE data_tmp TIMESTAMP;
    DECLARE data_buff TIMESTAMP;
    DECLARE cs_iscrittimax INT;
    DECLARE sps_iscrittimax INT;
    DECLARE personemaxslot_buffer INT;
    BEGIN
        --check_cancella_giorni
        DELETE FROM giorni WHERE data < CURRENT_DATE - 7;
        --check_data_fine_abbonamento
        INSERT INTO nonabbonati (id) SELECT id FROM abbonati WHERE datafineabbonamento < CURRENT_DATE;
        INSERT INTO prenotazioninonabbonati (nonabbonato, slot) SELECT p.abbonato, p.slot 
                                                                FROM prenotazioni p JOIN slot s ON p.slot=s.id
                                                                WHERE p.abbonato IN (SELECT * FROM nonabbonati) AND s.giorno > CURRENT_DATE - 7;
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
        SELECT COALESCE(MAX(id),0) INTO idSedute FROM sedutecorsi;
        idSedute = idSedute + 1;
        FOR c IN SELECT * FROM corsi ORDER BY id LOOP
            FOR i IN 0..6 LOOP
                SELECT se.dataseduta INTO data_tmp FROM sedutecorsi se WHERE se.corso=c.id AND i=(SELECT EXTRACT(DOW FROM se.dataseduta));
                IF (data_tmp IS NOT NULL) THEN
                    FOR j IN 0..3 LOOP
                        IF (NOT EXISTS(SELECT * FROM sedutecorsi se WHERE se.corso=c.id AND se.dataseduta=(data_tmp + (INTERVAL '1 day' * 7*j)))) THEN
                            INSERT INTO sedutecorsi VALUES(idSedute, c.id, data_tmp + (INTERVAL '1 day' * 7*j)); 
                            SELECT dataseduta INTO data_buff FROM sedutecorsi WHERE id=idSedute;
                            SELECT id INTO idSlot FROM slot WHERE giorno=(data_buff::date);
                            SELECT cs.iscrittimax INTO cs_iscrittimax 
                                                    FROM corsislot cs JOIN slot s ON cs.slot=s.id 
                                                    WHERE cs.corso=c.id AND s.giorno > CURRENT_DATE - 7 AND i=(SELECT EXTRACT(DOW FROM s.giorno));
                            INSERT INTO corsislot VALUES(c.id, idSlot, cs_iscrittimax);
                            idSedute = idSedute + 1;
                        END IF;
                    END LOOP; 
                END IF;
            END LOOP;    
        END LOOP;
        --check_aggiungi_sapalesi_slot
        /*FOR sp IN SELECT * FROM salepesi LOOP
            FOR s IN SELECT * FROM slot WHERE giorno > CURRENT_DATE + 7 AND giorno < CURRENT_DATE + 30 LOOP
                IF (NOT EXISTS(SELECT * FROM salapesislot WHERE salapesi=sp.id AND slot=s.id)) THEN
                    SELECT sps.iscrittimax INTO sps_iscrittimax
                                            FROM salapesislot sps JOIN slot sl ON sps.slot=sl.id
                                            WHERE sl.giorno = s.giorno - 7 AND sl.orainizio=s.orainizio;
                    INSERT INTO salapesislot VALUES(sp.id, s.id, sps_iscrittimax);
                END IF;
            END LOOP;
        END LOOP;*/
        FOR sp IN SELECT * FROM salepesi LOOP
            FOR i IN 1..30 LOOP
                FOR s IN SELECT * FROM slot WHERE s.giorno = CURRENT_DATE + i LOOP
                    IF (NOT EXISTS(SELECT * FROM salapesislot WHERE salapesi=sp.id AND slot=s.id)) THEN
                        INSERT INTO salapesislot VALUES(sp.id, s.id, sp.iscrittimax);
                    END IF;
                END LOOP;
            END LOOP;
        END LOOP;
        --SELECT personemaxslot INTO personemaxslot_buffer FROM informazioni;
        --UPDATE informazioni SET personemaxslot = personemaxslot_buffer;

        RETURN NEW;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER check_data_fine_abbonamento BEFORE UPDATE ON controlli
FOR EACH ROW
EXECUTE FUNCTION trigger_check_data_fine_abbonamento();
