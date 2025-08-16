import pygame
import json
import sys
from pathlib import Path

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_PATH = Path("font/NanumGothic.ttf")

DEFAULT_SCENES = {
    "start": {
        "background": None,
        "character": None,
        "text": "환영합니다! assets 폴더에 이미지를 넣어보세요.",
        "choices": []
    }
}

class Scene:
    def __init__(self, data):
        self.background = data.get("background")
        self.character = data.get("character")
        self.text = data.get("text", "")
        self.choices = data.get("choices", [])

def ensure_environment():
    assets_dir = Path("assets")
    font_dir = Path("font")
    assets_dir.mkdir(exist_ok=True)
    font_dir.mkdir(exist_ok=True)

    scenes_path = Path("scenes.json")
    if not scenes_path.exists():
        scenes_path.write_text(json.dumps(DEFAULT_SCENES, ensure_ascii=False, indent=2), encoding="utf-8")


def load_scenes(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {name: Scene(scene) for name, scene in raw.items()}


def draw_scene(screen, scene, font):
    screen.fill((0, 0, 0))

    if scene.background:
        bg = pygame.image.load(Path("assets") / scene.background)
        screen.blit(bg, (0, 0))
    if scene.character:
        char = pygame.image.load(Path("assets") / scene.character)
        screen.blit(char, (200, 100))

    text_surf = font.render(scene.text, True, (255, 255, 255))
    screen.blit(text_surf, (50, 450))

    for i, choice in enumerate(scene.choices):
        choice_surf = font.render(f"{i+1}. {choice['label']}", True, (255, 255, 0))
        screen.blit(choice_surf, (50, 500 + i * 30))


def main():
    ensure_environment()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Visual Novel Tool")

    if FONT_PATH.exists():
        font = pygame.font.Font(str(FONT_PATH), 24)
    else:
        font = pygame.font.SysFont(None, 24)

    scenes = load_scenes("scenes.json")
    current_scene_name = "start"

    clock = pygame.time.Clock()
    running = True

    while running:
        scene = scenes[current_scene_name]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and scene.choices:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(scene.choices):
                        current_scene_name = scene.choices[index]["next"]

        draw_scene(screen, scene, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
