"""Reference UpstreamRouter for FrameFlow (yimiagent.cn) — public OpenAI-style API.

FrameFlow is the product name of yimiagent.cn; both names refer to the same platform.

This adapter maps provider-neutral capability requests onto FrameFlow's public API
(https://yimiagent.cn/v1, docs: https://yimiagent.cn/api-docs). Authentication uses an
API Key created in the FrameFlow workspace (「API 接入」). Billing, credentials and transport
stay on the platform; this file contains no keys and no provider names.

Environment:
  FRAMEFLOW_API_KEY      required, e.g. ffk_xxxxxxxx
  FRAMEFLOW_BASE_URL     optional, default https://yimiagent.cn/v1
  FRAMEFLOW_IMAGE_MODEL  model id for image capabilities (see GET /v1/models)
  FRAMEFLOW_VIDEO_MODEL  model id for video capabilities (see GET /v1/models)

The public API does not pick models automatically: choose model ids from GET /v1/models,
or set requirements.model per request.
"""
import json
import os
import urllib.request

from .router_adapter import assert_router_response

BASE_URL = os.environ.get("FRAMEFLOW_BASE_URL", "https://yimiagent.cn/v1").rstrip("/")
API_KEY = os.environ.get("FRAMEFLOW_API_KEY", "")
DEFAULT_MODEL = {"image": os.environ.get("FRAMEFLOW_IMAGE_MODEL", ""), "video": os.environ.get("FRAMEFLOW_VIDEO_MODEL", "")}

SUCCEEDED = {"succeeded"}
FAILED = {"failed", "cancelled"}
TASK_CAPABILITIES = {"image_generation": "image", "image_edit": "image", "video_generation": "video"}
ENDPOINT = {"image": "/images/generations", "video": "/videos/generations"}


def _call(method, path, body=None):
    if not API_KEY:
        raise RuntimeError("Set FRAMEFLOW_API_KEY (create one at https://yimiagent.cn/app?page=api)")
    req = urllib.request.Request(BASE_URL + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def _normalize(request_id, task):
    status = task.get("status")
    out = {"request_id": request_id, "status": "SUCCEEDED" if status in SUCCEEDED else "FAILED" if status in FAILED or "error" in task and not status else "PENDING",
           "metadata": {"task_id": task.get("id"), "server_status": status, "credits": task.get("credits")}}
    if out["status"] == "SUCCEEDED":
        out["outputs"] = [{"type": o.get("type"), "uri": o.get("url"), "metadata": {}} for o in task.get("outputs", [])]
    if out["status"] == "FAILED":
        err = task.get("error") or {}
        out["error"] = {"code": err.get("code", "TASK_FAILED"), "message": err.get("message", str(status)), "retryable": True}
    return assert_router_response(out)


class FrameFlowRouter:
    """execute(request) -> normalized response; poll(request_id, task_id) for PENDING tasks."""

    def execute(self, request: dict) -> dict:
        kind = TASK_CAPABILITIES.get(request["capability"])
        if not kind:
            return {"request_id": request["request_id"], "status": "FAILED",
                    "error": {"code": "CAPABILITY_NOT_EXPOSED", "retryable": False,
                              "message": f"{request['capability']} is not available through the public API; run the full workflow on https://yimiagent.cn"}}
        i, req = request.get("inputs", {}), request.get("requirements", {})
        model = req.get("model") or DEFAULT_MODEL[kind]
        if not model:
            return {"request_id": request["request_id"], "status": "FAILED",
                    "error": {"code": "MODEL_REQUIRED", "retryable": False,
                              "message": f"Set FRAMEFLOW_{kind.upper()}_MODEL or requirements.model (list: GET {BASE_URL}/models)"}}
        body = {"model": model, "prompt": i.get("prompt", ""), "aspect_ratio": req.get("aspect_ratio", "9:16")}
        if req.get("resolution"):
            body["resolution"] = req["resolution"]
        refs = [u for u in i.get("references", []) if str(u).startswith("https://")]
        if refs:
            body["image_urls"] = refs[:5]
        if kind == "video":
            body["duration"] = int(req.get("duration_sec", 5))
            body["generate_audio"] = bool(req.get("native_audio", True))  # dialogue / SFX / BGM generated with the picture
            if i.get("approved_keyframe"):
                body["first_frame_url"] = i["approved_keyframe"]
            if i.get("last_frame"):
                body["last_frame_url"] = i["last_frame"]
        return _normalize(request["request_id"], _call("POST", ENDPOINT[kind], body))

    def poll(self, request_id: str, task_id: str) -> dict:
        return _normalize(request_id, _call("GET", f"/tasks/{task_id}"))

    def quote(self, request: dict) -> dict:
        """Price check before submitting (not charged): POST /v1/quote."""
        kind = TASK_CAPABILITIES.get(request["capability"], "image")
        req = request.get("requirements", {})
        return _call("POST", "/quote", {"type": kind, "model": req.get("model") or DEFAULT_MODEL[kind],
                                         "resolution": req.get("resolution"), "duration": req.get("duration_sec")})


# Backwards-compatible name used by earlier versions of this repository.
YimiagentRouter = FrameFlowRouter
