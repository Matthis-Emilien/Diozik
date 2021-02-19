BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Tracklist" (
	"track"	INTEGER NOT NULL,
	"music_title"	TEXT,
	"author"	INTEGER NOT NULL,
	PRIMARY KEY("track"),
	FOREIGN KEY("author") REFERENCES "Accounts"("account")
);
CREATE TABLE IF NOT EXISTS "Plans" (
	"plan"	INTEGER NOT NULL,
	"plan_title"	TEXT,
	PRIMARY KEY("plan")
);
CREATE TABLE IF NOT EXISTS "Users_Plan" (
	"account"	INTEGER NOT NULL UNIQUE,
	"plan"	INTEGER NOT NULL,
	FOREIGN KEY("account") REFERENCES "Accounts"("account"),
	FOREIGN KEY("plan") REFERENCES "Plans"("plan")
);
CREATE TABLE IF NOT EXISTS "Accounts" (
	"account"	INTEGER NOT NULL,
	"mail"	TEXT UNIQUE,
	"password"	TEXT,
	"username"	TEXT UNIQUE,
	PRIMARY KEY("account")
);
INSERT INTO "Tracklist" VALUES (1,'Trousse',1);
INSERT INTO "Tracklist" VALUES (2,'Crayon',2);
INSERT INTO "Tracklist" VALUES (3,'Règle',1);
INSERT INTO "Tracklist" VALUES (4,'Gomme',3);
INSERT INTO "Tracklist" VALUES (5,'Compas',3);
INSERT INTO "Tracklist" VALUES (6,'Calculatrice',1);
INSERT INTO "Plans" VALUES (1,'Essentiel');
INSERT INTO "Plans" VALUES (2,'Student');
INSERT INTO "Plans" VALUES (3,'Premium');
INSERT INTO "Users_Plan" VALUES (1,1);
INSERT INTO "Users_Plan" VALUES (2,2);
INSERT INTO "Users_Plan" VALUES (3,3);
INSERT INTO "Accounts" VALUES (1,'free@mail.com','password123','Pierre');
INSERT INTO "Accounts" VALUES (2,'student@mail.com','password123','Paul');
INSERT INTO "Accounts" VALUES (3,'premium@mail.com','password123','Jaques');
COMMIT;
