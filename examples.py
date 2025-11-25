#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Studio One 매크로 번역기 - 사용 예제
"""

from korean_to_s1_macro import StudioOneMacroTranslator


def example_1_basic():
    """예제 1: 기본 사용법"""
    print("\n" + "=" * 60)
    print("📌 예제 1: 기본 사용법")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 간단한 명령어
    xml = translator.translate("트랙 추가", "기본_예제")

    # 파일로 저장
    translator.save_macro(xml, "example_1_basic")


def example_2_multiple_commands():
    """예제 2: 여러 명령어 조합"""
    print("\n" + "=" * 60)
    print("📌 예제 2: 여러 명령어 조합")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 쉼표로 구분된 여러 명령어
    korean_text = "트랙 추가, 음소거, 재생"
    xml = translator.translate(korean_text, "복합_명령어")

    translator.save_macro(xml, "example_2_multiple")


def example_3_natural_language():
    """예제 3: 자연어 입력"""
    print("\n" + "=" * 60)
    print("📌 예제 3: 자연어 입력")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 자연스러운 한글 문장
    korean_text = "새 트랙을 추가하고 음소거해줘"
    xml = translator.translate(korean_text, "자연어_예제")

    translator.save_macro(xml, "example_3_natural")


def example_4_workflow():
    """예제 4: 실제 워크플로우"""
    print("\n" + "=" * 60)
    print("📌 예제 4: 실제 워크플로우 - 빠른 녹음 준비")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 녹음 시작을 위한 워크플로우
    workflow = "새 트랙, 녹음"
    xml = translator.translate(workflow, "빠른_녹음_준비")

    translator.save_macro(xml, "example_4_quick_record")


def example_5_mixing_workflow():
    """예제 5: 믹싱 워크플로우"""
    print("\n" + "=" * 60)
    print("📌 예제 5: 믹싱 워크플로우")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 믹싱을 위한 뷰 설정
    workflow = "믹서 열기, 브라우저 열기, 인스펙터 열기"
    xml = translator.translate(workflow, "믹싱_뷰_설정")

    translator.save_macro(xml, "example_5_mixing_setup")


def example_6_editing_workflow():
    """예제 6: 편집 워크플로우"""
    print("\n" + "=" * 60)
    print("📌 예제 6: 편집 워크플로우 - 복사/붙여넣기")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 편집 작업
    workflow = "전체 선택, 복사, 붙여넣기"
    xml = translator.translate(workflow, "복사_붙여넣기")

    translator.save_macro(xml, "example_6_copy_paste")


def example_7_custom_command():
    """예제 7: 커스텀 명령어 추가"""
    print("\n" + "=" * 60)
    print("📌 예제 7: 커스텀 명령어 추가")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 커스텀 명령어 추가
    translator.add_custom_command(
        korean_name="템포 120",
        s1_command="Transport.Tempo",
        args={"BPM": "120"}
    )

    translator.add_custom_command(
        korean_name="페이드 인",
        s1_command="Audio.FadeIn",
        args={}
    )

    # 커스텀 명령어 사용
    workflow = "템포 120, 페이드 인, 재생"
    xml = translator.translate(workflow, "커스텀_워크플로우")

    translator.save_macro(xml, "example_7_custom")


def example_8_complex_workflow():
    """예제 8: 복잡한 워크플로우"""
    print("\n" + "=" * 60)
    print("📌 예제 8: 복잡한 프로덕션 워크플로우")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 프로덕션 시작 워크플로우
    workflow = """
    믹서 열기,
    브라우저 열기,
    인스펙터 열기,
    새 트랙,
    리버브 추가,
    컴프레서 추가
    """

    xml = translator.translate(workflow, "프로덕션_시작")
    translator.save_macro(xml, "example_8_production_start")


def example_9_list_all_commands():
    """예제 9: 사용 가능한 모든 명령어 보기"""
    print("\n" + "=" * 60)
    print("📌 예제 9: 사용 가능한 모든 명령어 보기")
    print("=" * 60)

    translator = StudioOneMacroTranslator()
    translator.list_commands()


def example_10_batch_create():
    """예제 10: 여러 매크로 일괄 생성"""
    print("\n" + "=" * 60)
    print("📌 예제 10: 여러 매크로 일괄 생성")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 자주 사용하는 매크로들을 한 번에 생성
    macros = {
        "빠른_재생": "재생",
        "빠른_정지": "정지",
        "빠른_녹음": "녹음",
        "음소거_토글": "음소거",
        "솔로_토글": "솔로",
        "전체복사": "전체 선택, 복사",
        "실행취소": "실행 취소",
        "다시실행": "다시 실행",
        "새_오디오_트랙": "트랙 추가",
        "트랙_삭제": "트랙 삭제",
    }

    for name, korean_cmd in macros.items():
        xml = translator.translate(korean_cmd, name)
        translator.save_macro(xml, f"batch_{name}")

    print(f"\n✅ {len(macros)}개의 매크로가 생성되었습니다!")


def run_all_examples():
    """모든 예제 실행"""
    print("\n" + "=" * 80)
    print("🎵 Studio One 매크로 번역기 - 예제 모음")
    print("=" * 80)

    examples = [
        example_1_basic,
        example_2_multiple_commands,
        example_3_natural_language,
        example_4_workflow,
        example_5_mixing_workflow,
        example_6_editing_workflow,
        example_7_custom_command,
        example_8_complex_workflow,
        example_9_list_all_commands,
        example_10_batch_create,
    ]

    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"❌ {example_func.__name__} 실행 중 오류: {e}")

    print("\n" + "=" * 80)
    print("✅ 모든 예제가 완료되었습니다!")
    print("=" * 80)
    print("\n생성된 파일들:")
    import os
    macro_files = [f for f in os.listdir('.') if f.endswith('.studioonemacro')]
    for i, filename in enumerate(sorted(macro_files), 1):
        print(f"  {i}. {filename}")


if __name__ == "__main__":
    # 개별 예제 실행:
    # example_1_basic()
    # example_2_multiple_commands()
    # ...

    # 또는 모든 예제 실행:
    run_all_examples()
