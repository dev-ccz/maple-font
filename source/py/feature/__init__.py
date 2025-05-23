import json
from source.py.feature import ast
from source.py.feature.base import get_base_feature_cn_only
from source.py.feature.calt import get_calt_lookup
from source.py.feature.regular import (
    feature_file_regular,
    feature_file_regular_cn,
    cls_var,
    cls_hex_letter,
    cv_list_regular,
    cv_list_cn,
    ss_list_regular,
)
from source.py.feature.italic import (
    feature_file_italic,
    feature_file_italic_cn,
    cv_list_italic,
    ss_list_italic,
)
from source.py.feature.cv import cv96, cv97, cv98, cv99


def generate_fea_string(italic: bool, cn: bool):
    if italic:
        if cn:
            return feature_file_italic_cn
        else:
            return feature_file_italic
    else:
        if cn:
            return feature_file_regular_cn
        else:
            return feature_file_regular


def generate_fea_string_cn_only():
    return ast.create(
        [
            get_base_feature_cn_only(),
            cv96.cv96_feat_cn,
            cv97.cv97_feat_cn,
            cv98.cv98_feat_cn,
            cv99.cv99_feat_cn,
        ],
    )


def get_all_calt_text():
    result = []

    for item in ast.recursive_iterate(get_calt_lookup(cls_var, cls_hex_letter, False)):
        if isinstance(item, ast.Lookup) and item.desc:
            if item.name == "escape":
                result.append(item.desc.replace("\\ ", "\\\\ "))
            else:
                result.append(item.desc)

    return "\n".join(result)


zero_desc = "Dot style `0`"


def get_version_info(
    features: list[ast.CharacterVariant] | list[ast.StylisticSet],
) -> dict[str, dict[str, str]]:
    result = {}
    for item in features:
        if item.version not in result:
            result[item.version] = {}
        result[item.version][item.tag] = item.sample
    return result


def get_cv_desc():
    return "\n".join(
        [cv.desc_item() for cv in cv_list_regular] + [f"- [v7.0] zero: {zero_desc}"]
    )


def get_cv_version_info() -> dict[str, dict[str, str]]:
    return get_version_info(cv_list_regular)


def get_cv_italic_desc():
    return "\n".join(
        [cv.desc_item() for cv in cv_list_italic if cv.id > 30 and cv.id < 61]
    )

def get_cv_italic_version_info() -> dict[str, dict[str, str]]:
    return get_version_info([cv for cv in cv_list_italic if cv.id > 30 and cv.id < 61])


def get_cv_cn_desc():
    return "\n".join([cv.desc_item() for cv in cv_list_cn])


def get_cv_cn_version_info() -> dict[str, dict[str, str]]:
    return get_version_info(cv_list_cn)

def get_ss_desc():
    result = {}
    for ss in ss_list_regular + ss_list_italic:
        if ss.id not in result:
            desc = ss.desc_item()

            if ss.id == 5:
                desc = desc.replace("`\\\\`", "`\\\\\\\\`")

            result[ss.id] = desc

    return "\n".join(sorted(result.values()))


def get_ss_version_info() -> dict[str, dict[str, str]]:
    ss = list({s.tag: s for s in ss_list_regular + ss_list_italic}.values())
    return get_version_info(sorted(ss, key=lambda x: x.tag))


__total_feat_list = (
    cv_list_regular + cv_list_italic + cv_list_cn + ss_list_regular + ss_list_italic
)


def get_total_feat_dict() -> dict[str, str]:
    result = {}

    for item in __total_feat_list:
        if item.tag not in result:
            result[item.tag] = f"[v{item.version}] " + item.desc.replace("`", "'")

    result["zero"] = "[v7.0] " + zero_desc.replace("`", "'")

    return dict(sorted(result.items()))


def get_total_feat_ts() -> str:
    feat_dict = {}

    for item in __total_feat_list:
        if item.tag not in feat_dict:
            feat_dict[item.tag] = item.desc

    feat_dict["calt"] = "Default ligatures"
    feat_dict["zero"] = zero_desc

    feat_dict = dict(sorted(feat_dict.items()))

    js_object = "\n"
    for key, val in feat_dict.items():
        js_object += f"  /** {val} */\n  {key}: string\n"

    return f"""// Auto generated by `python task.py fea`
// @prettier-ignore
/* eslint-disable */

export interface FeatureDescription {{{js_object}}}

export const featureArray = {json.dumps(list(feat_dict.keys()), indent=2)}
"""


def get_freeze_moving_rules() -> list[str]:
    result = set()

    for feat in __total_feat_list:
        if feat.has_lookup:
            result.add(feat.tag)

    return list(result)
