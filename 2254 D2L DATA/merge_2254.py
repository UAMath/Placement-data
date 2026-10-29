import csv
from pathlib import Path

INPUT_DIR = Path(__file__).resolve().parent
csv_files = sorted(INPUT_DIR.glob('*_GradesExport*.csv'))
if not csv_files:
    raise SystemExit('No CSV files found matching *_GradesExport*.csv')

HEADER_NORMALIZATION = {
    'What is my current math class placement for next semseter (SI_3) Text Grade <Text>':
        'What is my current math class placement for next semester (SI_3) Text Grade <Text>',
    'ALEKS IKC Points Grade <Numeric MaxPoints:700 Category:ALEKS Topic Goals Weekly Counts (Hidden)>':
        'IKC Topics Points Grade <Numeric MaxPoints:700 Category:ALEKS Topic Goals Weekly Counts (Hidden)>',
    'ALEKS IKC Scheme Symbol':
        'IKC Topics Scheme Symbol',
}

def normalize_headers(headers):
    return [HEADER_NORMALIZATION.get(h, h) for h in headers]

all_headers = []
seen_headers = set()
rows = []
seen_student_ids = set()

for csv_file in csv_files:
    with csv_file.open(newline='', encoding='utf-8-sig') as fh:
        reader = csv.reader(fh)
        try:
            raw_header = next(reader)
        except StopIteration:
            raise ValueError(f'{csv_file.name} is empty') from None
        header = normalize_headers(raw_header)
        if 'OrgDefinedId' not in header:
            raise ValueError(f'{csv_file.name} does not contain an OrgDefinedId column')
        for h in header:
            if h not in seen_headers:
                seen_headers.add(h)
                all_headers.append(h)
        for line_number, row in enumerate(reader, start=2):
            if len(row) != len(header):
                raise ValueError(
                    f'{csv_file.name}:{line_number} has {len(row)} values; '
                    f'expected {len(header)}'
                )
            record = dict(zip(header, row))
            student_id = record['OrgDefinedId'].strip().lstrip('#')
            if not student_id.isdecimal():
                raise ValueError(
                    f'{csv_file.name}:{line_number} has invalid OrgDefinedId '
                    f'{record["OrgDefinedId"]!r}'
                )
            if student_id in seen_student_ids:
                raise ValueError(
                    f'{csv_file.name}:{line_number} duplicates student ID {student_id}'
                )
            seen_student_ids.add(student_id)
            rows.append(record)

output_path = INPUT_DIR / '2254_merged.csv'
with output_path.open('w', newline='', encoding='utf-8') as fh:
    writer = csv.DictWriter(fh, fieldnames=all_headers)
    writer.writeheader()
    writer.writerows(rows)

print(f'Merged {len(rows)} rows from {len(csv_files)} files into {output_path.name}')
print(f'Columns in merged file: {len(all_headers)}')
for index, column_name in enumerate(all_headers, start=1):
    print(f'{index}: {column_name}')
