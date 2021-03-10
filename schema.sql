CREATE TABLE "tweets" (
	"content"	TEXT NOT NULL,
	"timestamp"	INTEGER,
	"location"	TEXT,
	"id"	INTEGER NOT NULL UNIQUE,
	"likes" INTEGER,
	"user"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);