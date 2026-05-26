from app.ui.menu_i18n.menu_en import MENU_EN
from app.ui.menu_i18n.menu_id import MENU_ID
from app.ui.menu_i18n.menu_ja import MENU_JA
from app.ui.menu_i18n.menu_ko import MENU_KO
from app.ui.menu_i18n.menu_my import MENU_MY
from app.ui.menu_i18n.menu_ru import MENU_RU
from app.ui.menu_i18n.menu_th import MENU_TH
from app.ui.menu_i18n.menu_vi import MENU_VI
from app.ui.menu_i18n.menu_zh_tw import MENU_ZH_TW
from app.ui.menu_i18n.schema import MenuI18n


MENU_I18N_REGISTRY: dict[str, MenuI18n] = {
    "zh-TW": MENU_ZH_TW,
    "en": MENU_EN,
    "ja": MENU_JA,
    "th": MENU_TH,
    "vi": MENU_VI,
    "ko": MENU_KO,
    "id": MENU_ID,
    "my": MENU_MY,
    "ru": MENU_RU,
}


def get_menu_i18n(language_code: str) -> MenuI18n:
    return MENU_I18N_REGISTRY.get(language_code, MENU_ZH_TW)
