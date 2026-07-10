from __future__ import annotations

import locale
import os
from typing import Dict

SUPPORTED_LANGUAGES = ("auto", "en", "zh", "ja")

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "dashboard_title": "InferDoctor - Local AI Stack Health Check",
        "dashboard_health": "Overall Health: {score} / 100  ({label})",
        "dashboard_scores": "PASS 100 | WARN 60 | FAIL 0 | SKIP 85  (heuristic)",
        "dashboard_header": "Component   Status   Summary",
        "dashboard_divider": "----------- -------- --------------------------------------------------",
        "dashboard_top_fixes": "Top recommended fixes (most useful first):",
        "dashboard_no_fixes": "No immediate fixes recommended. Your detected stack looks healthy.",
        "dashboard_fix": "{index}. {component}: {issue}",
        "dashboard_likely_cause": "   Likely cause: {cause}",
        "dashboard_impact": "   Impact: {impact}",
        "dashboard_try": "   Try: {command}",
        "dashboard_config": "   {hint_label}: {config_hint}",
        "dashboard_detail": "Detailed diagnostics:",
        "dashboard_stack_summary": "Stack Summary: {pass_count} working | {warn_count} needs attention | {skip_count} optional/offline | {fail_count} failed",
        "dashboard_doctor_read_fail": "Doctor's read: At least one required check failed. Start with the first fix below.",
        "dashboard_doctor_read_warn": "Doctor's read: Some components need attention. Start with the first fix below.",
        "dashboard_doctor_read_skip": "Doctor's read: No hard failures detected. Skipped components are optional unless you use them.",
        "dashboard_doctor_read_pass": "Doctor's read: All detected checks passed. Your local AI stack looks ready.",
        "console_status": "[{status:<4}] {name:<10} {summary}",
        "console_detail": "       - {detail}",
        "console_suggestion": "       suggestion: {suggestion}",
        "console_raw_data": "       raw_data:",
    },
    "zh": {
        "dashboard_title": "InferDoctor - 本地 AI 堆栈健康检查",
        "dashboard_health": "总体健康：{score} / 100  ({label})",
        "dashboard_scores": "PASS 100 | WARN 60 | FAIL 0 | SKIP 85  (启发式)",
        "dashboard_header": "组件         状态     摘要",
        "dashboard_divider": "----------- -------- --------------------------------------------------",
        "dashboard_top_fixes": "推荐修复（按最有用排序）：",
        "dashboard_no_fixes": "没有发现紧急修复建议。检测到的堆栈看起来很健康。",
        "dashboard_fix": "{index}. {component}: {issue}",
        "dashboard_likely_cause": "   可能原因：{cause}",
        "dashboard_impact": "   影响：{impact}",
        "dashboard_try": "   尝试：{command}",
        "dashboard_config": "   {hint_label}：{config_hint}",
        "dashboard_detail": "详细诊断：",
        "dashboard_stack_summary": "堆栈摘要：{pass_count} 个正常 | {warn_count} 个需注意 | {skip_count} 个可选/离线 | {fail_count} 个失败",
        "dashboard_doctor_read_fail": "医生诊断：至少一个必需检查失败。请从下一个修复开始。",
        "dashboard_doctor_read_warn": "医生诊断：某些组件需要注意。请从下一个修复开始。",
        "dashboard_doctor_read_skip": "医生诊断：未检测到严重失败。跳过的组件是可选的，除非您使用它们。",
        "dashboard_doctor_read_pass": "医生诊断：所有检测通过。您的本地 AI 堆栈看起来已准备就绪。",
        "console_status": "[{status:<4}] {name:<10} {summary}",
        "console_detail": "       - {detail}",
        "console_suggestion": "       建议：{suggestion}",
        "console_raw_data": "       原始数据：",
    },
    "ja": {
        "dashboard_title": "InferDoctor - ローカルAIスタックヘルスチェック",
        "dashboard_health": "全体の健康度：{score} / 100  ({label})",
        "dashboard_scores": "PASS 100 | WARN 60 | FAIL 0 | SKIP 85  (ヒューリスティック)",
        "dashboard_header": "コンポーネント   ステータス   サマリー",
        "dashboard_divider": "----------- -------- --------------------------------------------------",
        "dashboard_top_fixes": "推奨修正（有用な順）:",
        "dashboard_no_fixes": "すぐに必要な修正はありません。検出されたスタックは健康に見えます。",
        "dashboard_fix": "{index}. {component}: {issue}",
        "dashboard_likely_cause": "   考えられる原因: {cause}",
        "dashboard_impact": "   影響: {impact}",
        "dashboard_try": "   試す: {command}",
        "dashboard_config": "   {hint_label}: {config_hint}",
        "dashboard_detail": "詳細診断:",
        "dashboard_stack_summary": "スタック概要: {pass_count} 成功 | {warn_count} 注意 | {skip_count} オプション/オフライン | {fail_count} 失敗",
        "dashboard_doctor_read_fail": "ドクターの診断: 必要なチェックが少なくとも1つ失敗しました。最初の修正から始めてください。",
        "dashboard_doctor_read_warn": "ドクターの診断: いくつかのコンポーネントに注意が必要です。最初の修正から始めてください。",
        "dashboard_doctor_read_skip": "ドクターの診断: 重大な失敗は検出されませんでした。スキップされたコンポーネントは使用する場合を除きオプションです。",
        "dashboard_doctor_read_pass": "ドクターの診断: すべての検出されたチェックが合格しました。ローカルAIスタックは準備が整っているようです。",
        "console_status": "[{status:<4}] {name:<10} {summary}",
        "console_detail": "       - {detail}",
        "console_suggestion": "       suggestion: {suggestion}",
        "console_raw_data": "       raw_data:",
    },
}


def detect_system_language() -> str:
    candidates = []
    locale_values = locale.getlocale()
    if locale_values[0]:
        candidates.append(locale_values[0])
    env_locale = os.environ.get("LANG") or os.environ.get("LANGUAGE")
    if env_locale:
        candidates.append(env_locale)

    for candidate in candidates:
        normalized = candidate.split(".")[0].replace("-", "_").lower()
        if normalized.startswith("zh"):
            return "zh"
        if normalized.startswith("ja"):
            return "ja"
        if normalized.startswith("en"):
            return "en"

    return "en"


def normalize_language(language: str) -> str:
    normalized = (language or "").strip().lower()
    if normalized in SUPPORTED_LANGUAGES:
        return normalized
    if normalized.startswith("zh"):
        return "zh"
    if normalized.startswith("ja"):
        return "ja"
    if normalized.startswith("en"):
        return "en"
    raise ValueError("Unsupported language: {0}".format(language))


def t(key: str, language: str = "auto", **kwargs: object) -> str:
    if language == "auto":
        language = detect_system_language()
    try:
        normalized_language = normalize_language(language)
    except ValueError:
        normalized_language = "en"
    translation = TRANSLATIONS.get(normalized_language, TRANSLATIONS["en"])
    template = translation.get(key, TRANSLATIONS["en"].get(key, key))
    return template.format(**kwargs)
