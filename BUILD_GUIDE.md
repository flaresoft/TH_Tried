# Resonance Detector VST3 빌드 가이드

이 문서는 Resonance Detector VST3 플러그인을 빌드하는 상세한 가이드입니다.

## 사전 준비

### Windows

1. **Visual Studio 2019 이상** 설치
   - "C++를 사용한 데스크톱 개발" 워크로드 선택
   - CMake 도구 포함

2. **CMake** (Visual Studio에 포함되지 않은 경우)
   - https://cmake.org/download/ 에서 다운로드
   - 설치 시 "Add CMake to system PATH" 옵션 선택

### macOS

1. **Xcode** 설치
   ```bash
   xcode-select --install
   ```

2. **CMake** 설치
   ```bash
   brew install cmake
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install build-essential cmake git
sudo apt-get install libasound2-dev libx11-dev libxext-dev libxrandr-dev \
                     libxinerama-dev libxcursor-dev libfreetype6-dev \
                     libgl1-mesa-dev
```

## 빌드 프로세스

### 1. 저장소 클론

```bash
git clone https://github.com/flaresoft/TH_Tried.git
cd TH_Tried
```

### 2. 빌드 디렉토리 생성

```bash
mkdir build
cd build
```

### 3. CMake 구성

#### Windows (Visual Studio)
```bash
cmake .. -G "Visual Studio 16 2019" -A x64
```

#### macOS / Linux
```bash
cmake .. -DCMAKE_BUILD_TYPE=Release
```

### 4. 빌드 실행

#### Windows
```bash
cmake --build . --config Release
```

또는 Visual Studio에서 생성된 `.sln` 파일을 열어서 빌드할 수 있습니다.

#### macOS / Linux
```bash
cmake --build . --config Release -j 4
```

(`-j 4`는 4개의 CPU 코어를 사용하여 병렬 빌드를 수행합니다)

## 빌드 결과물

빌드가 성공하면 다음 위치에서 플러그인을 찾을 수 있습니다:

- **Windows**: `build\ResonanceDetector_artefacts\Release\VST3\ResonanceDetector.vst3`
- **macOS**: `build/ResonanceDetector_artefacts/Release/VST3/ResonanceDetector.vst3`
- **Linux**: `build/ResonanceDetector_artefacts/Release/VST3/ResonanceDetector.vst3`

## 플러그인 설치

빌드된 VST3 파일을 DAW가 인식할 수 있는 위치로 복사합니다:

### Windows
```bash
copy build\ResonanceDetector_artefacts\Release\VST3\ResonanceDetector.vst3 "%CommonProgramFiles%\VST3\"
```

### macOS
```bash
cp -r build/ResonanceDetector_artefacts/Release/VST3/ResonanceDetector.vst3 ~/Library/Audio/Plug-Ins/VST3/
```

### Linux
```bash
mkdir -p ~/.vst3
cp -r build/ResonanceDetector_artefacts/Release/VST3/ResonanceDetector.vst3 ~/.vst3/
```

## 문제 해결

### JUCE 다운로드 실패

CMake가 JUCE를 자동으로 다운로드하지 못하는 경우:

1. 수동으로 JUCE를 다운로드:
   ```bash
   git clone --branch 7.0.9 https://github.com/juce-framework/JUCE.git
   ```

2. CMakeLists.txt에서 `FetchContent_Declare` 부분을 수정:
   ```cmake
   set(JUCE_DIR "${CMAKE_SOURCE_DIR}/JUCE")
   add_subdirectory(${JUCE_DIR})
   ```

### 컴파일 오류

- C++17 지원 확인: 컴파일러가 C++17을 지원하는지 확인하세요
- JUCE 버전: JUCE 7.0.9 이상을 사용하고 있는지 확인하세요

### DAW에서 플러그인이 보이지 않음

1. DAW를 재시작합니다
2. DAW의 플러그인 스캔 기능을 실행합니다
3. VST3 경로가 올바른지 확인합니다

## 개발 모드

개발 중에는 다음과 같이 디버그 빌드를 사용할 수 있습니다:

```bash
cmake .. -DCMAKE_BUILD_TYPE=Debug
cmake --build . --config Debug
```

디버그 빌드는 더 많은 로깅과 어설션을 포함하여 문제 진단에 도움이 됩니다.

## 추가 정보

- JUCE 프레임워크: https://juce.com/
- VST3 SDK 문서: https://steinbergmedia.github.io/vst3_doc/
- 문제가 발생하면 GitHub Issues에 보고해주세요: https://github.com/flaresoft/TH_Tried/issues
