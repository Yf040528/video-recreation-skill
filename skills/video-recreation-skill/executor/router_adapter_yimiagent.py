"""Concrete UpstreamRouter for the yimiagent.cn server (see tools/router_mapping.yimiagent.json).

Maps provider-neutral capability requests onto the server's existing intelligent router
(POST /api/tasks with model 'auto'). Provider/model selection, failover, credentials and
billing stay on the server; nothing here names a provider or model.
"""
import json
import os
import urllib.request

from .router_adapter import assert_router_response

BASE_URL = os.environ.get("VIDEO_AGENT_BASE_URL", "https://yimiagent.cn")
SESSION = os.environ.get("VIDEO_AGENT_SESSION", "")  # session cookie of the operating account

SUCCEEDED = {"success"}
FAILED = {"fail", "archive_error", "submission_unknown"}
TASK_CAPABILITIES = {"image_generation": "image", "image_edit": "image", "video_generation": "video"}


def _call(method, path, body=None):
    req = urllib.request.Request(BASE_URL + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Cookie": f"ff_session={SESSION}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def _normalize(request_id, task):
    status = task.get("status")
    out = {"request_id": request_id, "status": "SUCCEEDED" if status in SUCCEEDED else "FAILED" if status in FAILED else "PENDING",
           "metadata": {"task_id": task.get("id"), "server_status": status}}
    if out["status"] == "SUCCEEDED":
        out["outputs"] = [{"type": o.get("type"), "uri": o.get("url"), "metadata": {k: o[k] for k in ("sourceUrl", "poster") if k in o}} for o in task.get("outputs", [])]
    if out["status"] == "FAILED":
        out["error"] = {"code": "UPSTREAM_TASK_FAILED", "message": str(task.get("error") or status), "retryable": True}
    return assert_router_response(out)


class YimiagentRouter:
    """execute(request) -> normalized response; poll(request_id, task_id) for PENDING tasks."""

    def execute(self, request: dict) -> dict:
        kind = TASK_CAPABILITIES.get(request["capability"])
        if not kind:
            return {"request_id": request["request_id"], "status": "FAILED",
                    "error": {"code": "CAPABILITY_NOT_EXPOSED", "message": f"{request['capability']} is executed inside the server workflow, not via /api/tasks", "retryable": False}}
        i, req = request.get("inputs", {}), request.get("requirements", {})
        body = {"kind": kind, "model": "auto", "prompt": i.get("prompt", ""), "refs": i.get("references", []),
                "ratio": req.get("aspect_ratio", "9:16"), "clientRequestId": request["request_id"]}
        if req.get("resolution"):
            body["resolution"] = req["resolution"]
        if kind == "video":
            body.update({"firstFrame": i.get("approved_keyframe", ""), "lastFrame": i.get("last_frame", ""),
                         "videoRefs": i.get("motion_reference_videos", []), "audioRefs": i.get("audio_references", []),
                         "duration": int(req.get("duration_sec", 5)),
                         # V2.2.1: dialogue / SFX / BGM are generated with the picture
                         "generateAudio": req.get("native_audio", True)})
        for key in ("recreationOf", "shotIndex", "shotGroup"):
            if key in request.get("metadata", {}):
                body[key] = request["metadata"][key]
        return _normalize(request["request_id"], _call("POST", "/api/tasks", body))

    def poll(self, request_id: str, task_id: str) -> dict:
        return _normalize(request_id, _call("GET", f"/api/tasks/{task_id}"))
