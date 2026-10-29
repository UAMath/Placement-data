from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
SOURCE_MAIN_CSV = BASE_DIR / "2254_merged.csv"
SOURCE_DEMOGRAPHICS_CSV = BASE_DIR / "2254_full_course_with_demographics.csv"
INPUT_CSV = BASE_DIR / "2254_merged_with_untitled.csv"
OUTPUT_TEX = BASE_DIR / "placement_demographic_analysis.tex"

DEMOGRAPHIC_COLUMNS = [
    "Student ID",
    "First Generation Flag",
    "Gender Code",
    "High School State Code",
    "White Flag",
    "Hispanic or Latinx Flag",
    "Native Hawaiian or Other Pacific Islander Flag",
    "Asian Flag",
    "American Indian or Alaska Native Flag",
    "Black or African American Flag",
]

TOPICS_COL = (
    "Final Exam Topics Points Grade <Numeric MaxPoints:705 "
    "Category:ALEKS Topic Goals Weekly Counts (Hidden)>"
)
IKC_COL = (
    "IKC Topics Points Grade <Numeric MaxPoints:700 "
    "Category:ALEKS Topic Goals Weekly Counts (Hidden)>"
)

PLACEMENT_ORDER = ["Math 108/112", "Math 106/107", "Math 100"]


def build_combined_csv() -> pd.DataFrame:
    main = pd.read_csv(SOURCE_MAIN_CSV, dtype=str)
    demographics_source = pd.read_csv(SOURCE_DEMOGRAPHICS_CSV, dtype=str)
    missing_columns = [
        column for column in DEMOGRAPHIC_COLUMNS if column not in demographics_source.columns
    ]
    if missing_columns:
        raise ValueError(
            f"{SOURCE_DEMOGRAPHICS_CSV.name} is missing required columns: "
            f"{', '.join(missing_columns)}"
        )
    demographics = demographics_source[DEMOGRAPHIC_COLUMNS].copy()

    main["_join_id"] = main["OrgDefinedId"].str.strip().str.lstrip("#")
    demographics["_join_id"] = demographics["Student ID"].str.strip()

    duplicate_ids = demographics["_join_id"].duplicated().sum()
    if duplicate_ids:
        raise ValueError(f"Found {duplicate_ids} duplicate Student ID rows in demographics CSV")

    combined = main.merge(demographics, on="_join_id", how="left", validate="one_to_one")
    unmatched = combined["Student ID"].isna()
    if unmatched.any():
        unmatched_ids = combined.loc[unmatched, "OrgDefinedId"].tolist()
        raise ValueError(
            f"{len(unmatched_ids)} rows in {SOURCE_MAIN_CSV.name} did not match a "
            f"Student ID: {unmatched_ids[:10]}"
        )

    combined = combined.drop(columns=["_join_id"])
    combined.to_csv(INPUT_CSV, index=False)
    return combined


def placement_from_topics(value: float) -> str:
    """Return the placement level associated with a final exam topic score."""
    if pd.isna(value):
        return "Missing"
    if value >= 550:
        return "Math 108/112"
    if value >= 400:
        return "Math 106/107"
    return "Math 100"


def detailed_bucket_from_topics(value: float) -> str:
    if pd.isna(value):
        return "Missing"
    if value >= 675:
        return "675+"
    if value >= 650:
        return "650-674"
    if value >= 625:
        return "625-649"
    if value >= 600:
        return "600-624"
    if value >= 550:
        return "550-599"
    if value >= 500:
        return "500-549"
    if value >= 400:
        return "400-499"
    if value >= 350:
        return "350-399"
    if value >= 200:
        return "200-349"
    if value >= 1:
        return "1-199"
    return "0"


def pct(numerator: float, denominator: float) -> float:
    if denominator == 0 or pd.isna(denominator):
        return 0.0
    return 100.0 * numerator / denominator


def format_percent(value: float) -> str:
    return f"{value:.1f}%"


def build_summary_table(df: pd.DataFrame, denominator: int) -> pd.DataFrame:
    rows = []
    for placement in PLACEMENT_ORDER:
        count = int((df["Placement"] == placement).sum())
        rows.append(
            {
                "Placement": placement,
                "Students": count,
                "Percent": format_percent(pct(count, denominator)),
            }
        )
    return pd.DataFrame(rows)


def build_detailed_bucket_table(df: pd.DataFrame, denominator: int) -> pd.DataFrame:
    bucket_order = [
        "675+",
        "650-674",
        "625-649",
        "600-624",
        "550-599",
        "500-549",
        "400-499",
        "350-399",
        "200-349",
        "1-199",
        "0",
        "Missing",
    ]
    placement_by_bucket = {
        "675+": "Math 108/112",
        "650-674": "Math 108/112",
        "625-649": "Math 108/112",
        "600-624": "Math 108/112",
        "550-599": "Math 108/112",
        "500-549": "Math 106/107",
        "400-499": "Math 106/107",
        "350-399": "Math 100",
        "200-349": "Math 100",
        "1-199": "Math 100",
        "0": "Math 100",
        "Missing": "Missing",
    }
    rows = []
    for bucket in bucket_order:
        count = int((df["Detailed Bucket"] == bucket).sum())
        rows.append(
            {
                "Topics": bucket,
                "Placement": placement_by_bucket[bucket],
                "Students": count,
                "Percent": format_percent(pct(count, denominator)),
            }
        )
    return pd.DataFrame(rows)


def race_ethnicity_group(row: pd.Series) -> str:
    race_flags = [
        ("Hispanic or Latinx", "Hispanic or Latinx Flag"),
        ("American Indian/Alaska Native", "American Indian or Alaska Native Flag"),
        ("Asian", "Asian Flag"),
        ("Black/African American", "Black or African American Flag"),
        (
            "Hawaiian/Pacific Islander",
            "Native Hawaiian or Other Pacific Islander Flag",
        ),
        ("White", "White Flag"),
    ]
    selected = [label for label, column in race_flags if str(row.get(column, "")).upper() == "Y"]
    if len(selected) > 1:
        return "Multiple flags"
    if selected:
        return selected[0]
    return "Not reported"


def build_group_table(df: pd.DataFrame, label_col: str, minimum_n: int = 1) -> pd.DataFrame:
    rows = []
    for label in sorted(df[label_col].fillna("Missing").unique()):
        group = df[df[label_col].fillna("Missing") == label]
        if len(group) < minimum_n:
            continue
        scored = group[group[TOPICS_COL].notna()]
        scored_n = len(scored)
        row = {
            "Group": label,
            "N": len(group),
            "Scored": scored_n,
            "Avg Topics": f"{scored[TOPICS_COL].mean():.1f}" if scored_n else "N/A",
            "Avg IKC": f"{scored[IKC_COL].mean():.1f}" if scored_n else "N/A",
        }
        rate_columns = {
            "Math 108/112": "108/112",
            "Math 106/107": "106/107",
            "Math 100": "100",
        }
        for placement, output_column in rate_columns.items():
            row[output_column] = format_percent(
                pct((scored["Placement"] == placement).sum(), scored_n)
            )
        rows.append(row)
    return pd.DataFrame(rows)


def tex_escape(value: object) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def latex_table(df: pd.DataFrame, align: str, caption: str) -> str:
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\small",
        rf"\caption{{{tex_escape(caption)}}}",
        rf"\begin{{tabular}}{{{align}}}",
        r"\hline",
        " & ".join(tex_escape(column) for column in df.columns) + r" \\",
        r"\hline",
    ]
    for row in df.astype(str).itertuples(index=False):
        lines.append(" & ".join(tex_escape(value) for value in row) + r" \\")
    lines.extend([r"\hline", r"\end{tabular}", r"\end{table}"])
    return "\n".join(lines)


def build_tex_report(
    df: pd.DataFrame,
    overall: pd.DataFrame,
    detailed: pd.DataFrame,
    az_table: pd.DataFrame,
    first_gen_table: pd.DataFrame,
    intersection: pd.DataFrame,
    gender_table: pd.DataFrame,
    race_table: pd.DataFrame,
    total_students: int,
    scored_students: int,
    missing_students: int,
    missing_demographics: int,
) -> str:
    return "\n\n".join(
        [
            r"\documentclass[11pt]{article}",
            r"\usepackage[margin=0.75in]{geometry}",
            r"\usepackage{array}",
            r"\setlength{\parindent}{0pt}",
            r"\setlength{\parskip}{6pt}",
            r"\setlength{\tabcolsep}{4.8pt}",
            r"\renewcommand{\arraystretch}{1.18}",
            r"\begin{document}",
            r"\begin{center}"
            + "\n"
            + r"{\Large\bfseries MATH 100 FA25 Placement Analysis}\\[4pt]"
            + "\n"
            + rf"{{\normalsize Source: {tex_escape(INPUT_CSV.name)} \quad Students included: {total_students:,}}}"
            + "\n"
            + r"\end{center}",
            (
                "Placement is based on Final Exam Topics from the ALEKS final exam "
                f"breakdown. {scored_students:,} students had final exam topic scores; "
                f"{missing_students:,} students had missing final exam topic scores. "
                "Scores of 701--704 are included in the 675+ top bucket because the "
                "source column allows up to 705 topics."
            ),
            r"\section*{Overall Placement}",
            latex_table(overall, "lrr", "Placement counts and percentages among scored students"),
            latex_table(detailed, "llrr", "Detailed final exam topic buckets among all students"),
            (
                f"Average Final Exam Topics among scored students: "
                f"{df[TOPICS_COL].mean():.1f}. Average IKC Topics: {df[IKC_COL].mean():.1f}."
            ),
            r"\clearpage",
            r"\section*{Demographic Placement Rates}",
            (
                f"The demographics file matched {total_students - missing_demographics:,} of "
                f"{total_students:,} students. Placement rates in this section are calculated "
                "among students in each group who had final exam topic scores."
            ),
            latex_table(az_table, "lrrrrrrr", "Placement rates by Arizona high school status"),
            latex_table(first_gen_table, "lrrrrrrr", "Placement rates by first-generation status"),
            latex_table(
                intersection,
                "lrrrrrrr",
                "Placement rates by first-generation and Arizona high school status",
            ),
            latex_table(gender_table, "lrrrrrrr", "Placement rates by gender"),
            latex_table(race_table, "lrrrrrrr", "Placement rates by race/ethnicity flags"),
            r"\end{document}",
        ]
    )


def main() -> None:
    df = build_combined_csv()
    df[TOPICS_COL] = pd.to_numeric(df[TOPICS_COL], errors="coerce")
    df[IKC_COL] = pd.to_numeric(df[IKC_COL], errors="coerce")

    df["Placement"] = df[TOPICS_COL].apply(placement_from_topics)
    df["Detailed Bucket"] = df[TOPICS_COL].apply(detailed_bucket_from_topics)
    df["Arizona HS"] = df["High School State Code"].fillna("").str.upper().eq("AZ")
    df["First Gen"] = df["First Generation Flag"].fillna("").str.upper().eq("Y")
    df["Arizona Group"] = df["Arizona HS"].map({True: "Arizona HS", False: "Non-Arizona HS"})
    df["First Gen Group"] = df["First Gen"].map({True: "First-gen", False: "Not first-gen"})
    df["First Gen / Arizona Group"] = df.apply(
        lambda row: (
            "First-gen AZ"
            if row["First Gen"] and row["Arizona HS"]
            else "First-gen non-AZ"
            if row["First Gen"]
            else "Non-first-gen AZ"
            if row["Arizona HS"]
            else "Non-first-gen non-AZ"
        ),
        axis=1,
    )
    df["Gender Group"] = df["Gender Code"].fillna("Missing")
    df["Race/Ethnicity Group"] = df.apply(race_ethnicity_group, axis=1)

    total_students = len(df)
    scored_students = int(df[TOPICS_COL].notna().sum())
    missing_students = total_students - scored_students
    missing_demographics = int(df["Student ID"].isna().sum())
    overall = build_summary_table(df, scored_students)
    detailed = build_detailed_bucket_table(df, total_students)
    az_table = build_group_table(df, "Arizona Group")
    first_gen_table = build_group_table(df, "First Gen Group")
    intersection = build_group_table(df, "First Gen / Arizona Group")
    gender_table = build_group_table(df, "Gender Group")
    race_table = build_group_table(df, "Race/Ethnicity Group", minimum_n=5)

    tex = build_tex_report(
        df,
        overall,
        detailed,
        az_table,
        first_gen_table,
        intersection,
        gender_table,
        race_table,
        total_students,
        scored_students,
        missing_students,
        missing_demographics,
    )
    OUTPUT_TEX.write_text(tex, encoding="utf-8")
    print(f"Wrote {OUTPUT_TEX}")
    print()
    print("Overall placement")
    print(overall.to_string(index=False))
    print()
    print("Arizona HS placement rates")
    print(az_table.to_string(index=False))
    print()
    print("First-gen placement rates")
    print(first_gen_table.to_string(index=False))
    print()
    print("First-gen / Arizona intersection")
    print(intersection.to_string(index=False))
    print()
    print("Gender placement rates")
    print(gender_table.to_string(index=False))
    print()
    print("Race/ethnicity placement rates")
    print(race_table.to_string(index=False))


if __name__ == "__main__":
    main()
