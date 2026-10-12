"""Persistência isolada para a contribuição de API/Core Backend."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("EV_CHARGEOPS_DB", "data/ev_chargeops.db"))


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessoes_recarga (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario TEXT NOT NULL,
                id_unidade TEXT NOT NULL,
                id_carregador TEXT NOT NULL,
                kwh_consumido REAL NOT NULL,
                tempo_conexao_minutos INTEGER NOT NULL,
                ocioso_minutos INTEGER NOT NULL,
                status_sessao TEXT NOT NULL,
                payload_hash TEXT NOT NULL UNIQUE,
                recebido_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


def salvar_sessao(payload: dict) -> tuple[dict, bool]:
    """Salva uma sessão e retorna (registro, já_existia)."""
    init_db()
    payload_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        existente = db.execute(
            "SELECT * FROM sessoes_recarga WHERE payload_hash = ?", (payload_hash,)
        ).fetchone()
        if existente:
            return dict(existente), True

        cursor = db.execute(
            """INSERT INTO sessoes_recarga
            (id_usuario, id_unidade, id_carregador, kwh_consumido,
             tempo_conexao_minutos, ocioso_minutos, status_sessao, payload_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                payload["id_usuario"],
                payload["id_unidade"],
                payload["id_carregador"],
                payload["kwh_consumido"],
                payload["tempo_conexao_minutos"],
                payload["ocioso_minutos"],
                payload["status_sessao"],
                payload_hash,
            ),
        )
        registro = db.execute(
            "SELECT * FROM sessoes_recarga WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        db.commit()
        return dict(registro), False
