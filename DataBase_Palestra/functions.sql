CREATE PROCEDURE test(ciao INT) AS $$
    BEGIN
        FOR i IN 0..5 LOOP
            INSERT INTO corsislot VALUES(ciao, i);
        END LOOP;
    END;
$$ LANGUAGE 'plpgsql';

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
        UPDATE informazioni SET personemaxslot = (SELECT MAX(personemax) FROM slot)
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
