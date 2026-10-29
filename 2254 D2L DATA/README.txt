2254 D2L DATA - Folder Guide
============================

Purpose
-------
This folder contains Fall 2025 MATH 100 grade exports and scripts to merge
the four section exports, join student demographics, and create a placement
analysis report.

Run the workflow
----------------
Run these commands from this folder:

    python "merge_2254.py"
    python "placement_demographic_analysis.py"
    pdflatex -interaction=nonstopmode -halt-on-error "placement_demographic_analysis.tex"

The Python analysis requires pandas. The merge script reads the four files
matching "*_GradesExport*.csv", combines their columns, and writes
"2254_merged.csv". It normalizes inconsistent D2L column names and stops if
an ID is invalid or duplicated across section files.

The analysis script joins "2254_merged.csv" to the demographic fields in
"2254_full_course_with_demographics.csv", matching OrgDefinedId to Student
ID. It stops if demographic IDs are duplicated, required demographic
columns are missing, or any grade row has no matching student. It writes
"2254_merged_with_untitled.csv" and
"placement_demographic_analysis.tex". The final command compiles that source
into "placement_demographic_analysis.pdf".

Placement bands are based on Final Exam Topics:

- 550 or more: Math 108/112
- 400-549: Math 106/107
- below 400: Math 100

The report also summarizes results by Arizona high school status,
first-generation status, the combination of those categories, gender, and
race/ethnicity flags. Race/ethnicity groups with fewer than five students
are omitted from the report table.

About the source files
----------------------
Some files in the folder had been saved with extensions that did not match
their contents. They have been given names matching their actual formats.
The two files named "MATH 100 FA25 recovered section ..._GradesExport.csv"
are valid section grade exports that had previously been named like LaTeX
build artifacts. Along with the T and W exports, these four section files
cover 1,796 distinct students.

"2254_full_course_with_demographics.csv" is the full-course export containing
demographic fields for those students. It is used as the demographic lookup,
not as another section export, because that would duplicate grade records.
"2254_full_course_grade_export.csv" is a separate full-course grade export
retained for reference and is not included in the section merge for the same
reason.

The old report PDF is retained as "placement_demographic_analysis_previous.pdf".

These files contain student-level educational and demographic information;
store and share them only in approved locations. Updating an export does not
automatically refresh the outputs; rerun the commands above after changing
source data.
