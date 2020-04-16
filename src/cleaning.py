from datetime import datetime
import numpy as np
import pandas as pd


def extract_days_to_resolution(review: dict):
    if "datetime" in review and "reply" in review["responses"]["final"]:
        init_dt = datetime.strptime(review["datetime"], '%Y-%m-%dT%H:%M:%SZ')
        final_ans_dt = datetime.strptime(review["responses"]["final"]["reply"][0]["datetime"], '%Y-%m-%dT%H:%M:%SZ')
        days_diff = (final_ans_dt - init_dt).days
        if days_diff < 0:
            return 0
        return days_diff
    return np.nan


def extract_days_to_first_contact(review: dict):
    if "datetime" in review and "business" in review["responses"] and len(review["responses"]["business"]) > 0:
        init_dt = datetime.strptime(review["datetime"], '%Y-%m-%dT%H:%M:%SZ')
        final_ans_dt = datetime.strptime(review["responses"]["business"][0]["datetime"], '%Y-%m-%dT%H:%M:%SZ')
        days_diff = (final_ans_dt - init_dt).days
        if days_diff < 0:
            return 0
        return days_diff
    return np.nan


def extract_seals(review: dict):
    """
    Extract seals from review dict
    :param review:
    :return:
    """
    hasSeal = lambda r: "responses" in r and "final" in r["responses"] and "seals" in r["responses"]["final"] and len(
        r["responses"]["final"]["seals"]) > 0
    seal_struct = {"service_grade": np.nan, "would_buy_again": np.nan}

    if hasSeal(review):
        for seal in review["responses"]["final"]["seals"]:
            if seal["seal"] == "Nota do atendimento":
                seal_struct["service_grade"] = int(seal["value"])
            elif seal["seal"] == "Voltaria a fazer negócio?":
                seal_struct["would_buy_again"] = False if seal["value"] == "Não" else True

    return seal_struct


def format_RA_to_df(review):
    """
    Format scrapped review dict into a pandas friendly data structure
    :param review:
    :return:
    """
    cols_for_df = ['title', 'description', 'business_name', 'uf', 'city', 'review_ID', 'datetime', 'timeCaptured']
    r_cp = {col: review[col] for col in cols_for_df if col in review}

    r_cp["days_to_resolution"] = extract_days_to_resolution(review)
    r_cp["days_to_first_contact"] = extract_days_to_first_contact(review)
    r_cp["resolution_outcome"] = review["responses"]["final"]["result"] if "responses" in review and "final" in review[
        "responses"] and "result" in review["responses"]["final"] else np.nan

    # Extract seals and add to dict
    seals = extract_seals(review)
    for seal_name, seal_value in seals.items():
        r_cp[seal_name] = seal_value

    return r_cp


def build_df_from_RA(reviews: list) -> pd.DataFrame:
    return pd.DataFrame([format_RA_to_df(r) for r in reviews])
