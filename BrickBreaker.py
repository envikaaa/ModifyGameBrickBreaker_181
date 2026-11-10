
import pygame
import random

# ==========================================
# 1. INISIALISASI PYGAME
# ==========================================
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


# ==========================================
# 2. CLASS STRIKER (PEMANTUL)
# ==========================================
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


# ==========================================
# 3. CLASS BLOCK (BALOK)
# ==========================================
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


# ==========================================
# 4. CLASS BALL (BOLA BERBENTUK PEACH)
# ==========================================
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


# ==========================================
# 5. FUNGSI PENGECEKAN TABRAKAN
# ==========================================
def collisionChecker(rect, ball):
    # Memeriksa apakah dua objek saling bertabrakan
    return pygame.Rect.colliderect(rect, ball)


# ==========================================
# 6. FUNGSI MEMBUAT BALOK
# ==========================================
def populateBlocks(blockWidth, blockHeight,
                   horizontalGap, verticalGap):

    listOfBlocks = []

    # Membuat balok dengan jarak horizontal dan vertikal
    for i in range(0, WIDTH, blockWidth + horizontalGap):
        for j in range(0, HEIGHT // 2, blockHeight + verticalGap):

            # Memilih warna balok secara acak antara pink dan putih
            listOfBlocks.append(
                Block(
                    i, j, blockWidth, blockHeight,
                    random.choice([PINK, WHITE])
                )
            )

    return listOfBlocks


# ==========================================
# 7. FUNGSI GAME OVER
# ==========================================
def gameOver():
    gameOver = True

    while gameOver:
        # Menampilkan tulisan Game Over
        screen.fill(BLACK)

        text = font.render("GAME OVER - Press SPACE to Restart",
                           True, PINK)
        textRect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, textRect)

        pygame.display.update()

        # Memeriksa input pemain
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True


# ==========================================
# 8. GAME MANAGER (PROGRAM UTAMA)
# ==========================================
def main():
    running = True
    lives = 3
    score = 0

    # Membuat striker atau pemantul
    striker = Striker(250, HEIGHT - 50, 100, 20, 10, LIGHT_PINK)
    strikerXFac = 0

    # Membuat bola berbentuk peach
    ball = Ball(WIDTH // 2, HEIGHT - 150, 10, 5, PEACH)

    # Menentukan ukuran dan jarak antarbalok
    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    # Membuat kumpulan balok pertama
    listOfBlocks = populateBlocks(
        blockWidth, blockHeight,
        horizontalGap, verticalGap
    )

    # ======================================
    # 9. GAME LOOP
    # ======================================
    while running:
        # Membersihkan layar setiap frame
        screen.fill(BLACK)

        # Menampilkan skor dan jumlah nyawa
        scoreText = font.render("Score : " + str(score), True, WHITE)
        livesText = font.render("Lives : " + str(lives), True, WHITE)

        screen.blit(scoreText, (10, HEIGHT - 25))
        screen.blit(livesText, (120, HEIGHT - 25))

        # Membuat balok baru jika semua balok sudah hancur
        if not listOfBlocks:
            listOfBlocks = populateBlocks(
                blockWidth, blockHeight,
                horizontalGap, verticalGap
            )

        # Memeriksa apakah nyawa pemain sudah habis
        if lives <= 0:
            running = gameOver()

            # Mengatur ulang permainan
            if running:
                lives = 3
                score = 0
                ball.reset()
                striker.posx = 250
                striker.update(0)

                listOfBlocks = populateBlocks(
                    blockWidth, blockHeight,
                    horizontalGap, verticalGap
                )

        # ==================================
        # 10. EVENT HANDLING
        # ==================================
        for event in pygame.event.get():

            # Keluar dari permainan
            if event.type == pygame.QUIT:
                running = False

            # Menggerakkan striker ke kiri atau kanan
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1

                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            # Menghentikan striker ketika tombol dilepas
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    strikerXFac = 0

        # ==================================
        # 11. COLLISION CHECK (TABRAKAN)
        # ==================================

        # Memeriksa tabrakan antara striker dan bola
        if collisionChecker(striker.getRect(), ball.getRect()):
            ball.hit()

        # Memeriksa tabrakan antara bola dan balok
        for block in listOfBlocks[:]:
            if collisionChecker(block.getRect(), ball.getRect()):
                ball.hit()
                block.hit()

                # Menghapus balok jika health sudah habis
                if block.getHealth() <= 0:
                    listOfBlocks.remove(block)
                    score += 5

        # ==================================
        # 12. UPDATE POSISI OBJEK
        # ==================================

        # Memperbarui posisi striker
        striker.update(strikerXFac)

        # Memperbarui posisi bola
        lifeLost = ball.update()

        # Mengurangi nyawa jika bola jatuh
        if lifeLost:
            lives -= 1
            ball.reset()

        # ==================================
        # 13. DISPLAY (MENAMPILKAN OBJEK)
        # ==================================

        # Menampilkan striker dan bola peach
        striker.display()
        ball.display()

        # Menampilkan semua balok
        for block in listOfBlocks:
            block.display()

        # Memperbarui tampilan layar
        pygame.display.update()

        # Mengatur FPS permainan
        clock.tick(FPS)


# ==========================================
# 14. MENJALANKAN PROGRAM
# ==========================================
if __name__ == "__main__":
    main()

    # Menutup seluruh modul Pygame
    pygame.quit()