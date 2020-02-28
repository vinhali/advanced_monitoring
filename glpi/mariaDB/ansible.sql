CREATE TABLE ansible_tickets (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     num_event CHAR(30) NOT NULL,
     playbook CHAR(30) NOT NULL,
     event_date TIMESTAMP NOT NULL,
     PRIMARY KEY (id)
 );
