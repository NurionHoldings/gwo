#!/usr/bin/env python3
"""Generate locale JSON files for the GWO template."""

from __future__ import annotations

import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "assets" / "locales"
LANGS = ("ko", "si", "en", "zh", "fil", "th", "ur", "uz", "ky")

# path -> {lang: value}
T: dict[str, dict[str, str]] = {}


def s(path: str, ko: str, si: str, en: str, zh: str, fil: str, th: str, ur: str, uz: str, ky: str) -> None:
    T[path] = {
        "ko": ko, "si": si, "en": en, "zh": zh, "fil": fil,
        "th": th, "ur": ur, "uz": uz, "ky": ky,
    }


def build_nested(flat: dict[str, str]) -> dict:
    root: dict = {}
    for path, value in flat.items():
        parts = path.split(".")
        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
    return root


def count_keys(obj) -> int:
    if isinstance(obj, dict):
        return sum(count_keys(v) for v in obj.values())
    return 1


def populate_strings() -> None:
    # --- common.nav ---
    s("common.nav.mandate",
      "위탁 업무", "භාරකාර කාර්යයන්", "Delegated Tasks", "委托业务", "Mga Inilaang Gawain",
      "งานที่มอบหมาย", "سپردہ کام", "Topshiriq vazifalari", "Өткөрүлгөн тапсырмалар")
    s("common.nav.education",
      "동반교육", "එක්ව අධ්‍යාපනය", "Co-Education", "协同教育", "Ko-edukasyon",
      "การศึกษาร่วม", "مشترکہ تعلیم", "Hamkor ta'lim", "Кошумча окутуу")
    s("common.nav.support",
      "적응·권익", "අනුවර්තනය සහ අයිතිවාසිකම්", "Adaptation & Rights", "适应与权益", "Pag-aangkop at Karapatan",
      "การปรับตัวและสิทธิ", "موافقت اور حقوق", "Moslashuv va huquqlar", "Бейиш жана укуктар")
    s("common.nav.dashboard",
      "운영 대시보드", "මෙහෙයුම් උපකරණ පුවරුව", "Operations Dashboard", "运营仪表板", "Dashboard ng Operasyon",
      "แดชบอร์ดการดำเนินงาน", "آپریشن ڈیش بورڈ", "Operatsiya paneli", "Операциялык панель")
    s("common.nav.report",
      "정책 보고", "ප්‍රතිපත්ති වාර්තාව", "Policy Reporting", "政策报告", "Ulat sa Patakaran",
      "รายงานนโยบาย", "پالیسی رپورٹ", "Siyosat hisoboti", "Саясаттык отчет")
    s("common.nav.inquiry",
      "협력 문의", "සහයෝගීතා විමසීම", "Partnership Inquiry", "合作咨询", "Pagtatanong sa Pakikipagtulungan",
      "สอบถามความร่วมมือ", "شراکت کی درخواست", "Hamkorlik so'rovi", "Өнөктөшүү суроосу")
    s("common.nav.menuOpen",
      "메뉴 열기", "මෙනුව විවෘත කරන්න", "Open menu", "打开菜单", "Buksan ang menu",
      "เปิดเมนู", "مینو کھولیں", "Menyuni ochish", "Менюну ачуу")
    s("common.nav.menuClose",
      "메뉴 닫기", "මෙනුව වසන්න", "Close menu", "关闭菜单", "Isara ang menu",
      "ปิดเมนู", "مینو بند کریں", "Menyuni yopish", "Менюну жабуу")
    s("common.nav.home",
      "홈", "මුල් පිටුව", "Home", "首页", "Home",
      "หน้าแรก", "ہوم", "Bosh sahifa", "Башкы бет")

    # --- common back / learn ---
    s("common.learnMore",
      "자세히 보기 →", "වැඩි විස්තර →", "Learn more →", "了解更多 →", "Alamin pa →",
      "ดูรายละเอียด →", "مزید جانیں →", "Batafsil →", "Кененирээк →")
    s("common.backHome",
      "← 홈으로", "← මුල් පිටුවට", "← Back to home", "← 返回首页", "← Bumalik sa home",
      "← กลับหน้าแรก", "← ہوم پر واپس", "← Bosh sahifaga", "← Башкы бетке")
    s("common.backMandate",
      "← 위탁 업무로", "← භාරකාර කාර්යයන් වෙත", "← Back to delegated tasks", "← 返回委托业务", "← Bumalik sa inilaang gawain",
      "← กลับไปงานที่มอบหมาย", "← سپردہ کاموں پر", "← Topshiriq vazifalariga", "← Өткөрүлгөн тапсырмаларга")
    s("common.backCycle",
      "← 근로자 여정으로", "← සේවක ගමන වෙත", "← Back to worker journey", "← 返回劳动者旅程", "← Bumalik sa paglalakbay ng manggagawa",
      "← กลับไปเส้นทางแรงงาน", "← کارکن کے سفر پر", "← Ishchi yo'liga", "← Эмгекчи сапарына")
    s("common.backEducation",
      "← 동반교육으로", "← එක්ව අධ්‍යාපනය වෙත", "← Back to co-education", "← 返回协同教育", "← Bumalik sa ko-edukasyon",
      "← กลับไปการศึกษาร่วม", "← مشترکہ تعلیم پر", "← Hamkor ta'limga", "← Кошумча окутууга")

    # --- common.footer ---
    s("common.footer.platform",
      "Platform", "වේදිකාව", "Platform", "平台", "Platform",
      "แพลตฟอร์ม", "پلیٹ فارم", "Platforma", "Платформа")
    s("common.footer.contact",
      "Contact", "සම්බන්ධතා", "Contact", "联系方式", "Contact",
      "ติดต่อ", "رابطہ", "Aloqa", "Байланыш")
    s("common.footer.copyright",
      "© 2026 Global Workforce Operations. All rights reserved.",
      "© 2026 Global Workforce Operations. සියලු හිමිකම් ඇවිරිණි.",
      "© 2026 Global Workforce Operations. All rights reserved.",
      "© 2026 Global Workforce Operations. 保留所有权利。",
      "© 2026 Global Workforce Operations. Lahat ng karapatan ay nakalaan.",
      "© 2026 Global Workforce Operations. สงวนลิขสิทธิ์",
      "© 2026 Global Workforce Operations. جملہ حقوق محفوظ ہیں۔",
      "© 2026 Global Workforce Operations. Barcha huquqlar himoyalangan.",
      "© 2026 Global Workforce Operations. Бардык укуктар корголгон.")
    s("common.footer.tagline",
      "지자체 위임형 해외 인력 통합 운영 플랫폼",
      "ප්‍රාදේශීය සභා භාරකාර විදේශීය ශ්‍රම ඒකාබද්ධ මෙහෙයුම් වේදිකාව",
      "Municipality-delegated integrated foreign workforce operations platform",
      "地方政府委托型海外劳动力综合运营平台",
      "Pinagsamang plataporma ng operasyon ng dayuhang manggagawa na inilaan ng munisipyo",
      "แพลตฟอร์มบูรณาการการดำเนินงานแรงงานต่างชาติแบบมอบหมายจากองค์กรปกครองท้องถิ่น",
      "بلدیاتی سپردگی پر مبنی غیر ملکی افرادی قوت کا مربوط آپریشن پلیٹ فارم",
      "Mahalliy hokimiyat topshirig'idagi xorijiy ishchi kuchi integratsiyalangan operatsiya platformasi",
      "Жергиликтүү бийлик тапшырмачыл чет элдик жумушчу күчүн бириктирген операциялык платформа")
    s("common.footer.taglineDetail",
      "입국 후 동반교육 · 적응·안전 점검 · 이직·근무처 변경 지원 · 정책 보고",
      "ආගමනයෙන් පසු එක්ව අධ්‍යාපනය · අනුවර්තනය සහ ආරක්ෂක පරීක්ෂාව · සේවා ස්ථාන වෙනස් කිරීමේ සහාය · ප්‍රතිපත්ති වාර්තාව",
      "Post-arrival co-education · Adaptation & safety checks · Job/worksite change support · Policy reporting",
      "入境后协同教育 · 适应与安全检查 · 转职与工作地点变更支持 · 政策报告",
      "Ko-edukasyon pagkatapos ng pagdating · Pagsusuri sa pag-aangkop at kaligtasan · Suporta sa paglipat ng trabaho · Ulat sa patakaran",
      "การศึกษาร่วมหลังเข้าประเทศ · ตรวจสอบการปรับตัวและความปลอดภัย · สนับสนุนการเปลี่ยนงาน · รายงานนโยบาย",
      "آمد کے بعد مشترکہ تعلیم · موافقت اور حفاظت کی جانچ · نوکری/کام کی جگہ تبدیلی کی مدد · پالیسی رپورٹ",
      "Kelgandan keyin hamkor ta'lim · Moslashuv va xavfsizlik tekshiruvi · Ish/o'rin o'zgarishi yordami · Siyosat hisoboti",
      "Келгенден кийин кошумча окутуу · Бейиш жана коопсуздук текшерүү · Жумуш/орун алмаштыруу колдоосу · Саясаттык отчет")
    s("common.footer.linkMandate",
      "지자체 위탁 업무", "ප්‍රාදේශීය සභා භාරකාර කාර්යයන්", "Municipal delegated tasks", "地方政府委托业务", "Inilaang gawain ng munisipyo",
      "งานที่มอบหมายจากองค์กรปกครองท้องถิ่น", "بلدیاتی سپردہ کام", "Mahalliy hokimiyat topshirig'i", "Жергиликтүү бийлик тапшырмалары")
    s("common.footer.linkEducation",
      "동반교육", "එක්ව අධ්‍යාපනය", "Co-education", "协同教育", "Ko-edukasyon",
      "การศึกษาร่วม", "مشترکہ تعلیم", "Hamkor ta'lim", "Кошумча окутуу")
    s("common.footer.linkSupport",
      "적응·권익 지원", "අනුවර්තනය සහ අයිතිවාසිකම් සහාය", "Adaptation & rights support", "适应与权益支持", "Suporta sa pag-aangkop at karapatan",
      "สนับสนุนการปรับตัวและสิทธิ", "موافقت اور حقوق کی مدد", "Moslashuv va huquqlar yordami", "Бейиш жана укуктар колдоосу")
    s("common.footer.linkDashboard",
      "운영 대시보드", "මෙහෙයුම් උපකරණ පුවරුව", "Operations dashboard", "运营仪表板", "Dashboard ng operasyon",
      "แดชบอร์ดการดำเนินงาน", "آپریشن ڈیش بورڈ", "Operatsiya paneli", "Операциялык панель")
    s("common.footer.linkReport",
      "정책 보고", "ප්‍රතිපත්ති වාර්තාව", "Policy reporting", "政策报告", "Ulat sa patakaran",
      "รายงานนโยบาย", "پالیسی رپورٹ", "Siyosat hisoboti", "Саясаттык отчет")

    # --- common.buttons ---
    s("common.buttons.municipalityInquiry",
      "지자체 협력 문의", "ප්‍රාදේශීය සභා සහයෝගීතා විමසීම", "Municipal partnership inquiry", "地方政府合作咨询", "Pagtatanong sa pakikipagtulungan ng munisipyo",
      "สอบถามความร่วมมือกับองค์กรปกครองท้องถิ่น", "بلدیاتی شراکت کی درخواست", "Mahalliy hokimiyat hamkorligi so'rovi", "Жергиликтүү бийлик өнөктөшүү суроосу")
    s("common.buttons.viewMandate",
      "위탁 업무 보기", "භාරකාර කාර්යයන් බලන්න", "View delegated tasks", "查看委托业务", "Tingnan ang inilaang gawain",
      "ดูงานที่มอบหมาย", "سپردہ کام دیکھیں", "Topshiriq vazifalarini ko'rish", "Өткөрүлгөн тапсырмаларды көрүү")
    s("common.buttons.cooperationConsult",
      "협력 구조 상담하기", "සහයෝගීතා ව්‍යුහය සාකච්ඡා කරන්න", "Consult on partnership structure", "咨询合作结构", "Kumonsulta sa istruktura ng pakikipagtulungan",
      "ปรึกษาโครงสร้างความร่วมมือ", "شراکت کی ساخت پر مشورہ", "Hamkorlik tuzilmasi bo'yicha maslahat", "Өнөктөшүү түзүлүшү боюнча кеңеш")
    s("common.buttons.backToTop",
      "처음으로", "ආරම්භයට", "Back to top", "返回顶部", "Bumalik sa simula",
      "กลับด้านบน", "اوپر واپس", "Boshiga qaytish", "Башына кайтуу")
    s("common.buttons.viewReport",
      "보고서 구성 보기", "වාර්තා ව්‍යුහය බලන්න", "View report structure", "查看报告结构", "Tingnan ang istruktura ng ulat",
      "ดูโครงสร้างรายงาน", "رپورٹ کی ساخت دیکھیں", "Hisobot tuzilmasini ko'rish", "Отчет түзүлүшүн көрүү")
    s("common.buttons.viewLegal",
      "AI법친 연계 흐름 보기", "AI නීති සහාය සම්බන්ධතා ප්‍රවාහය බලන්න", "View AI legal support flow", "查看AI法务联动流程", "Tingnan ang daloy ng AI legal support",
      "ดูขั้นตอนเชื่อมต่อ AI ด้านกฎหมาย", "AI قانونی مدد کے ربط کا عمل دیکھیں", "AI huquqiy yordam oqimini ko'rish", "AI юридикалык колдоо агымын көрүү")

    # --- common.modal ---
    s("common.modal.close",
      "닫기", "වසන්න", "Close", "关闭", "Isara",
      "ปิด", "بند کریں", "Yopish", "Жабуу")
    s("common.modal.inquiry.title",
      "협력 문의", "සහයෝගීතා විමසීම", "Partnership inquiry", "合作咨询", "Pagtatanong sa pakikipagtulungan",
      "สอบถามความร่วมมือ", "شراکت کی درخواست", "Hamkorlik so'rovi", "Өнөктөшүү суроосу")
    s("common.modal.inquiry.desc",
      "도입 목적과 운영 환경을 남겨주시면 제안 흐름을 검토할 수 있도록 구성한 데모 양식입니다.",
      "ඔබේ හඳුන්වාදීමේ අරමුණ සහ මෙහෙයුම් පරිසරය තබන්න. මෙය යෝජනා ප්‍රවාහය සමාලෝචනය කිරීමට සැකසූ ආදර්ශ පෝරමයකි.",
      "Leave your adoption goals and operating environment. This is a demo form configured to review a proposal flow.",
      "请留下引入目的和运营环境。这是为审查提案流程而配置的演示表单。",
      "Ilagay ang layunin ng pagpapakilala at kapaligiran ng operasyon. Ito ay demo form para suriin ang daloy ng panukala.",
      "กรอกวัตถุประสงค์การนำเข้าและสภาพแวดล้อมการดำเนินงาน นี่คือแบบฟอร์มสาธิตสำหรับตรวจสอบขั้นตอนเสนอ",
      "اپنی متعارف کرنے کی غرض اور آپریشن ماحول درج کریں۔ یہ تجویز کے عمل کا جائزہ لینے کے لیے ڈیمو فارم ہے۔",
      "Joriy etish maqsadi va operatsiya muhitini qoldiring. Bu taklif oqimini ko'rib chiqish uchun demo shakl.",
      "Киргизүү максаты жана операциялык чөйрөнү калтырыңыз. Бул сунуш агымын карап чыгуу үчүн демо форма.")
    s("common.modal.municipality.title",
      "지자체 협력 문의", "ප්‍රාදේශීය සභා සහයෝගීතා විමසීම", "Municipal partnership inquiry", "地方政府合作咨询", "Pagtatanong sa pakikipagtulungan ng munisipyo",
      "สอบถามความร่วมมือกับองค์กรปกครองท้องถิ่น", "بلدیاتی شراکت کی درخواست", "Mahalliy hokimiyat hamkorligi so'rovi", "Жергиликтүү бийлик өнөктөшүү суроосу")
    s("common.modal.municipality.desc",
      "지역의 업종·인력 현황·기존 운영 체계를 기준으로 입국 후 동반교육, 적응·안전 점검, 변경 업무 지원의 위탁 모델을 구성합니다.",
      "කලාපයේ කර්මාන්ත, ශ්‍රම තත්ත්වය සහ පවතින මෙහෙයුම් පද්ධතිය මත පදනම්ව ආගමනයෙන් පසු එක්ව අධ්‍යාපනය, අනුවර්තනය සහ ආරක්ෂක පරීක්ෂාව සහ වෙනස් කිරීමේ සහාය සඳහා භාරකාර මාදිලිය සකසයි.",
      "Based on local industry, workforce status, and existing operations, we configure a delegated model for post-arrival co-education, adaptation and safety checks, and change support.",
      "根据地区产业、劳动力现状和现有运营体系，配置入境后协同教育、适应与安全检查及变更业务支持的委托模式。",
      "Batay sa industriya, kalagayan ng workforce, at umiiral na operasyon sa rehiyon, bubuuin ang delegated model para sa ko-edukasyon, pagsusuri sa pag-aangkop at kaligtasan, at suporta sa pagbabago.",
      "อิงตามอุตสาหกรรม สถานะแรงงาน และระบบปฏิบัติการเดิมในพื้นที่ กำหนดรูปแบบมอบหมายสำหรับการศึกษาร่วมหลังเข้าประเทศ การตรวจสอบการปรับตัวและความปลอดภัย และการสนับสนุนการเปลี่ยนแปลง",
      "علاقے کی صنعت، افرادی قوت کی صورتحال اور موجودہ آپریشن کے مطابق آمد کے بعد مشترکہ تعلیم، موافقت و حفاظت کی جانچ اور تبدیلی کی مدد کا سپردہ ماڈل تشکیل دیا جاتا ہے۔",
      "Hududning sanoati, ishchi kuchi holati va mavjud operatsiya tizimiga asoslanib, kelgandan keyingi hamkor ta'lim, moslashuv va xavfsizlik tekshiruvi hamda o'zgarish yordami uchun topshirma modeli tuziladi.",
      "Аймактын өнөр жайы, жумушчу күчүнүн абалы жана учурдагы операциялык тизме негизинде келгенден кийинки кошумча окутуу, бейиш жана коопсуздук текшерүү жана өзгөрүү колдоосу үчүн тапшырма моделин түзөт.")
    s("common.modal.legal.title",
      "AI법친 연계 흐름", "AI නීති සහාය සම්බන්ධතා ප්‍රවාහය", "AI legal support flow", "AI法务联动流程", "Daloy ng AI legal support",
      "ขั้นตอนเชื่อมต่อ AI ด้านกฎหมาย", "AI قانونی مدد کا ربط", "AI huquqiy yordam oqimi", "AI юридикалык колдоо агымы")
    s("common.modal.legal.desc",
      "근로자의 모국어 입력 → 상황 정리 → 자료·절차 안내 → 운영센터 확인 → 필요 시 전문가 연결의 초기 지원 흐름을 설계합니다.",
      "සේවකයාගේ මව් භාෂාවෙන් ආදානය → තත්ත්වය සංවිධානය → දත්ත සහ ක්‍රියාපටිපාටි මාර්ගෝපදේශනය → මෙහෙයුම් මධ්‍යස්ථානය සත්‍යාපනය → අවශ්‍ය නම් විශේෂඥ සම්බන්ධතාව.",
      "Worker's native-language input → situation summary → guidance on documents and procedures → operations center review → expert referral when needed.",
      "劳动者母语输入 → 情况整理 → 资料与流程指引 → 运营中心确认 → 必要时连接专家。",
      "Input sa katutubong wika ng manggagawa → pag-aayos ng sitwasyon → gabay sa dokumento at proseso → beripikasyon ng operations center → eksperto kung kinakailangan.",
      "ป้อนข้อมูลภาษาแม่ของแรงงาน → สรุปสถานการณ์ → แนะนำเอกสารและขั้นตอน → ศูนย์ปฏิบัติการตรวจสอบ → เชื่อมผู้เชี่ยวชาญเมื่อจำเป็น",
      "کارکن کی مادری زبان میں درج → صورتحال کی ترتیب → دستاویزات و طریقہ کار کی رہنمائی → آپریشنز سینٹر کی تصدیق → ضرورت پر ماہر سے رابطہ",
      "Ishchining ona tilidagi kiritma → vaziyatni tartibga solish → hujjat va tartib yo'riqnomasi → operatsiya markazi tekshiruvi → kerak bo'lsa mutaxassisga ulanish",
      "Эмгекчиндин эне тилинде киргизүү → абалды түзөтүү → документтер жана тартип боюнча көрсөтмө → операциялык борбор текшерүү → керек болсо адис менен байланыш")
    s("common.modal.report.title",
      "정책 보고 구성", "ප්‍රතිපත්ති වාර්තා ව්‍යුහය", "Policy report structure", "政策报告结构", "Istruktura ng ulat sa patakaran",
      "โครงสร้างรายงานนโยบาย", "پالیسی رپورٹ کی ساخت", "Siyosat hisoboti tuzilmasi", "Саясаттык отчет түзүлүшү")
    s("common.modal.report.desc",
      "주간·월간·분기별로 어떤 지표를 수집하고, 어떤 정보는 비식별 요약으로 제공할지 구성하는 화면입니다.",
      "සතිපතා, මාසික සහ කාර්තුමය ලෙස කුමන දර්ශක එකතු කරනවාද සහ කුමන තොරතුරු නිර්නාමික සාරාංශ ලෙස සපයනවාද යන්න සකසන තිරයකි.",
      "A screen to configure which indicators are collected weekly, monthly, and quarterly, and which information is provided as de-identified summaries.",
      "用于配置按周、月、季度收集哪些指标，以及哪些信息以去标识化摘要提供的界面。",
      "Screen para i-configure kung aling mga indicator ang kokolektahin lingguhan, buwanan, at quarterly, at aling impormasyon ang ibibigay bilang de-identified summary.",
      "หน้าจอสำหรับกำหนดตัวชี้วัดที่รวบรวมรายสัปดาห์ รายเดือน และรายไตรมาส และข้อมูลใดที่สรุปแบบไม่ระบุตัวตน",
      "ہفتہ وار، ماہانہ اور سہ ماہی طور پر کون سے اشارے جمع کیے جائیں اور کون سی معلومات غیر شناختہ خلاصے میں فراہم کی جائیں، اس کی ترتیب کا اسکرین۔",
      "Haftalik, oylik va choraklik qaysi ko'rsatkichlar yig'ilishi va qaysi ma'lumotlar anonim xulosa sifatida berilishini sozlash ekrani.",
      "Апталык, айлык жана чейрек боюнча кайсы көрсөткүчтөр чогултулушу жана кайсы маалыматтар анонимдүү жыйынтыкта берилиши керектигин жөндөө экраны.")

    # --- common.form ---
    s("common.form.org",
      "기관·기업명", "ආයතන/සමාගම් නාමය", "Organization / company", "机构/企业名称", "Pangalan ng organisasyon/kumpanya",
      "ชื่อหน่วยงาน/บริษัท", "ادارہ/کمپنی کا نام", "Tashkilot/kompaniya nomi", "Уюм/компания аты")
    s("common.form.name",
      "담당자명", "භාරකරුගේ නම", "Contact name", "负责人姓名", "Pangalan ng contact",
      "ชื่อผู้รับผิดชอบ", "ذمہ دار کا نام", "Mas'ul shaxs ismi", "Жооптуу адамдын аты")
    s("common.form.type",
      "문의 유형", "විමසීම් වර්ගය", "Inquiry type", "咨询类型", "Uri ng pagtatanong",
      "ประเภทการสอบถาม", "درخواست کی قسم", "So'rov turi", "Суроонун түрү")
    s("common.form.message",
      "문의 내용", "විමසීම් අන්තර්ගතය", "Message", "咨询内容", "Nilalaman ng mensahe",
      "เนื้อหาการสอบถาม", "پیغام", "Xabar matni", "Суроонун мазмуну")
    s("common.form.submit",
      "문의 내용 확인하기", "විමසීම් අන්තර්ගතය තහවුරු කරන්න", "Confirm inquiry", "确认咨询内容", "Kumpirmahin ang mensahe",
      "ยืนยันเนื้อหาการสอบถาม", "درخواست کی تصدیق", "So'rovni tasdiqlash", "Суроону ырастоо")
    s("common.form.note",
      "이 템플릿의 양식은 데모입니다. 실제 운영 시 개인정보 처리방침·동의·접근권한 체계를 별도로 적용해야 합니다.",
      "මෙම ආදර්ශ පෝරමය demo වේ. සැබෑ මෙහෙයුමේදී පෞද්ගලිකත්ව ප්‍රතිපත්තිය, එකඟතාව සහ ප්‍රවේශ අවසර පද්ධතිය වෙනම යොදා ගත යුතුය.",
      "This template form is a demo. In production, apply a separate privacy policy, consent, and access control system.",
      "此模板表单为演示用途。实际运营时需另行适用隐私政策、同意及访问权限体系。",
      "Ang form na ito ay demo. Sa aktwal na operasyon, ilapat ang hiwalay na privacy policy, pahintulot, at access control.",
      "แบบฟอร์มนี้เป็นตัวอย่างสาธิต ในการใช้งานจริงต้องใช้นโยบายความเป็นส่วนตัว ความยินยอม และสิทธิ์การเข้าถึงแยกต่างหาก",
      "یہ ٹیمپلیٹ فارم ڈیمو ہے۔ اصل آپریشن میں الگ رازداری کی پالیسی، رضامندی اور رسائی کے نظام کا اطلاق کریں۔",
      "Ushbu shablon demo hisoblanadi. Haqiqiy operatsiyada alohida maxfiylik siyosati, rozilik va kirish huquqlari tizimini qo'llang.",
      "Бул шаблон демо. Чыныгы иштетүүдө жеке маалымат саясаты, макулдук жана кирүү укуктарын өзүнчө колдонуу керек.")
    s("common.form.submitNote",
      "입력 내용이 확인되었습니다. 실제 연동 시 담당자 이메일 또는 CRM 접수 흐름으로 연결합니다.",
      "ආදානය තහවුරු විය. සැබෑ සම්බන්ධතාවේදී වගකිව යුතු ඊමේල් හෝ CRM ප්‍රවාහයට සම්බන්ධ කෙරේ.",
      "Your input has been confirmed. In a live integration, this connects to a responsible email or CRM intake flow.",
      "输入内容已确认。实际对接时将连接至负责人邮箱或CRM受理流程。",
      "Nakumpirma ang input. Sa aktwal na integrasyon, ikokonekta sa email ng responsable o CRM intake flow.",
      "ยืนยันการป้อนข้อมูลแล้ว ในการเชื่อมต่อจริงจะเชื่อมกับอีเมลผู้รับผิดชอบหรือ CRM",
      "درج کردہ معلومات کی تصدیق ہو گئی۔ اصل انضمام میں ذمہ دار ای میل یا CRM کے عمل سے منسلک ہوگا۔",
      "Kiritilgan ma'lumot tasdiqlandi. Haqiqiy integratsiyada mas'ul email yoki CRM qabul oqimiga ulanadi.",
      "Киргизилген маалымат ырасталды. Чыныгы интеграцияда жооптуу email же CRM кабыл алуу агымына туташат.")
    s("common.form.orgPlaceholder",
      "기관 또는 기업명", "ආයතනය හෝ සමාගම් නාමය", "Organization or company name", "机构或企业名称", "Pangalan ng organisasyon o kumpanya",
      "ชื่อหน่วยงานหรือบริษัท", "ادارہ یا کمپنی کا نام", "Tashkilot yoki kompaniya nomi", "Уюм же компания аты")
    s("common.form.namePlaceholder",
      "담당자 성함", "භාරකරුගේ නම", "Contact person's name", "负责人姓名", "Pangalan ng contact person",
      "ชื่อผู้รับผิดชอบ", "ذمہ دار کا نام", "Mas'ul shaxs ismi", "Жооптуу адамдын аты")
    s("common.form.messagePlaceholder",
      "도입 지역, 업종, 대상 규모, 우선 해결 과제를 적어주세요.",
      "හඳුන්වාදීමේ ප්‍රදේශය, කර්මාන්තය, ඉලක්ක පරිමාණය සහ ප්‍රමුඛ විසඳුම් කාර්යයන් ලියන්න.",
      "Please enter adoption region, industry, target scale, and priority issues to address.",
      "请填写引入地区、行业、目标规模及优先解决的问题。",
      "Ilagay ang rehiyon, industriya, target na sukat, at prayoridad na isusulong.",
      "กรอกพื้นที่นำเข้า อุตสาหกรรม ขนาดเป้าหมาย และประเด็นที่ต้องแก้ไขก่อน",
      "متعارف کرنے کا علاقہ، صنعت، ہدف کا پیمانہ اور ترجیحی مسائل درج کریں۔",
      "Joriy etish hududi, sanoat, maqsadli hajm va ustuvor vazifalarni yozing.",
      "Киргизүү аймагы, өнөр жайы, максаттуу көлөм жана башкы чечүүчү тапсырмаларды жазыңыз.")
    s("common.form.typeMunicipality",
      "지자체 위탁운영 상담", "ප්‍රාදේශීය සභා භාරකාර මෙහෙයුම් සාකච්ඡාව", "Municipal delegated operations consultation", "地方政府委托运营咨询", "Konsultasyon sa delegated operations ng munisipyo",
      "ปรึกษาการดำเนินงานแบบมอบหมายจากองค์กรปกครองท้องถิ่น", "بلدیاتی سپردہ آپریشن مشاورت", "Mahalliy hokimiyat topshirma operatsiyasi maslahati", "Жергиликтүү бийлик тапшырмачыл иштетүү кеңеши")
    s("common.form.typeCompany",
      "기업 도입 상담", "සමාගම් හඳුන්වාදීම් සාකච්ඡාව", "Company adoption consultation", "企业引入咨询", "Konsultasyon sa pagpapakilala ng kumpanya",
      "ปรึกษาการนำเข้าใช้ของบริษัท", "کمپنی متعارف کرنے کی مشاورت", "Kompaniya joriy etish maslahati", "Компанияны киргизүү боюнча кеңеш")
    s("common.form.typeEducation",
      "동반교육 프로그램 상담", "එක්ව අධ්‍යාපන ක්‍රමවේදය සාකච්ඡාව", "Co-education program consultation", "协同教育项目咨询", "Konsultasyon sa programang ko-edukasyon",
      "ปรึกษาโปรแกรมการศึกษาร่วม", "مشترکہ تعلیم پروگرام مشاورت", "Hamkor ta'lim dasturi maslahati", "Кошумча окутуу программасы боюнча кеңеш")
    s("common.form.typeReport",
      "보고·대시보드 구축 상담", "වාර්තා/උපකරණ පුවරු සැකසුම් සාකච්ඡාව", "Reporting & dashboard setup consultation", "报告与仪表板构建咨询", "Konsultasyon sa pag-setup ng ulat at dashboard",
      "ปรึกษาการสร้างรายงานและแดชบอร์ด", "رپورٹ اور ڈیش بورڈ کی تشکیل مشاورت", "Hisobot va panel sozlash maslahati", "Отчет жана панель куруу боюнча кеңеш")

    # --- common.lang ---
    s("common.lang.sectionTitle",
      "언어", "භාෂා", "Language", "语言", "Wika",
      "ภาษา", "زبان", "Til", "Тил")
    s("common.lang.switcherLabel",
      "언어 선택", "භාෂාව තෝරන්න", "Select language", "选择语言", "Pumili ng wika",
      "เลือกภาษา", "زبان منتخب کریں", "Tilni tanlash", "Тил тандоо")


# remainder populated in locale_strings_ext.py and merged at runtime
def _load_ext_strings() -> None:
    from locale_strings_ext import register_strings
    from locale_strings_worker import register_strings as register_worker
    register_strings(s)
    register_worker(s)


def main() -> None:
    populate_strings()
    _load_ext_strings()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    key_count = 0
    created: list[str] = []

    for lang in LANGS:
        flat = {path: vals[lang] for path, vals in T.items()}
        nested = build_nested(flat)
        out = OUTPUT_DIR / f"{lang}.json"
        out.write_text(json.dumps(nested, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created.append(out.name)
        if lang == "ko":
            key_count = count_keys(nested)

    print(f"Created {len(created)} locale files in {OUTPUT_DIR}:")
    for name in created:
        print(f"  - {name}")
    print(f"Total keys per locale: {key_count}")


if __name__ == "__main__":
    main()
