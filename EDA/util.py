import json
from pathlib import Path


def agg_jsonls(folder_path):
    files = [file for file in Path(folder_path).rglob("*.jl")]
    ad_ls = []
    for file in files:
        for ad in file.open("r", encoding="utf-8"):
            ad_ls.append(json.loads(ad))
    return ad_ls
