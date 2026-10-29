import csv
from pathlib import Path


INPUT_DIR = Path(__file__).resolve().parent
csv_files = sorted(INPUT_DIR.glob("*GradesExport*.csv"))
if not csv_files:
    raise SystemExit("No CSV files found matching *GradesExport*.csv")

HEADER_NORMALIZATION = {
    "Proctored Initial Knowledge Check Points Grade <Numeric MaxPoints:5 Category:Orienation Assignments>":
        "Proctored Initial Knowledge Check Points Grade <Numeric MaxPoints:5 Category:Orientation>",
    "IKC Topics Points Grade <Numeric MaxPoints:700 Category:ALEKS Assessment Topic Counts>":
        "IKC Topics Points Grade <Numeric MaxPoints:700 Category:ALEKS Topic Goals Weekly Counts (Hidden)>",
}


def normalize_headers(headers):
    return [HEADER_NORMALIZATION.get(header, header) for header in headers]


all_headers = []
seen_headers = set()
rows = []
excluded_placeholder_rows = 0

for csv_file in csv_files:
    with csv_file.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        header = normalize_headers(next(reader))
        for column in header:
            if column not in seen_headers:
                seen_headers.add(column)
                all_headers.append(column)
        for row in reader:
            record = dict(zip(header, row))
            org_defined_id = record.get("OrgDefinedId", "").strip().lstrip("#")
            if org_defined_id == "Student1.Math100":
                excluded_placeholder_rows += 1
                continue
            if not org_defined_id.isdecimal():
                raise ValueError(
                    f"Unexpected nonnumeric OrgDefinedId {org_defined_id!r} "
                    f"in {csv_file.name}"
                )
            rows.append(record)

output_path = INPUT_DIR / "2261_merged.csv"
with output_path.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=all_headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"Merged {len(rows)} rows from {len(csv_files)} files into {output_path.name}")
print(f"Excluded {excluded_placeholder_rows} known non-student placeholder rows")
print(f"Columns in merged file: {len(all_headers)}")
for index, column_name in enumerate(all_headers, start=1):
    print(f"{index}: {column_name}")
