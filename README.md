# Resonance Detector VST3 Plugin

Studio One 7 호환 VST3 플러그인 - 실시간 레조넌스 감지 및 표시

## 기능

- **실시간 레조넌스 감지**: FFT 분석을 통해 오디오 신호에서 레조넌스를 자동으로 감지합니다
- **주파수 맵 시각화**: 20Hz ~ 20kHz 범위의 주파수 스펙트럼과 감지된 레조넌스를 시각적으로 표시
- **지속적인 레조넌스 추적**: 감지된 레조넌스는 Reset 버튼을 누르기 전까지 계속 유지됩니다
- **Q 팩터 표시**: 각 레조넌스의 품질 계수(Q Factor)를 함께 표시

## 빌드 방법

### 필수 요구사항

- CMake 3.15 이상
- C++17 호환 컴파일러
  - Windows: Visual Studio 2019 이상
  - macOS: Xcode 11 이상
  - Linux: GCC 9 이상

### 빌드 단계

1. 저장소 클론:
```bash
git clone https://github.com/flaresoft/TH_Tried.git
cd TH_Tried
```

2. 빌드 디렉토리 생성 및 CMake 실행:
```bash
mkdir build
cd build
cmake ..
```

3. 빌드:
```bash
cmake --build . --config Release
```

빌드가 완료되면 VST3 플러그인이 자동으로 시스템의 VST3 플러그인 폴더에 복사됩니다.

### VST3 플러그인 위치

- **Windows**: `C:\Program Files\Common Files\VST3\`
- **macOS**: `~/Library/Audio/Plug-Ins/VST3/` 또는 `/Library/Audio/Plug-Ins/VST3/`
- **Linux**: `~/.vst3/`

## 사용 방법

1. Studio One 7에서 오디오 트랙 또는 악기 트랙에 "Resonance Detector" 플러그인을 추가합니다
2. 오디오를 재생하면 실시간으로 레조넌스가 감지되어 주파수 맵에 표시됩니다
3. 감지된 레조넌스는 빨간색 점으로 표시되며, 주파수와 Q 팩터 정보가 함께 표시됩니다
4. "Reset Resonances" 버튼을 클릭하면 감지된 레조넌스를 초기화할 수 있습니다

## 기술 상세

- **FFT 크기**: 8192 샘플 (고해상도 주파수 분석)
- **윈도우 함수**: Hann 윈도우
- **최소 Q 팩터**: 2.0 (낮은 Q 값의 노이즈 필터링)
- **주파수 범위**: 20Hz ~ 20kHz
- **UI 업데이트 속도**: 30 FPS

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트를 환영합니다!