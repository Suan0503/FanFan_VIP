from __future__ import annotations

from dataclasses import dataclass
import os
import subprocess
import tempfile
from urllib.parse import quote

import requests

from app.core.config import settings
from app.ui.travel_result_i18n import get_travel_result_i18n


NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GOOGLE_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


http = requests.Session()
http.headers.update({"User-Agent": "FanFanVIP/1.0 (travel-assistant)"})


@dataclass
class TravelSnapshot:
    region_name: str
    landmarks: list["TravelPlace"]
    restaurants: list["TravelPlace"]
    exchange_rate: str | None = None


@dataclass
class TravelPlace:
    name: str
    google_maps_url: str


@dataclass
class TravelPreference:
    coffee_only: bool = False
    budget_cheap: bool = False
    summary: str = ""


def reverse_geocode(latitude: float, longitude: float) -> str:
    params = {
        "format": "jsonv2",
        "lat": latitude,
        "lon": longitude,
        "zoom": 14,
        "accept-language": "en,zh-TW,ja",
    }
    response = http.get(NOMINATIM_URL, params=params, timeout=15)
    response.raise_for_status()
    payload = response.json()
    return str(payload.get("display_name") or "Unknown area")


def _build_google_maps_url(name: str, latitude: float, longitude: float) -> str:
    query = quote(f"{name} {latitude},{longitude}")
    return f"https://www.google.com/maps/search/?api=1&query={query}"


def _overpass_nearby(latitude: float, longitude: float, query_tag: str, radius_m: int = 1200) -> list[TravelPlace]:
    query = f"""
[out:json][timeout:20];
(
  node[{query_tag}](around:{radius_m},{latitude},{longitude});
  way[{query_tag}](around:{radius_m},{latitude},{longitude});
  relation[{query_tag}](around:{radius_m},{latitude},{longitude});
);
out center 12;
""".strip()
    response = http.post(OVERPASS_URL, data=query.encode("utf-8"), timeout=25)
    response.raise_for_status()
    elements = response.json().get("elements", [])

    places: list[TravelPlace] = []
    seen_names: set[str] = set()
    for item in elements:
        tags = item.get("tags", {})
        name = tags.get("name") or tags.get("name:en")
        if not isinstance(name, str) or not name.strip():
            continue
        normalized_name = name.strip()
        if normalized_name in seen_names:
            continue
        center = item.get("center", {}) if isinstance(item.get("center"), dict) else {}
        item_lat = item.get("lat", center.get("lat", latitude))
        item_lon = item.get("lon", center.get("lon", longitude))
        try:
            place_lat = float(item_lat)
            place_lon = float(item_lon)
        except (TypeError, ValueError):
            place_lat = latitude
            place_lon = longitude
        places.append(
            TravelPlace(
                name=normalized_name,
                google_maps_url=_build_google_maps_url(normalized_name, place_lat, place_lon),
            )
        )
        seen_names.add(normalized_name)
        if len(places) >= 5:
            break
    return places


def _parse_preferences(user_query: str | None) -> TravelPreference:
    text = (user_query or "").strip().lower()
    if not text:
        return TravelPreference()

    coffee_keywords = [
        "咖啡",
        "咖啡廳",
        "cafe",
        "coffee",
        "카페",
        "カフェ",
        "кафе",
    ]
    cheap_keywords = [
        "便宜",
        "平價",
        "省錢",
        "cheap",
        "budget",
        "low cost",
        "安い",
        "деш",
    ]

    coffee_only = any(keyword in text for keyword in coffee_keywords)
    budget_cheap = any(keyword in text for keyword in cheap_keywords)

    parts: list[str] = []
    if coffee_only:
        parts.append("coffee only")
    if budget_cheap:
        parts.append("budget")

    return TravelPreference(
        coffee_only=coffee_only,
        budget_cheap=budget_cheap,
        summary=", ".join(parts),
    )


def _build_food_query(preference: TravelPreference) -> str:
    if preference.coffee_only and preference.budget_cheap:
        return 'amenity~"cafe|fast_food"'
    if preference.coffee_only:
        return 'amenity~"cafe|coffee_shop"'
    if preference.budget_cheap:
        return 'amenity~"restaurant|fast_food|food_court"'
    return 'amenity="restaurant"'


def build_travel_progress_text(language_code: str) -> str:
    i18n = get_travel_result_i18n(language_code)
    return (
        f"{i18n['progress_title']}\n"
        f"[▓░░] {i18n['progress_region']}\n"
        f"[▓▓░] {i18n['progress_places']}\n"
        f"[▓▓▓] {i18n['progress_ai']}"
    )


def _try_groq_summary(prompt: str) -> str | None:
    if not settings.groq_api_key.strip():
        return None
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
    }
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key.strip()}",
        "Content-Type": "application/json",
    }
    response = http.post(GROQ_CHAT_URL, json=payload, headers=headers, timeout=20)
    if response.status_code != 200:
        return None
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        return None
    content = choices[0].get("message", {}).get("content")
    return str(content).strip() if content else None


def _try_google_summary(prompt: str) -> str | None:
    if not settings.google_ai_studio_api_key.strip():
        return None
    params = {"key": settings.google_ai_studio_api_key.strip()}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = http.post(GOOGLE_GEMINI_URL, params=params, json=payload, timeout=20)
    if response.status_code != 200:
        return None
    data = response.json()
    candidates = data.get("candidates") or []
    if not candidates:
        return None
    parts = candidates[0].get("content", {}).get("parts", [])
    texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
    summary = "\n".join(texts).strip()
    return summary if summary else None


def _fallback_summary(snapshot: TravelSnapshot, language_code: str, preference: TravelPreference) -> str:
    i18n = get_travel_result_i18n(language_code)
    landmarks = (
        "\n\n".join(f"{place.name}\n{place.google_maps_url}" for place in snapshot.landmarks)
        if snapshot.landmarks
        else i18n["no_data"]
    )
    restaurants = (
        "\n\n".join(f"{place.name}\n{place.google_maps_url}" for place in snapshot.restaurants)
        if snapshot.restaurants
        else i18n["no_data"]
    )
    exchange_rate = snapshot.exchange_rate or i18n["no_data"]
    preference_line = ""
    if preference.summary:
        preference_line = f"\n{i18n['preference_label']}: {preference.summary}"
    return (
        f"{i18n['title']}\n"
        f"{i18n['region_label']}: {snapshot.region_name}\n"
        f"{i18n['landmarks_label']}: {landmarks}\n"
        f"{i18n['restaurants_label']}: {restaurants}\n"
        f"{i18n['exchange_label']}: {exchange_rate}"
        f"{preference_line}"
    )


def transcribe_audio_with_whisper_open_source(audio_bytes: bytes) -> str | None:
    whisper_bin = os.environ.get("WHISPER_BIN", "whisper")
    model_name = os.environ.get("WHISPER_MODEL", "small")

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "input.m4a")
        with open(audio_path, "wb") as fp:
            fp.write(audio_bytes)

        command = [
            whisper_bin,
            audio_path,
            "--model",
            model_name,
            "--task",
            "transcribe",
            "--output_format",
            "txt",
            "--output_dir",
            tmpdir,
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)
        except Exception:
            return None

        output_path = os.path.join(tmpdir, "input.txt")
        if not os.path.exists(output_path):
            return None
        with open(output_path, "r", encoding="utf-8") as fp:
            content = fp.read().strip()
        return content or None


def _detect_base_currency(language_code: str) -> str:
    mapping = {
        "zh-TW": "TWD",
        "en": "USD",
        "ja": "JPY",
        "th": "THB",
        "vi": "VND",
        "ko": "KRW",
        "id": "IDR",
        "my": "MMK",
        "ru": "RUB",
    }
    return mapping.get(language_code, "USD")


def get_exchange_rate(base: str, target: str) -> str | None:
    api_key = settings.exchange_rate_api_key.strip()
    if not api_key:
        return None
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base}/{target}"
    response = http.get(url, timeout=15)
    if response.status_code != 200:
        return None
    payload = response.json()
    rate = payload.get("conversion_rate")
    if rate is None:
        return None
    return f"{base}/{target} = {rate}"


def build_travel_reply(latitude: float, longitude: float, language_code: str, user_query: str | None = None) -> str:
    preference = _parse_preferences(user_query)
    region = reverse_geocode(latitude, longitude)
    landmarks = _overpass_nearby(latitude, longitude, 'tourism~"attraction|museum|viewpoint"')
    restaurants = _overpass_nearby(latitude, longitude, _build_food_query(preference))
    base_currency = _detect_base_currency(language_code)
    exchange_rate = get_exchange_rate(base_currency, "USD")
    snapshot = TravelSnapshot(region_name=region, landmarks=landmarks, restaurants=restaurants, exchange_rate=exchange_rate)

    prompt = (
        "You are FanFan travel assistant. Summarize nearby places in 4 short lines. "
        f"Language code: {language_code}. Region: {region}. "
        f"Landmarks: {[place.name for place in landmarks]}. Restaurants: {[place.name for place in restaurants]}. Exchange rate: {exchange_rate}. "
        f"Traveler request: {user_query or 'none'}"
    )

    ai_text = _try_groq_summary(prompt) or _try_google_summary(prompt)
    if ai_text:
        return ai_text
    return _fallback_summary(snapshot, language_code, preference)
