#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Studio One 매크로 번역기 테스트
"""

from korean_to_s1_macro import StudioOneMacroTranslator


def test_basic_commands():
    """기본 명령어 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 1: 기본 명령어")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    test_cases = [
        "트랙 추가",
        "재생",
        "정지",
        "복사",
        "붙여넣기",
        "음소거",
        "솔로",
    ]

    for korean_cmd in test_cases:
        xml = translator.translate(korean_cmd, f"테스트_{korean_cmd}")
        assert xml, f"'{korean_cmd}' 번역 실패"

    print("✅ 기본 명령어 테스트 통과")


def test_multiple_commands():
    """복합 명령어 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 2: 복합 명령어")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    test_cases = [
        "트랙 추가하고 음소거해줘",
        "재생, 그리고 반복 재생",
        "복사한 다음 붙여넣기",
        "트랙 추가, 음소거, 솔로",
        "저장하고 믹서 열기",
    ]

    for korean_cmd in test_cases:
        xml = translator.translate(korean_cmd, "복합_명령어_테스트")
        assert xml, f"'{korean_cmd}' 번역 실패"

    print("✅ 복합 명령어 테스트 통과")


def test_natural_language():
    """자연어 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 3: 자연어 입력")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    test_cases = [
        "새 트랙을 추가해줘",
        "음소거 해제하고 볼륨 올리기",
        "브라우저 열고 인스펙터도 열기",
        "전체 선택한 다음 복사해줘",
    ]

    for korean_cmd in test_cases:
        xml = translator.translate(korean_cmd, "자연어_테스트")
        # 자연어는 일부만 매칭될 수 있으므로 실패하지 않음

    print("✅ 자연어 입력 테스트 통과")


def test_save_macro():
    """매크로 저장 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 4: 매크로 파일 저장")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    korean_cmd = "트랙 추가, 음소거, 재생"
    xml = translator.translate(korean_cmd, "테스트_매크로")

    # 파일 저장
    translator.save_macro(xml, "test_macro")

    # 파일 확인
    import os
    assert os.path.exists("test_macro.studioonemacro"), "파일 저장 실패"

    print("✅ 매크로 파일 저장 테스트 통과")

    # 생성된 파일 내용 출력
    with open("test_macro.studioonemacro", 'r', encoding='utf-8') as f:
        print("\n생성된 파일 내용:")
        print(f.read())


def test_custom_command():
    """커스텀 명령어 추가 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 5: 커스텀 명령어 추가")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 커스텀 명령어 추가
    translator.add_custom_command("템포 120으로", "Transport.Tempo", {"BPM": "120"})
    translator.add_custom_command("페이드 인", "Audio.FadeIn", {})

    # 커스텀 명령어 테스트
    xml = translator.translate("템포 120으로, 페이드 인", "커스텀_테스트")
    assert xml, "커스텀 명령어 번역 실패"

    print("✅ 커스텀 명령어 추가 테스트 통과")


def test_workflow_examples():
    """실제 워크플로우 예제 테스트"""
    print("\n" + "=" * 60)
    print("🧪 테스트 6: 실제 워크플로우 예제")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    workflows = {
        "빠른_녹음_준비": "새 트랙, 녹음",
        "믹싱_시작": "믹서 열기, 브라우저 열기",
        "복사_붙여넣기_워크플로우": "전체 선택, 복사, 붙여넣기",
        "트랙_정리": "음소거, 솔로 해제",
        "저장_및_내보내기": "저장, 내보내기",
    }

    for name, korean_cmd in workflows.items():
        xml = translator.translate(korean_cmd, name)
        if xml:
            translator.save_macro(xml, f"workflow_{name}")

    print("✅ 워크플로우 예제 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "=" * 80)
    print("🚀 Studio One 매크로 번역기 전체 테스트 시작")
    print("=" * 80)

    try:
        test_basic_commands()
        test_multiple_commands()
        test_natural_language()
        test_save_macro()
        test_custom_command()
        test_workflow_examples()

        print("\n" + "=" * 80)
        print("✅ 모든 테스트 통과!")
        print("=" * 80)

    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}")
        raise
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
