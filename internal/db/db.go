package db

import (
	"database/sql"
	"sync"

	"bctx/internal/config"
	_ "modernc.org/sqlite"
)

var (
	once sync.Once
	conn *sql.DB
	err  error
)

// Open returns the singleton DB connection. Creates + migrates on first call.
func Open() (*sql.DB, error) {
	once.Do(func() {
		config.EnsureDirs()
		path := config.DBPath()
		conn, err = sql.Open("sqlite", path)
		if err != nil {
			return
		}
		conn.Exec("PRAGMA journal_mode=WAL")
		conn.Exec("PRAGMA busy_timeout=5000")
		err = migrate(conn)
	})
	return conn, err
}

// OpenPath opens a specific database path (for testing with :memory:).
func OpenPath(path string) (*sql.DB, error) {
	db, err := sql.Open("sqlite", path)
	if err != nil {
		return nil, err
	}
	db.Exec("PRAGMA journal_mode=WAL")
	db.Exec("PRAGMA busy_timeout=5000")
	if err := migrate(db); err != nil {
		db.Close()
		return nil, err
	}
	return db, nil
}

// migrate runs CREATE TABLE IF NOT EXISTS for context_files.
func migrate(db *sql.DB) error {
	stmts := []string{
		`CREATE TABLE IF NOT EXISTS context_files (
			name        TEXT PRIMARY KEY,
			path        TEXT NOT NULL,
			scope       TEXT DEFAULT 'global',
			enabled     BOOLEAN DEFAULT 1,
			category    TEXT DEFAULT 'rules',
			type        TEXT DEFAULT 'rules',
			description TEXT DEFAULT ''
		)`,
	}

	for _, s := range stmts {
		if _, err := db.Exec(s); err != nil {
			return err
		}
	}
	return nil
}

// ResetSingleton clears the singleton connection (for testing).
func ResetSingleton() {
	if conn != nil {
		conn.Close()
	}
	once = sync.Once{}
	conn = nil
	err = nil
}
