2254 D2L DATA - Folder Guide
============================

Purpose
-------
This folder contains D2L MATH 100 grade exports and code intended to combine
the section exports with student demographic data, summarize math placement,
and produce a report.

Intended workflow
-----------------
1. Export the relevant D2L grade data as CSV files. The merge step looks for
   files whose names match "*GradesExport*.csv".
2. Run the merge script. It combines the grade exports, keeps the union of
   their columns, and normalizes a few inconsistent column headings. Its
   intended output is 2254_merged.csv.
3. Run the demographic analysis script. It reads 2254_merged.csv and
   Untitled Analysis (16).csv, matching OrgDefinedId to Student ID. It stops
   if demographic IDs are duplicated or if any grade-export student cannot
   be matched, then writes 2254_merged_with_untitled.csv and
   placement_demographic_analysis.tex.
4. The analysis groups final-exam topic scores into placement bands:
   - 550 or more: Math 108/112
   - 400-549: Math 106/107
   - below 400: Math 100
   It also summarizes results by Arizona high school status, first-generation
   status, gender, and race/ethnicity flags. Race/ethnicity groups with fewer
   than five students are omitted from that report table.
5. To create a printable report, compile the generated .tex file with
   pdfLaTeX. The analysis script itself writes the .tex file; it does not
   compile the PDF.

Current folder state - check before running
-------------------------------------------
Several files presently have names or extensions that do not match their
contents, so the workflow above is not ready to run as-is:

- "2254_merged_with_untitled (1).csv" contains the Python merge script, not
  merged data. The script expects to be saved/run as Python code.
- "MATH 100 FA25 R 055-072_GradesExport_2026-07-21-17-52 (1).csv" contains
  the Python demographic-analysis script, not a grade export. Because its
  name matches "*GradesExport*.csv", the merge script would try to read it
  as data.
- "analysis (2).py" contains CSV grade data, not Python code.
- "Untitled Analysis (16) (1).csv" contains PDF data, not the demographics
  CSV expected by the analysis script. The expected input name is
  "Untitled Analysis (16).csv".
- Some files named like report outputs also appear to contain other file
  types. Check a file's contents before treating it as a valid report or
  input.

Before running the workflow, identify the correct source files, give each
file an extension matching its actual format, and make sure the required
inputs use the exact names expected by the scripts. Do not treat the
student-level files as de-identified; store and share them only in approved
locations.

The scripts are run manually; replacing an export does not automatically
refresh the merged data or report. Re-run the merge and analysis steps after
updating source data.
