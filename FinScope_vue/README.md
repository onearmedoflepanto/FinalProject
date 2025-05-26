# FinScope_vue

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

---

## 금리 변동시 이메일 알림 기능 상세

본 프로젝트에는 사용자가 관심 금융상품(예/적금)의 금리 변동시 이메일로 알림을 받을 수 있는 기능이 구현되었습니다. 주요 변경 사항 및 구성 요소는 다음과 같습니다.

### 주요 기능:
- 사용자는 금융상품 상세 페이지에서 특정 상품에 대한 금리 변동 알림을 구독하거나 구독 취소할 수 있습니다.
- 관리자는 Django Admin 페이지에서 직접 금융상품의 금리 정보를 수정할 수 있으며, 이 변경 사항은 구독한 사용자에게 알림을 트리거합니다.
- 백그라운드에서 주기적으로 금융감독원 API를 통해 최신 금융상품 정보를 가져와 데이터베이스를 업데이트하고, 이때 금리 변동이 감지되면 자동으로 알림을 발송합니다.

### Django 백엔드 변경 사항 (`FinScope_Django/`):
1.  **모델 (`accounts/models.py`):**
    *   `FinancialProduct`: 금융상품의 상세 정보(은행명, 상품명, 각종 조건 등)를 저장합니다.
    *   `ProductOption`: `FinancialProduct`에 연결되어 기간별 금리(6개월, 12개월 등) 및 금리 유형(단리/복리) 등의 옵션 정보를 저장합니다.
    *   `SavedFinancialProduct`: 기존 모델에 `notify_on_rate_change` (boolean) 필드를 추가하여 사용자의 알림 구독 상태를 저장하고, `financial_product_ref`를 추가하여 `FinancialProduct` 모델과 연결했습니다.
2.  **데이터베이스 마이그레이션:** 모델 변경 사항을 DB에 반영했습니다.
3.  **설정 (`FinScope/settings.py`):**
    *   이메일 발송을 위해 Gmail SMTP 설정을 추가했습니다 (`EMAIL_BACKEND`, `EMAIL_HOST` 등). 실제 이메일 발송을 위해서는 `.env` 파일에 `EMAIL_HOST_USER` (Gmail 주소) 및 `EMAIL_HOST_PASSWORD` (Gmail 앱 비밀번호) 설정이 필요합니다.
    *   금융감독원 API 키 (`VITE_FSS_API_KEY`)를 `.env`에서 로드하도록 설정했습니다.
4.  **Admin (`accounts/admin.py`):**
    *   `FinancialProduct`, `ProductOption`, `SavedFinancialProduct` 모델을 Django Admin에 등록했습니다.
    *   `FinancialProduct` 관리 페이지에서 `ProductOption`(금리 정보)을 인라인으로 직접 수정할 수 있게 설정했습니다.
    *   관리자가 `ProductOption`의 `intr_rate` (금리)를 변경하고 저장하면, 해당 상품을 구독한 사용자들에게 자동으로 금리 변동 알림 이메일이 발송되도록 `save_model` 메서드를 오버라이드했습니다.
5.  **API 뷰 (`accounts/views.py`):**
    *   `FinancialProductListView`: Django DB에 저장된 금융상품 목록을 제공하는 API 엔드포인트를 추가했습니다. (Vue 앱이 이 엔드포인트를 통해 상품 정보를 가져옵니다.)
    *   `toggle_product_notification`: 사용자가 특정 저장 상품에 대한 알림 구독 상태를 변경할 수 있는 API 엔드포인트를 추가했습니다.
6.  **URL (`accounts/urls.py`):** 위에서 언급된 새로운 API 뷰들에 대한 URL 경로를 추가했습니다.
7.  **관리 명령어:**
    *   `fetch_fss_products` (`accounts/management/commands/`): 금융감독원 API로부터 예/적금 상품 정보를 주기적으로 가져와 Django DB의 `FinancialProduct`, `ProductOption` 모델을 업데이트합니다. 이 과정에서 금리 변동이 감지되면 구독자에게 알림 이메일을 발송합니다. **이 명령어는 서버에서 cron job 등으로 주기적 실행이 필요합니다.**
    *   `send_test_notification` (`accounts/management/commands/`): 특정 상품 ID에 대해 구독자에게 테스트 알림을 발송하는 명령어입니다 (개발/테스트용).
8.  **알림 로직 (`accounts/notifications.py`):**
    *   `dispatch_rate_change_notifications`: 특정 금융상품의 금리가 변경되었을 때 구독자들에게 이메일을 실제로 구성하고 발송하는 함수입니다.

### Vue.js 프론트엔드 변경 사항 (`FinScope_vue/`):
1.  **API 호출 (`src/api/depositSavingsApi.js`):**
    *   `fetchDepositProducts`, `fetchSavingsProducts` 함수를 수정하여, 기존의 FSS API 직접 호출(Vite 프록시 경유) 방식에서 Django 백엔드의 새로운 `/api/accounts/financial-products/` 엔드포인트를 호출하도록 변경했습니다.
    *   `toggleNotificationSubscription` 함수를 추가하여, 사용자가 알림 구독 상태를 변경할 수 있도록 Django API를 호출합니다.
2.  **상품 목록 페이지 (`src/views/DepositPage.vue`):**
    *   데이터 fetching 로직을 수정하여 Django 백엔드로부터 상품 정보를 가져오도록 변경했습니다.
    *   새로운 데이터 구조에 맞게 상품 정보(은행명, 상품명, 금리 등) 표시 방식을 조정했습니다.
    *   상품 상세 정보 확장 시, "MyPage에 저장" 버튼 옆에 "금리변동 알림받기" / "알림 해제" 버튼을 추가했습니다. 이 버튼은 사용자가 로그인하고 해당 상품을 저장했을 경우에만 표시됩니다.
    *   `isSubscribedToNotifications` 계산된 속성을 추가하여 알림 구독 상태에 따라 버튼의 텍스트와 모양이 동적으로 변경되도록 했습니다.
    *   `handleToggleNotification` 메소드를 추가하여 알림 구독/해지 API 호출 및 UI 상태 업데이트를 처리합니다.

### 환경 설정 (`.env` 및 `.env.example`):
-   `FinScope_Django/.env.example`: Django 백엔드 실행에 필요한 환경 변수(시크릿 키, FSS API 키, 이메일 계정 정보 등) 목록을 업데이트했습니다.
-   `FinScope_vue/.env.example`: Vue 프론트엔드 실행에 필요한 환경 변수 목록을 확인했습니다.

이러한 변경을 통해 사용자는 관심 상품의 금리 변동 정보를 이메일로 받아볼 수 있게 되었으며, 관리자는 시스템의 금융상품 정보를 직접 관리하고 필요시 알림을 유도할 수 있습니다. 데이터의 최신 상태 유지를 위해서는 `fetch_fss_products` 명령어의 주기적인 자동 실행이 중요합니다.
