from app.ui.Menu_ID.Menu_ID import MENU_ID
from app.ui.Menu_JP.Menu_JP import MENU_JA
from app.ui.Menu_KR.Menu_KR import MENU_KO
from app.ui.Menu_MM.Menu_MM import MENU_MY
from app.ui.Menu_RU.Menu_RU import MENU_RU
from app.ui.Menu_TH.Menu_TH import MENU_TH
from app.ui.Menu_TW.Menu_TW import MENU_ZH_TW
from app.ui.Menu_US.Menu_US import MENU_EN
from app.ui.Menu_VN.Menu_VN import MENU_VI
from app.ui.menu_schema import MenuI18n


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


