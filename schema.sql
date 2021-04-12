CREATE TABLE IF NOT EXISTS "tweets" (
	"content"	TEXT NOT NULL,
	"timestamp"	INTEGER,
	"location"	TEXT,
	"id"	INTEGER NOT NULL UNIQUE,
	"likes" INTEGER,
	"user"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "users" (
  "userName" TEXT NOT NULL UNIQUE,
  "password" TEXT,
  "cookie" TEXT,
  "salt" TEXT
);
