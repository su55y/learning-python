#!/bin/sh

MIGRATIONS_DIR=basic_sqlite_migrations/migrations
if [ ! -d "$MIGRATIONS_DIR" ]; then
    echo "Migrations dir not found at $MIGRATIONS_DIR"
    exit 1
fi

# positional args:
# 1: filepath
# 2: user_version value
check_version() {
    [ -f "$1" ] || exit 1
    v=$(sqlite3 "$1" 'PRAGMA user_version;')
    case $v in
    "$2") ;;
    *)
        echo "Unexpected user_version $v, should be $2"
        exit 1
        ;;
    esac
}

printok() { printf 'Test %d: \033[1;32mOK\033[0m\n---\n' $1; }

[ -n "$DB_FILE_1" ] || DB_FILE_1=test1.db
[ -n "$DB_FILE_2" ] || DB_FILE_2=test2.db
touch "$DB_FILE_1" "$DB_FILE_2"
cleanup() { rm -v "$DB_FILE_1" "$DB_FILE_2"; }
trap cleanup EXIT

echo "Test 1: Migrate from v1 to v2"
check_version "$DB_FILE_1" 0
sqlite3 "$DB_FILE_1" <"$MIGRATIONS_DIR/0001_create_table.sql"
check_version "$DB_FILE_1" 1
python3 -m basic_sqlite_migrations "$DB_FILE_1"
check_version "$DB_FILE_1" 2
printok 1

echo "Test 2: Migrate to v2 from scratch"
python3 -m basic_sqlite_migrations "$DB_FILE_2"
check_version "$DB_FILE_2" 2
printok 2
