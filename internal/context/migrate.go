package context

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"

	"bctx/internal/db"
	_ "modernc.org/sqlite"
)

// MigrateFromBay imports context_files from bay's database on first run.
// This is a one-time migration: if bctx already has entries, it's a no-op.
func MigrateFromBay() error {
	home, err := os.UserHomeDir()
	if err != nil {
		return nil
	}

	bayDBPath := filepath.Join(home, ".bay", "bay.db")
	if _, err := os.Stat(bayDBPath); os.IsNotExist(err) {
		return nil // bay not installed, nothing to migrate
	}

	d, err := db.Open()
	if err != nil {
		return fmt.Errorf("opening bctx db: %w", err)
	}

	// Check if we already have entries — skip if so
	var count int
	if err := d.QueryRow(`SELECT COUNT(*) FROM context_files`).Scan(&count); err != nil {
		return nil
	}
	if count > 0 {
		return nil // already migrated or user has added entries
	}

	bayDB, err := sql.Open("sqlite", bayDBPath)
	if err != nil {
		return nil // can't open bay DB, skip silently
	}
	defer bayDB.Close()

	rows, err := bayDB.Query(`SELECT name, path, scope, enabled, category, COALESCE(type, 'rules'), COALESCE(description, '') FROM context_files`)
	if err != nil {
		return nil // bay DB might not have this table
	}
	defer rows.Close()

	migrated := 0
	for rows.Next() {
		var name, path, scope, category, typ, description string
		var enabled bool
		if err := rows.Scan(&name, &path, &scope, &enabled, &category, &typ, &description); err != nil {
			continue
		}

		_, err := d.Exec(
			`INSERT OR IGNORE INTO context_files (name, path, scope, enabled, category, type, description) VALUES (?, ?, ?, ?, ?, ?, ?)`,
			name, path, scope, enabled, category, typ, description,
		)
		if err == nil {
			migrated++
		}
	}

	if migrated > 0 {
		fmt.Printf("bctx: migrated %d context files from bay\n", migrated)
	}
	return nil
}
