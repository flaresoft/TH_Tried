# 🎵 Studio One 7 한글 매크로 번역기

**한글 자연어로 Studio One 7 매크로를 만드세요!**

Studio One 7의 복잡한 매크로 문법을 몰라도, 한글로 명령어를 입력하면 자동으로 `.studioonemacro` 파일로 변환해주는 번역 프로그램입니다.

## ✨ 주요 기능

- 🇰🇷 **한글 자연어 입력**: "트랙 추가하고 음소거해줘" 같은 자연스러운 한글 명령어 사용
- 🎯 **자동 변환**: Studio One 7 매크로 XML 형식으로 자동 변환
- 💾 **파일 저장**: `.studioonemacro` 파일로 바로 저장
- 🔧 **커스텀 명령어**: 원하는 명령어를 직접 추가 가능
- 📋 **풍부한 기본 명령어**: 50+ 개의 기본 한글 명령어 내장

## 🚀 빠른 시작

### 설치

```bash
git clone https://github.com/flaresoft/TH_Tried.git
cd TH_Tried
```

Python 3.6 이상이 필요합니다. 추가 패키지 설치는 필요 없습니다!

### 사용법

#### 1. 대화형 모드

```bash
python3 korean_to_s1_macro.py
```

프로그램을 실행하면 대화형 인터페이스가 시작됩니다:

```
============================================================
🎵 Studio One 7 한글 매크로 번역기 🎵
============================================================
한글로 명령어를 입력하면 Studio One 매크로로 번역해드립니다!
명령어: 'list' - 사용 가능한 명령어 보기
명령어: 'quit' - 종료
============================================================

한글 명령어 입력: 트랙 추가, 음소거, 재생
매크로 이름 (엔터: 'My Macro'): 빠른_녹음

🔄 번역 시작: 트랙 추가, 음소거, 재생
============================================================
✅ 3개의 명령어 인식:
   1. Track.Add
   2. Track.Mute
   3. Transport.Play

📄 생성된 매크로:
<?xml version="1.0" ?>
<Macro version="1.0" name="빠른_녹음">
  <Commands>
    <Command name="Track.Add"/>
    <Command name="Track.Mute"/>
    <Command name="Transport.Play"/>
  </Commands>
</Macro>
============================================================

파일로 저장하시겠습니까? (y/n): y
파일명 입력: my_quick_recording
💾 매크로 저장 완료: my_quick_recording.studioonemacro
```

#### 2. Python 코드에서 사용

```python
from korean_to_s1_macro import StudioOneMacroTranslator

# 번역기 생성
translator = StudioOneMacroTranslator()

# 한글 명령어 번역
xml = translator.translate("트랙 추가, 음소거, 재생", "나의_매크로")

# 파일로 저장
translator.save_macro(xml, "my_macro")
```

## 📖 사용 가능한 명령어

### 트랙 관련
- `트랙 추가`, `새 트랙` → 새 트랙 추가
- `트랙 삭제` → 트랙 삭제
- `트랙 복제` → 트랙 복제

### 재생 관련
- `재생` → 재생
- `정지`, `멈춤` → 정지
- `녹음` → 녹음
- `처음으로` → 처음으로 돌아가기
- `반복 재생` → 반복 재생 켜기
- `반복 끄기` → 반복 재생 끄기

### 편집 관련
- `복사` → 복사
- `붙여넣기` → 붙여넣기
- `잘라내기` → 잘라내기
- `실행 취소` → Undo
- `다시 실행` → Redo
- `삭제` → 삭제
- `전체 선택` → 모두 선택

### 믹싱 관련
- `음소거`, `무음` → Mute
- `솔로` → Solo
- `음소거 해제` → Unmute
- `솔로 해제` → Unsolo

### 볼륨 관련
- `볼륨 올리기`, `음량 올리기` → 볼륨 증가
- `볼륨 내리기`, `음량 내리기` → 볼륨 감소

### 줌 관련
- `확대`, `축소` → 줌
- `수평 확대`, `수평 축소` → 가로 줌
- `수직 확대`, `수직 축소` → 세로 줌

### 저장 관련
- `저장` → 저장
- `다른 이름으로 저장` → 다른 이름으로 저장
- `내보내기` → Export

### 뷰 관련
- `믹서 열기`, `믹서 닫기` → 믹서 토글
- `브라우저 열기`, `브라우저 닫기` → 브라우저 토글
- `인스펙터 열기`, `인스펙터 닫기` → 인스펙터 토글

### 이펙트 관련
- `리버브 추가`, `딜레이 추가`, `컴프레서 추가`, `EQ 추가`

### 마커 관련
- `마커 추가`, `마커 삭제`

**전체 명령어 보기**: 프로그램에서 `list` 명령어 입력

## 💡 예제

### 예제 1: 빠른 녹음 준비
```
한글: "새 트랙, 녹음"
결과: Track.Add → Transport.Record
```

### 예제 2: 믹싱 시작
```
한글: "믹서 열기, 브라우저 열기"
결과: View.Mixer (State=1) → View.Browser (State=1)
```

### 예제 3: 복사-붙여넣기 워크플로우
```
한글: "전체 선택, 복사, 붙여넣기"
결과: Edit.SelectAll → Edit.Copy → Edit.Paste
```

### 예제 4: 자연어 입력
```
한글: "트랙을 추가하고 음소거해줘"
결과: Track.Add → Track.Mute
```

## 🔧 커스텀 명령어 추가

원하는 명령어를 직접 추가할 수 있습니다:

```python
translator = StudioOneMacroTranslator()

# 커스텀 명령어 추가
translator.add_custom_command(
    korean_name="템포 120으로",
    s1_command="Transport.Tempo",
    args={"BPM": "120"}
)

# 사용
xml = translator.translate("템포 120으로, 재생")
```

## 📁 파일 구조

```
TH_Tried/
├── korean_to_s1_macro.py      # 메인 번역기 프로그램
├── test_translator.py          # 테스트 스크립트
├── README.md                   # 이 문서
└── *.studioonemacro           # 생성된 매크로 파일들
```

## 🧪 테스트

```bash
python3 test_translator.py
```

테스트를 실행하면 다음 항목들이 자동으로 검증됩니다:
- ✅ 기본 명령어 번역
- ✅ 복합 명령어 처리
- ✅ 자연어 입력
- ✅ 파일 저장
- ✅ 커스텀 명령어
- ✅ 실제 워크플로우 예제

## 📝 Studio One에서 매크로 사용하기

1. 생성된 `.studioonemacro` 파일을 복사
2. Studio One의 Macros 폴더에 붙여넣기
   - Windows: `%USERPROFILE%\Documents\Studio One\Macros`
   - macOS: `~/Documents/Studio One/Macros`
3. Studio One 재시작 또는 Macro Organizer에서 새로고침
4. Macro Toolbar에서 매크로 사용

## 🤝 기여하기

새로운 명령어 추가, 버그 수정, 기능 개선 등 모든 기여를 환영합니다!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

This project is open source and available under the MIT License.

## 🔗 참고 자료

- [Studio One Manual - Macro Toolbar](https://s1manual.presonus.com/en/Content/Editing_Topics/Macro_Toolbar.htm)
- [Studio One Toolbox - Macro Documentation](https://s1toolbox.com/macrodocumentation)
- [Getting started with Macros in Studio One](https://studiooneforum.com/threads/getting-started-with-macros-in-studio-one-crash-course.22/)

## 💬 문의 및 지원

이슈가 있거나 질문이 있으시면 GitHub Issues에 등록해주세요.

---

**Made with ❤️ for Studio One users**