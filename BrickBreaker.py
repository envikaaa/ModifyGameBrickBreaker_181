
import pygame
import random

# 1. INISIALISASI PYGAME
# Mengaktifkan seluruh modul Pygame
pygame.init()

# Mengatur ukuran layar permainan
WIDTH, HEIGHT = 600, 500

# Menentukan warna yang digunakan
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
LIGHT_PINK = (255, 182, 193)
PEACH = (255, 180, 150)
DARK_PINK = (220, 80, 130)
GREEN = (100, 200, 100)

# Mengatur jenis dan ukuran tulisan
font = pygame.font.Font('freesansbold.ttf', 15)

# Membuat jendela permainan
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Peach Block Breaker")

# Mengatur kecepatan frame permainan
clock = pygame.time.Clock()
FPS = 30

# 2. CLASS STRIKER (PEMANTUL)
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        # Membuat area persegi untuk posisi dan tabrakan
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    # Menggambar striker pada layar
    def display(self):
        pygame.draw.rect(screen, self.color, self.strikerRect,
                         border_radius=8)

    # Menggerakkan striker ke kiri atau kanan
    def update(self, xFac):
        self.posx += self.speed * xFac

        # Membatasi gerakan agar tidak keluar layar
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        # Memperbarui posisi striker
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    # Mengembalikan area striker untuk pengecekan tabrakan
    def getRect(self):
        return self.strikerRect

# 3. CLASS BLOCK (BALOK)
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        # Balok putih memiliki 200 health sehingga perlu
        # terkena bola sebanyak dua kali untuk hancur
        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        # Membuat area balok
        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    # Menampilkan balok jika health masih lebih dari 0
    def display(self):
        if self.health > 0:
            pygame.draw.rect(
                screen, self.color, self.blockRect,
                border_radius=5
            )

    # Mengurangi health balok ketika terkena bola
    def hit(self):
        self.health -= self.damage

    # Mengembalikan area balok
    def getRect(self):
        return self.blockRect

    # Mengembalikan sisa health balok
    def getHealth(self):
        return self.health

# 4. CLASS BALL (BOLA BERBENTUK PEACH)
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

        # Membuat area tabrakan berbentuk persegi
        self.ballRect = pygame.Rect(
            self.posx - radius,
            self.posy - radius,
            radius * 2,
            radius * 2
        )

    # Menggambar bola dengan bentuk buah peach
    def display(self):
        # Bagian utama buah peach
        pygame.draw.circle(
            screen, PEACH,
            (int(self.posx), int(self.posy)),
            self.radius
        )

        # Memberikan warna pink pada sisi buah
        pygame.draw.circle(
            screen, DARK_PINK,
            (int(self.posx - 3), int(self.posy)),
            self.radius - 3
        )

        # Menggambar bagian tengah peach
        pygame.draw.circle(
            screen, PEACH,
            (int(self.posx + 3), int(self.posy)),
            self.radius - 3
        )

        # Menggambar daun kecil di bagian atas buah
        pygame.draw.ellipse(
            screen, GREEN,
            (int(self.posx - 3), int(self.posy - self.radius - 4),
             9, 5)
        )

        # Memperbarui area tabrakan bola
        self.ballRect = pygame.Rect(
            int(self.posx - self.radius),
            int(self.posy - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    # Menggerakkan bola
    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # Memantulkan bola jika menyentuh sisi kiri atau kanan
        if self.posx - self.radius <= 0 or self.posx + self.radius >= WIDTH:
            self.xFac *= -1

        # Memantulkan bola jika menyentuh bagian atas layar
        if self.posy - self.radius <= 0:
            self.yFac *= -1

        # Mengembalikan True jika bola jatuh ke bawah layar
        if self.posy - self.radius >= HEIGHT:
            return True

        return False

    # Mengatur ulang posisi bola setelah kehilangan nyawa
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 150
        self.xFac, self.yFac = 1, -1

    # Mengubah arah bola ketika terjadi tabrakan
    def hit(self):
        self.yFac *= -1

    # Mengembalikan area tabrakan bola
    def getRect(self):
        return self.ballRect

# 5. FUNGSI PENGECEKAN TABRAKAN
def collisionChecker(rect, ball):
    # Memeriksa apakah dua objek saling bertabrakan
    return pygame.Rect.colliderect(rect, ball)

