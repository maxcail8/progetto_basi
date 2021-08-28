SELECT * FROM abbonati WHERE id = id

DECLARE exist altri%rowtype;
SELECT * INTO exist FROM altri WHERE id=0;
IF NOT exist THEN
    INSERT INTO utenti VALUES(0, "admin", hashlib.md5(pw.encode()).hexdigest(), "admin", "admin", "admin@palestra.it", '1000-01-01');
    INSERT INTO altri VALUES(0);
END IF;

SELECT * FROM abbonati WHERE id = id

SELECT * FROM utenti WHERE email = email

SELECT * FROM utenti WHERE id>=100 ORDER BY id DESC

SELECT * FROM utenti WHERE id<100 ORDER BY id DESC

SELECT * FROM corsi ORDER BY id DESC

SELECT * FROM stanze ORDER BY id DESC

SELECT * FROM salepesi ORDER BY id DESC

SELECT * FROM utenti WHERE id = 0

SELECT * FROM abbonamenti WHERE tipo = subscription

SELECT * FROM abbonamenti WHERE id = id

SELECT * FROM corsi ORDER BY id ASC

SELECT * FROM stanze ORDER BY id ASC

SELECT * FROM salepesi ORDER BY id ASC

SELECT * FROM istruttori NATURAL JOIN utenti ORDER BY id ASC

SELECT * FROM clienti NATURAL JOIN utenti ORDER BY id ASC

SELECT * FROM informazioni

SELECT * FROM controlli

SELECT * FROM corsi WHERE id = %s

SELECT * FROM corsi ORDER BY id DESC

SELECT * FROM slot WHERE giorno = DATE data

SELECT * FROM salepesi WHERE id IN (
    SELECT salapesi FROM salapesislot WHERE slot= slot)

SELECT * FROM corsi WHERE id IN (
    SELECT corso FROM corsislot WHERE slot= %s)

SELECT id FROM sedutecorsi WHERE (dataseduta::date)=(
    SELECT giorno FROM slot WHERE id = %s)
    AND corso = %s