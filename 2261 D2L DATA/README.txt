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
   "MATH 100 SP26 ..._GradesExport_....csv". From this folder, run:

       python "merge (1).py"

   The merge script combines all files matching "*GradesExport*.csv",
   normalizes two inconsistent D2L column headings, excludes the known
   non-student "Student1.Math100" placeholder, and writes 2261_merged.csv.
   It stops if any other nonnumeric D2L ID appears.
2. Run the analysis script:

       python "analysis (3).py"

   It reads 2261_merged.csv and the existing demographics export
   "Untitled Analysis (18) (1).csv". It matches grade records' OrgDefinedId
   values to demographic records' Student ID values and writes
   2261_merged_with_untitled.csv and 2261_placement_analysis.tex. It stops
   for duplicate demographic IDs or any unmatched grade row. This step
   requires Python and pandas.
3. The analysis assigns placement from Final Exam Topics:
   - 550 or more: Math 108/112
   - 400-549: Math 106/107
   - below 400: Math 100
   It also reports detailed score buckets and placement summaries by
   Arizona high school status, first-generation status, the combination of
   those two categories, gender, and race/ethnicity flags. Race/ethnicity
   groups with fewer than five students are omitted.
4. To make a printable report, run this from the same folder:

       pdflatex -interaction=nonstopmode -halt-on-error "2261_placement_analysis.tex"

   This creates 2261_placement_analysis.pdf. The Python analysis script
   generates the LaTeX source but does not compile it to PDF.

The existing files with "(1)" suffixes are prior exports or generated
artifacts; the scripts now use the current demographic export's actual name
and create clean, unsuffixed merged/report outputs. "2264_merged (1).csv"
is not used by either 2261 script. The LaTeX source can be compiled with
pdfLaTeX to create a PDF; the analysis script does not compile it.

These files contain student-level educational and demographic information;
store and share them only in approved locations.

The scripts run manually. Updating a D2L export does not automatically
refresh the merged data or report; rerun the merge and analysis steps after
source data changes.
