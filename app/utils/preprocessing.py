from __future__ import annotations

import pandas as pd
from typing import List, Dict


def load_skills_lookup(skills_taxonomy_df: pd.DataFrame) -> Dict[str, str]:
    """
    Build alias -> canonical skill lookup.
    Example:
    'powerbi' -> 'Power BI'
    'microsoft excel' -> 'Excel'
    """
    alias_to_skill = {}

    for _, row in skills_taxonomy_df.iterrows():
        canonical = str(row["skill_name"]).strip()
        aliases = str(row["aliases"]).split(",")

        alias_to_skill[canonical.lower()] = canonical

        for alias in aliases:
            alias_to_skill[alias.strip().lower()] = canonical

    return alias_to_skill


def normalize_skill_text(skill_text: str) -> List[str]:
    """
    Split comma-separated skill text into clean list.
    """
    if pd.isna(skill_text):
        return []

    return [
        s.strip()
        for s in str(skill_text).split(",")
        if str(s).strip()
    ]


def standardize_skills(skill_text: str, alias_lookup: Dict[str, str]) -> List[str]:
    """
    Convert raw skills into canonical skills using taxonomy aliases.
    """
    raw_skills = normalize_skill_text(skill_text)
    standardized = []

    for skill in raw_skills:
        canonical = alias_lookup.get(skill.lower(), skill.strip())
        standardized.append(canonical)

    return sorted(list(set(standardized)))


def standardize_skills_column(
    df: pd.DataFrame,
    source_col: str,
    target_col: str,
    alias_lookup: Dict[str, str]
) -> pd.DataFrame:
    """
    Add standardized skills column to dataframe.
    """
    df = df.copy()
    df[target_col] = df[source_col].apply(lambda x: standardize_skills(x, alias_lookup))
    return df


def ensure_string_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    df = df.copy()
    for col in columns:
        df[col] = df[col].fillna("").astype(str)
    return df