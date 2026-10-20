import random
import hashlib
from PIL import Image, ImageDraw
from pathlib import Path

class AvatarGenerator:
    def __init__(self, size=200):
        self.size = size
        self.cell_size = size // 5
        
    def _get_color_from_hash(self, seed):
        """Генерирует цвет на основе хеша"""
        hash_obj = hashlib.md5(seed.encode())
        hash_hex = hash_obj.hexdigest()
        return tuple(int(hash_hex[i:i+2], 16) for i in (0, 2, 4))
    
    def _get_pattern(self, seed):
        """Генерирует уникальный паттерн на основе хеша"""
        random.seed(seed)
        pattern = []
        for _ in range(12):
            pattern.append(random.choice([True, False]))
        return pattern
    
    def generate(self, username, output_path=None):
        """
        Генерирует аватарку на основе username
        
        Args:
            username (str): Имя пользователя для генерации
            output_path (str): Путь для сохранения аватарки
        
        Returns:
            Image: PIL Image объект
        """
    
        bg_color = self._get_color_from_hash(username)
        fg_color = tuple(255 - c for c in bg_color)
        
        # Создаём изображение
        img = Image.new('RGB', (self.size, self.size), bg_color)
        draw = ImageDraw.Draw(img)
        
        pattern = self._get_pattern(username)
        
        
        pattern_idx = 0
        for row in range(5):
            for col in range(5):
                if pattern[pattern_idx % len(pattern)]:
                    x0 = col * self.cell_size
                    y0 = row * self.cell_size
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    draw.rectangle([x0, y0, x1, y1], fill=fg_color)
                pattern_idx += 1
        
        # Сохраняем если указан путь
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path)
            print(f"✓ Аватарка сохранена: {output_path}")
        
        return img
    
    def generate_batch(self, usernames, output_dir="avatars"):
        """Генерирует аватарки для нескольких пользователей"""
        for username in usernames:
            output_path = f"{output_dir}/{username}.png"
            self.generate(username, output_path)



if __name__ == "__main__":
    generator = AvatarGenerator(size=200)

    
    generator.generate("Имя которое хотите1", "avatars/test1.png")
    generator.generate("2", "avatars/test2.png")
    generator.generate("3", "avatars/test3.png")
    
    
    usernames = ["user1", "user2", "user3", "user4", "user5"]
    generator.generate_batch(usernames)
    
    print("✓ Все аватарки сгенерированы!")
