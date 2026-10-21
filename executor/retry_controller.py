def retry_decision(qa_result: dict, attempt: int, max_attempts: int = 3) -> dict:
    failed=[k for k,v in qa_result.get("checks",{}).items() if v is not True]
    if qa_result.get("status") == "PASS" and not failed:
        return {"action":"ACCEPT","failed_checks":[]}
    if attempt >= max_attempts:
        return {"action":"STOP_FAILED","failed_checks":failed}
    return {"action":"REGENERATE_CURRENT_ASSET","failed_checks":failed,"instructions":qa_result.get("retry_instructions",[])}
