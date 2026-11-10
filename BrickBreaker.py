
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

