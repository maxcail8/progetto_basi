/*
Dato un corso (id) e il giorno della settimana in cui si deve svolgere, aggiungere alla tabella corslislot tutti i valori
necessari indicati dal parametro slot
*/
CREATE PROCEDURE aggiungi_corsi_slot(idcorso INT, giorno INT, slot TIME) AS $$
    DECLARE giorno_corrente DATE = CURRENT_DATE;
    DECLARE giorno_finale DATE = CURRENT_DATE + 30;
    DECLARE giorno_buffer DATE = CURRENT_DATE;
    DECLARE giorno_settimana INT;
    DECLARE slot_c INT;
    BEGIN
        WHILE giorno_buffer < giorno_finale LOOP
            SELECT EXTRACT(DOW FROM giorno_buffer) INTO giorno_settimana;
            IF (giorno_settimana = giorno) THEN
                SELECT s.id INTO slot_c FROM slot s WHERE s.giorno = giorno_buffer AND s.orainizio = slot;
                INSERT INTO corsislot VALUES (idcorso, slot_c);
                giorno_buffer = giorno_buffer + 7;
            ELSE 
                giorno_buffer = giorno_buffer + 1;
            END IF;
        END LOOP;
    END;
$$ LANGUAGE 'plpgsql';

CALL aggiungi_corsi_slot(1, 1, '05:30:00')

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

CREATE TRIGGER t_personemq() AFTER UPDATE OF personemq ON informazioni
FOR EACH ROW
EXECUTE FUNCTION trigger_personemq();

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

CREATE TRIGGER t_personemaxslot() AFTER UPDATE OF personemaxslot ON informazioni
FOR EACH ROW
EXECUTE FUNCTION trigger_personemaxslot();
