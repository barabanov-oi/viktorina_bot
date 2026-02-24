from flask import Flask, request, jsonify

from app.config import get_settings
from app.dto.admin import BanUserRequest, DeactivateQuestionRequest, ResolveModerationRequest
from app.persistence.unit_of_work import UnitOfWork
from app.services.moderation import ModerationService


def create_app() -> Flask:
    app = Flask(__name__)
    settings = get_settings()
    moderation = ModerationService()

    @app.before_request
    def auth_admin():
        if request.path.startswith("/admin"):
            token = request.headers.get("X-Admin-Token", "")
            if token != settings.admin_api_token:
                return jsonify({"error": "unauthorized"}), 401

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/admin/prompt-logs")
    def prompt_logs():
        limit = int(request.args.get("limit", "50"))
        with UnitOfWork() as uow:
            logs = uow.prompt_logs.latest(limit)
            return jsonify([
                {
                    "id": x.id,
                    "status": x.status,
                    "latency_ms": x.latency_ms,
                    "created_at": x.created_at.isoformat(),
                }
                for x in logs
            ])

    @app.post("/admin/ban-user")
    def ban_user():
        payload = BanUserRequest.model_validate(request.get_json(force=True))
        ok = moderation.ban_user(payload.tg_user_id)
        return {"ok": ok}

    @app.post("/admin/question/deactivate")
    def deactivate_question():
        payload = DeactivateQuestionRequest.model_validate(request.get_json(force=True))
        ok = moderation.deactivate_question(payload.question_id)
        return {"ok": ok}

    @app.post("/admin/moderation/resolve")
    def resolve_moderation():
        payload = ResolveModerationRequest.model_validate(request.get_json(force=True))
        ok = moderation.resolve_flag(payload.flag_id, payload.resolution)
        return {"ok": ok}

    return app


app = create_app()
