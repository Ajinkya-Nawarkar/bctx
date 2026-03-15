package tests

import (
	"os"
	"path/filepath"
	"testing"

	bctxctx "bctx/internal/context"
	"bctx/internal/db"
)

func TestContextFileAddAndList(t *testing.T) {
	d, err := db.OpenPath(":memory:")
	if err != nil {
		t.Fatalf("OpenPath failed: %v", err)
	}
	defer d.Close()

	if err := bctxctx.AddDB(d, "go-standards", "/home/user/docs/go-standards.md", "global", "rules", "rules", "Go coding standards"); err != nil {
		t.Fatalf("Add failed: %v", err)
	}
	if err := bctxctx.AddDB(d, "bay-conv", "/home/user/docs/DESIGN.md", "repo:bay", "docs", "rules", "Bay design doc"); err != nil {
		t.Fatalf("Add failed: %v", err)
	}

	list, err := bctxctx.ListDB(d)
	if err != nil {
		t.Fatalf("List failed: %v", err)
	}
	if len(list) != 2 {
		t.Fatalf("expected 2 context files, got %d", len(list))
	}

	if list[0].Name != "bay-conv" {
		t.Errorf("expected first entry 'bay-conv', got '%s'", list[0].Name)
	}
	if list[1].Name != "go-standards" {
		t.Errorf("expected second entry 'go-standards', got '%s'", list[1].Name)
	}
}

func TestContextFileRemove(t *testing.T) {
	d, err := db.OpenPath(":memory:")
	if err != nil {
		t.Fatalf("OpenPath failed: %v", err)
	}
	defer d.Close()

	bctxctx.AddDB(d, "test-rule", "/tmp/test.md", "global", "rules", "rules", "")
	if err := bctxctx.RemoveDB(d, "test-rule"); err != nil {
		t.Fatalf("Remove failed: %v", err)
	}

	list, _ := bctxctx.ListDB(d)
	if len(list) != 0 {
		t.Errorf("expected 0 entries after remove, got %d", len(list))
	}
}

func TestContextFileToggle(t *testing.T) {
	d, err := db.OpenPath(":memory:")
	if err != nil {
		t.Fatalf("OpenPath failed: %v", err)
	}
	defer d.Close()

	bctxctx.AddDB(d, "test-rule", "/tmp/test.md", "global", "rules", "rules", "")

	list, _ := bctxctx.ListDB(d)
	if !list[0].Enabled {
		t.Error("expected entry to be enabled initially")
	}

	if err := bctxctx.ToggleDB(d, "test-rule"); err != nil {
		t.Fatalf("Toggle failed: %v", err)
	}

	list, _ = bctxctx.ListDB(d)
	if list[0].Enabled {
		t.Error("expected entry to be disabled after toggle")
	}

	bctxctx.ToggleDB(d, "test-rule")
	list, _ = bctxctx.ListDB(d)
	if !list[0].Enabled {
		t.Error("expected entry to be enabled after second toggle")
	}
}

func TestActiveRules(t *testing.T) {
	d, err := db.OpenPath(":memory:")
	if err != nil {
		t.Fatalf("OpenPath failed: %v", err)
	}
	defer d.Close()

	bctxctx.AddDB(d, "global-rule", "/tmp/global.md", "global", "rules", "rules", "")
	bctxctx.AddDB(d, "bay-rule", "/tmp/bay.md", "repo:bay", "rules", "rules", "")
	bctxctx.AddDB(d, "other-rule", "/tmp/other.md", "repo:other-project", "rules", "rules", "")
	bctxctx.AddDB(d, "disabled-global", "/tmp/disabled.md", "global", "rules", "rules", "")
	bctxctx.ToggleDB(d, "disabled-global")

	active, err := bctxctx.ActiveRulesDB(d, "bay")
	if err != nil {
		t.Fatalf("ActiveRules failed: %v", err)
	}
	if len(active) != 2 {
		t.Fatalf("expected 2 active entries for 'bay', got %d", len(active))
	}

	names := map[string]bool{}
	for _, f := range active {
		names[f.Name] = true
	}
	if !names["global-rule"] {
		t.Error("expected global-rule in active entries")
	}
	if !names["bay-rule"] {
		t.Error("expected bay-rule in active entries")
	}
}

func TestContextFileReadContent(t *testing.T) {
	tmpDir := t.TempDir()
	mdPath := filepath.Join(tmpDir, "test.md")
	content := "# Test Rule\nThis is a test rule."
	os.WriteFile(mdPath, []byte(content), 0644)

	f := bctxctx.ContextFile{Name: "test", Path: mdPath}
	got, err := bctxctx.ReadContent(f)
	if err != nil {
		t.Fatalf("ReadContent failed: %v", err)
	}
	if got != content {
		t.Errorf("expected content '%s', got '%s'", content, got)
	}
}

func TestContextFileUpsert(t *testing.T) {
	d, err := db.OpenPath(":memory:")
	if err != nil {
		t.Fatalf("OpenPath failed: %v", err)
	}
	defer d.Close()

	bctxctx.AddDB(d, "test", "/path/v1.md", "global", "rules", "rules", "v1 desc")
	bctxctx.AddDB(d, "test", "/path/v2.md", "repo:bay", "docs", "skills", "v2 desc")

	list, _ := bctxctx.ListDB(d)
	if len(list) != 1 {
		t.Fatalf("expected 1 entry after upsert, got %d", len(list))
	}
	if list[0].Path != "/path/v2.md" {
		t.Errorf("expected updated path, got '%s'", list[0].Path)
	}
	if list[0].Type != "skills" {
		t.Errorf("expected updated type 'skills', got '%s'", list[0].Type)
	}
}

func TestDBOpenInMemory(t *testing.T) {
	d, err := db.OpenPath(":memory:")
	if err != nil {
		t.Fatalf("OpenPath(:memory:) failed: %v", err)
	}
	defer d.Close()

	var name string
	err = d.QueryRow(
		"SELECT name FROM sqlite_master WHERE type='table' AND name = ?", "context_files",
	).Scan(&name)
	if err != nil {
		t.Errorf("context_files table not found: %v", err)
	}
}
