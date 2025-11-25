#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Studio One 7 한글 자연어 → 매크로 번역기
Korean Natural Language to Studio One 7 Macro Translator
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re
from typing import List, Dict, Tuple, Optional
import json


class StudioOneMacroTranslator:
    """Studio One 매크로를 한글 자연어로 작성할 수 있게 해주는 번역기"""

    def __init__(self):
        # 한글 명령어 → Studio One 명령어 매핑
        self.command_map = {
            # 트랙 관련
            "트랙 추가": {"command": "Track.Add", "args": {}},
            "트랙 삭제": {"command": "Track.Remove", "args": {}},
            "트랙을 추가": {"command": "Track.Add", "args": {}},
            "트랙을 삭제": {"command": "Track.Remove", "args": {}},
            "새 트랙": {"command": "Track.Add", "args": {}},
            "트랙 복제": {"command": "Track.Duplicate", "args": {}},

            # 재생 관련
            "재생": {"command": "Transport.Play", "args": {}},
            "정지": {"command": "Transport.Stop", "args": {}},
            "멈춤": {"command": "Transport.Stop", "args": {}},
            "일시정지": {"command": "Transport.Stop", "args": {}},
            "녹음": {"command": "Transport.Record", "args": {}},
            "처음으로": {"command": "Transport.Return", "args": {}},
            "반복 재생": {"command": "Transport.Loop", "args": {"State": "1"}},
            "반복 끄기": {"command": "Transport.Loop", "args": {"State": "0"}},

            # 편집 관련
            "복사": {"command": "Edit.Copy", "args": {}},
            "붙여넣기": {"command": "Edit.Paste", "args": {}},
            "잘라내기": {"command": "Edit.Cut", "args": {}},
            "실행 취소": {"command": "Edit.Undo", "args": {}},
            "다시 실행": {"command": "Edit.Redo", "args": {}},
            "삭제": {"command": "Edit.Delete", "args": {}},
            "전체 선택": {"command": "Edit.SelectAll", "args": {}},

            # 믹싱 관련
            "음소거": {"command": "Track.Mute", "args": {}},
            "솔로": {"command": "Track.Solo", "args": {}},
            "무음": {"command": "Track.Mute", "args": {}},
            "음소거 해제": {"command": "Track.UnMute", "args": {}},
            "솔로 해제": {"command": "Track.UnSolo", "args": {}},

            # 볼륨 관련
            "볼륨 올리기": {"command": "Track.VolumeUp", "args": {}},
            "볼륨 내리기": {"command": "Track.VolumeDown", "args": {}},
            "음량 올리기": {"command": "Track.VolumeUp", "args": {}},
            "음량 내리기": {"command": "Track.VolumeDown", "args": {}},

            # 줌 관련
            "확대": {"command": "Zoom.In", "args": {}},
            "축소": {"command": "Zoom.Out", "args": {}},
            "수평 확대": {"command": "Zoom.InHorizontal", "args": {}},
            "수평 축소": {"command": "Zoom.OutHorizontal", "args": {}},
            "수직 확대": {"command": "Zoom.InVertical", "args": {}},
            "수직 축소": {"command": "Zoom.OutVertical", "args": {}},

            # 저장 관련
            "저장": {"command": "File.Save", "args": {}},
            "다른 이름으로 저장": {"command": "File.SaveAs", "args": {}},
            "내보내기": {"command": "File.Export", "args": {}},

            # 뷰 관련
            "믹서 열기": {"command": "View.Mixer", "args": {"State": "1"}},
            "믹서 닫기": {"command": "View.Mixer", "args": {"State": "0"}},
            "브라우저 열기": {"command": "View.Browser", "args": {"State": "1"}},
            "브라우저 닫기": {"command": "View.Browser", "args": {"State": "0"}},
            "인스펙터 열기": {"command": "View.Inspector", "args": {"State": "1"}},
            "인스펙터 닫기": {"command": "View.Inspector", "args": {"State": "0"}},

            # 이펙트 관련
            "리버브 추가": {"command": "Insert.Effect", "args": {"Name": "Reverb"}},
            "딜레이 추가": {"command": "Insert.Effect", "args": {"Name": "Delay"}},
            "컴프레서 추가": {"command": "Insert.Effect", "args": {"Name": "Compressor"}},
            "EQ 추가": {"command": "Insert.Effect", "args": {"Name": "EQ"}},

            # 마커 관련
            "마커 추가": {"command": "Marker.Add", "args": {}},
            "마커 삭제": {"command": "Marker.Remove", "args": {}},
        }

        # 불필요한 접미사/접두사 (명령어 정리용)
        self.noise_words = [
            "해줘", "해주세요", "하세요", "해", "하기", "을", "를", "은", "는", "이", "가", "도", "요"
        ]

    def parse_korean_command(self, korean_text: str) -> List[Dict]:
        """
        한글 자연어를 파싱하여 명령어 리스트로 변환

        Args:
            korean_text: 한글 자연어 명령어

        Returns:
            Studio One 명령어 딕셔너리 리스트
        """
        # 텍스트 정리
        text = korean_text.strip()

        # 명령어 구분자로 분리 (쉼표, 그리고, 그 다음, 다음에 등)
        separators = [",", ", ", ". ", "그리고 ", "그 다음 ", "다음에 ", "하고 ", "한 후 ", "한 다음 "]
        commands_text = [text]

        # 각 구분자로 순차적으로 분리
        for sep in separators:
            new_commands = []
            for cmd in commands_text:
                parts = cmd.split(sep)
                new_commands.extend(parts)
            commands_text = new_commands

        # 각 명령어 정리 및 매칭
        matched_commands = []
        for cmd_text in commands_text:
            cmd_text = cmd_text.strip()
            if not cmd_text:
                continue

            # 불필요한 단어 제거
            cleaned_cmd = cmd_text
            for noise in self.noise_words:
                cleaned_cmd = cleaned_cmd.replace(noise, " ")
            cleaned_cmd = " ".join(cleaned_cmd.split())  # 중복 공백 제거

            # 1. 원본 텍스트로 완전 일치 검색
            if cmd_text in self.command_map:
                matched_commands.append(self.command_map[cmd_text])
                continue

            # 2. 정리된 텍스트로 완전 일치 검색
            if cleaned_cmd in self.command_map:
                matched_commands.append(self.command_map[cleaned_cmd])
                continue

            # 3. 원본 텍스트에서 부분 일치 검색 (긴 명령어부터)
            matched = False
            sorted_commands = sorted(self.command_map.items(), key=lambda x: len(x[0]), reverse=True)

            for korean_cmd, s1_cmd in sorted_commands:
                if korean_cmd in cmd_text:
                    matched_commands.append(s1_cmd)
                    matched = True
                    break

            # 4. 정리된 텍스트에서 부분 일치 검색
            if not matched:
                for korean_cmd, s1_cmd in sorted_commands:
                    if korean_cmd in cleaned_cmd:
                        matched_commands.append(s1_cmd)
                        matched = True
                        break

            if not matched:
                print(f"경고: '{cmd_text}' 명령어를 찾을 수 없습니다.")

        return matched_commands

    def create_macro_xml(self, commands: List[Dict], macro_name: str = "My Macro") -> str:
        """
        Studio One 매크로 XML 생성

        Args:
            commands: 명령어 딕셔너리 리스트
            macro_name: 매크로 이름

        Returns:
            XML 문자열
        """
        # 루트 엘리먼트 생성
        root = ET.Element("Macro")
        root.set("version", "1.0")
        root.set("name", macro_name)

        # 명령어 리스트 추가
        commands_element = ET.SubElement(root, "Commands")

        for idx, cmd in enumerate(commands):
            command_element = ET.SubElement(commands_element, "Command")
            command_element.set("name", cmd["command"])

            # 인자가 있으면 추가
            if cmd.get("args"):
                for arg_name, arg_value in cmd["args"].items():
                    arg_element = ET.SubElement(command_element, "Argument")
                    arg_element.set("name", arg_name)
                    arg_element.set("value", str(arg_value))

        # 예쁘게 포맷팅
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")

        # 불필요한 빈 줄 제거
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

        return pretty_xml

    def translate(self, korean_text: str, macro_name: str = "My Macro") -> str:
        """
        한글 자연어를 Studio One 매크로 XML로 번역

        Args:
            korean_text: 한글 자연어 명령어
            macro_name: 매크로 이름

        Returns:
            Studio One 매크로 XML 문자열
        """
        print(f"\n🔄 번역 시작: {korean_text}")
        print("=" * 60)

        # 명령어 파싱
        commands = self.parse_korean_command(korean_text)

        if not commands:
            print("❌ 인식된 명령어가 없습니다.")
            return ""

        print(f"✅ {len(commands)}개의 명령어 인식:")
        for idx, cmd in enumerate(commands, 1):
            args_str = f" ({cmd['args']})" if cmd['args'] else ""
            print(f"   {idx}. {cmd['command']}{args_str}")

        # XML 생성
        xml_output = self.create_macro_xml(commands, macro_name)

        print("\n📄 생성된 매크로:")
        print(xml_output)
        print("=" * 60)

        return xml_output

    def save_macro(self, xml_content: str, filename: str):
        """
        매크로 XML을 파일로 저장

        Args:
            xml_content: XML 문자열
            filename: 저장할 파일명 (.studioonemacro 확장자)
        """
        if not filename.endswith('.studioonemacro'):
            filename += '.studioonemacro'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        print(f"💾 매크로 저장 완료: {filename}")

    def add_custom_command(self, korean_name: str, s1_command: str, args: Dict = None):
        """
        커스텀 명령어 추가

        Args:
            korean_name: 한글 명령어 이름
            s1_command: Studio One 명령어
            args: 인자 딕셔너리
        """
        self.command_map[korean_name] = {
            "command": s1_command,
            "args": args or {}
        }
        print(f"✅ 커스텀 명령어 추가: '{korean_name}' → {s1_command}")

    def list_commands(self):
        """사용 가능한 모든 한글 명령어 출력"""
        print("\n📋 사용 가능한 한글 명령어:")
        print("=" * 60)

        categories = {
            "트랙": [],
            "재생": [],
            "편집": [],
            "믹싱": [],
            "볼륨": [],
            "줌": [],
            "저장": [],
            "뷰": [],
            "이펙트": [],
            "마커": []
        }

        for korean_cmd, s1_cmd in self.command_map.items():
            categorized = False
            for category in categories:
                if category in korean_cmd:
                    categories[category].append((korean_cmd, s1_cmd["command"]))
                    categorized = True
                    break

            if not categorized:
                for key in ["재생", "정지", "녹음", "처음", "반복"]:
                    if key in korean_cmd:
                        categories["재생"].append((korean_cmd, s1_cmd["command"]))
                        categorized = True
                        break

            if not categorized:
                for key in ["복사", "붙여넣기", "잘라내기", "실행", "삭제", "선택"]:
                    if key in korean_cmd:
                        categories["편집"].append((korean_cmd, s1_cmd["command"]))
                        categorized = True
                        break

            if not categorized:
                for key in ["음소거", "솔로", "무음"]:
                    if key in korean_cmd:
                        categories["믹싱"].append((korean_cmd, s1_cmd["command"]))
                        categorized = True
                        break

        for category, commands in categories.items():
            if commands:
                print(f"\n[{category}]")
                for korean, s1 in commands:
                    print(f"  • {korean:20s} → {s1}")

        print("\n" + "=" * 60)


def main():
    """메인 함수 - CLI 인터페이스"""
    print("=" * 60)
    print("🎵 Studio One 7 한글 매크로 번역기 🎵")
    print("=" * 60)
    print("한글로 명령어를 입력하면 Studio One 매크로로 번역해드립니다!")
    print("명령어: 'list' - 사용 가능한 명령어 보기")
    print("명령어: 'quit' - 종료")
    print("=" * 60)

    translator = StudioOneMacroTranslator()

    # 대화형 모드
    while True:
        try:
            korean_input = input("\n한글 명령어 입력: ").strip()

            if not korean_input:
                continue

            if korean_input.lower() in ['quit', 'exit', '종료', '나가기']:
                print("👋 프로그램을 종료합니다.")
                break

            if korean_input.lower() == 'list':
                translator.list_commands()
                continue

            # 매크로 이름 입력
            macro_name = input("매크로 이름 (엔터: 'My Macro'): ").strip()
            if not macro_name:
                macro_name = "My Macro"

            # 번역 실행
            xml_output = translator.translate(korean_input, macro_name)

            if xml_output:
                # 저장 여부 확인
                save_option = input("\n파일로 저장하시겠습니까? (y/n): ").strip().lower()
                if save_option in ['y', 'yes', 'ㅛ', '예']:
                    filename = input("파일명 입력: ").strip()
                    if filename:
                        translator.save_macro(xml_output, filename)

        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()
