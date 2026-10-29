2261 D2L DATA - Folder Guide
============================

Purpose
-------
This folder contains Spring 2026 MATH 100 D2L grade exports, demographic
data, and Python scripts for combining the data and producing a placement
analysis report.

Intended workflow
-----------------
1. The source grade exports are the files named
   "MATH 100 SP26 ..._GradesExport_....csv". The merge script (merge (1).py)
   reads all files in this folder matching "*GradesExport*.csv".
2. Run the merge script to combine the section exports into 2261_merged.csv.
   It combines the columns from the exports and normalizes two inconsistent
   D2L column headings.
3. Run the analysis script (analysis (3).py). It expects 2261_merged.csv and
   Untitled Analysis (18).csv. It matches grade records' OrgDefinedId values
   to demographic records' Student ID values and writes
   2261_merged_with_untitled.csv and 2261_placement_analysis.tex.
4. The analysis assigns placement from Final Exam Topics:
   - 550 or more: Math 108/112
   - 400-549: Math 106/107
   - below 400: Math 100
   It also reports detailed score buckets and placement summaries by
   Arizona high school status, first-generation status, the combination of
   those two categories, gender, and race/ethnicity flags. Race/ethnicity
   groups with fewer than five students are omitted.
5. To make a printable report, compile the generated .tex file using
   pdfLaTeX. The Python analysis script generates the LaTeX source but does
   not compile it to PDF.

Current folder state - check before running
-------------------------------------------
The current files mostly have the expected contents, but several names
include "(1)" suffixes while the scripts expect the unsuffixed names:

- The grade merge script writes "2261_merged.csv"; the existing merged file
  is named "2261_merged (1).csv".
- The analysis script expects "Untitled Analysis (18).csv"; the existing
  demographics export is named "Untitled Analysis (18) (1).csv".
- The existing combined data file is named
  "2261_merged_with_untitled (1).csv"; the analysis script writes
  "2261_merged_with_untitled.csv".
- The report source and generated report files have "(1)" in their names;
  the analysis script writes "2261_placement_analysis.tex".
- "2264_merged (1).csv" is not referenced by either 2261 script; verify
  that it belongs in this folder before using it.

Use the correct source files and ensure their names match what the scripts
expect before running. Do not let old merged outputs be mistaken for fresh
results. These files contain student-level educational and demographic
information; store and share them only in approved locations.

The scripts run manually. Updating a D2L export does not automatically
refresh the merged data or report; rerun the merge and analysis steps after
source data changes.
