# Global Workforce Operations — 1차 템플릿

## 배포 현황

| 항목 | URL |
|------|-----|
| GitHub | [github.com/NurionHoldings/gwo](https://github.com/NurionHoldings/gwo) |
| Netlify (미리보기) | [dulcet-piroshki-12725e.netlify.app](https://dulcet-piroshki-12725e.netlify.app) |
| 커스텀 도메인 (예정) | `www.globalworkforceoperations.com` |

홈·상세 페이지·다국어·에셋 모두 Netlify에서 정상 서비스 중입니다.

## 포함 내용
- 지자체 위탁 핵심업무 3종
  1. 입국 후 채용기업 동반교육
  2. 적응·안전 상태 점검 및 조기지원
  3. 이직·근무처 변경 업무 지원
- 근로자 다국어 교육 화면 예시
- AI법친 연계 영역 예시
- 지자체 / 기업체 / 운영센터 역할별 대시보드 예시
- 정기보고 및 담당 공무원 이메일 보고 예시
- CEO 및 연락처 반영

## 실행 (로컬)
`index.html` 파일을 브라우저로 열거나 Live Server로 열면 됩니다.

## GitHub → Netlify 배포

이 템플릿은 **정적 사이트**이므로 별도 빌드 없이 Netlify에 배포합니다.

### 1. GitHub 저장소 준비

`gwo-template` 폴더 내용을 **저장소 루트**로 푸시합니다.

```bash
cd gwo-template
git init
git add .
git commit -m "Initial commit: GWO template"
git branch -M main
git remote add origin https://github.com/NurionHoldings/gwo.git
git push -u origin main
```

> 상위 `GWO` 폴더 전체를 저장소로 쓸 경우, Netlify UI에서 **Publish directory**를 `gwo-template`로 지정하세요.

### 2. Netlify 사이트 연결

1. [Netlify](https://app.netlify.com) → **Add new site** → **Import an existing project**
2. **GitHub** 저장소 선택
3. 빌드 설정 (`netlify.toml`이 자동 적용됨)
   - **Build command:** *(비움)*
   - **Publish directory:** `.`
4. **Deploy site**

### 3. 커스텀 도메인

Netlify → **Domain management** → **Add domain**:

| 도메인 | 용도 |
|--------|------|
| `www.globalworkforceoperations.com` | Primary (권장) |
| `globalworkforceoperations.com` | Apex → `www`로 301 리다이렉트 (`netlify.toml` 설정됨) |

도메인 등록업체 DNS 예시:

```
www     CNAME   dulcet-piroshki-12725e.netlify.app
@       ALIAS  또는 A   Netlify Domain management 화면 안내값
```

Netlify → **Domain management** → `www.globalworkforceoperations.com` 추가 후, 위 CNAME을 등록하면 SSL이 자동 발급됩니다. 커스텀 도메인 연결 후 Netlify에서 **Primary domain**을 `www`로 지정하세요.

### 4. 배포 후 확인

- [dulcet-piroshki-12725e.netlify.app](https://dulcet-piroshki-12725e.netlify.app) (현재)
- `https://www.globalworkforceoperations.com/` (커스텀 도메인 연결 후)
- `/sitemap.xml`, `/robots.txt`
- 언어 전환·상세 페이지 링크·모바일 줄바꿈

### 5. 로케일 수정 시

`assets/locales/ko.json` 등을 수정한 뒤, 필요하면 로컬에서 `py build-locales.py` 실행 후 커밋·푸시하면 Netlify가 자동 재배포합니다.

### 배포 전 체크

- `assets/logo-icon.png` — 헤더 로고 이미지가 저장소에 포함되어 있는지 확인
- 협력 문의 폼은 현재 **데모**(제출 미연동). 실제 수신이 필요하면 Netlify Forms 또는 별도 API 연동

## 구현 전 확인이 필요한 항목
- 실제 지자체명 및 지역별 사업명
- 법인명, 사업자 정보, 이메일, 주소
- 실제 보고서 수신자·승인 절차
- 개인정보·민감정보 처리방침 및 권한체계
- AI법친 연결 URL 및 상담 접수 방식
- 다국어 우선 대상 언어와 업종별 매뉴얼 원문
