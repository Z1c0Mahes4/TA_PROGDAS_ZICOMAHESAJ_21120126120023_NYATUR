import pygame
import chess
import sys

# ==========================================
# 1. INISIALISASI GAME
# ==========================================
pygame.init()

WIDTH = 900
HEIGHT = 680
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NYATUR - 2 PLAYER")
clock = pygame.time.Clock()

# ==========================================
# 2. WARNA
# ==========================================
CREAM = (240, 217, 181)
BROWN = (181, 136, 99)
DARK = (35, 39, 47)
SIDEBAR = (29, 33, 41)
GREEN = (100, 180, 100)
YELLOW = (255, 220, 80)
RED = (220, 80, 80)
TEXT_WHITE = (245, 245, 245)
GRAY = (150, 155, 165)

# ==========================================
# 3. FONT DAN SIMBOL BIDAK
# ==========================================
font_piece = pygame.font.SysFont("segoeuisymbol", 65)
font_title = pygame.font.SysFont("arial", 32, bold=True)
font_normal = pygame.font.SysFont("arial", 18)
font_small = pygame.font.SysFont("arial", 14)

PIECES = {
    "K": "♔", "Q": "♕", "R": "♖",
    "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜",
    "b": "♝", "n": "♞", "p": "♟"
}

# ==========================================
# 4. DATA PERMAINAN
# ==========================================
board = chess.Board()
selected_square = None
legal_targets = []
move_history = []
game_message = "Giliran Pemain 1 (Putih)"
game_started = False


# ==========================================
# 5. FUNGSI TOMBOL
# ==========================================
def draw_button(x, y, width, height, text, color):
    pygame.draw.rect(
        screen, color, (x, y, width, height),
        border_radius=10
    )
    label = font_normal.render(text, True, TEXT_WHITE)
    label_rect = label.get_rect(
        center=(x + width // 2, y + height // 2)
    )
    screen.blit(label, label_rect)


# ==========================================
# 6. MEMULAI / MENGULANG PERMAINAN
# ==========================================
def start_game():
    global board, selected_square, legal_targets
    global move_history, game_message, game_started

    board = chess.Board()
    selected_square = None
    legal_targets = []
    move_history = []
    game_message = "Giliran Pemain 1 (Putih)"
    game_started = True


# ==========================================
# 7. MEMERIKSA STATUS PERMAINAN
# ==========================================
def update_game_status():
    global game_message

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            game_message = "SKAKMAT! Pemain 2 (Hitam) menang!"
        else:
            game_message = "SKAKMAT! Pemain 1 (Putih) menang!"
    elif board.is_stalemate():
        game_message = "REMIS - Stalemate"
    elif board.is_insufficient_material():
        game_message = "REMIS - Bidak tidak cukup"
    elif board.is_fivefold_repetition():
        game_message = "REMIS - Posisi berulang"
    elif board.is_seventyfive_moves():
        game_message = "REMIS - Aturan 75 langkah"
    elif board.is_check():
        if board.turn == chess.WHITE:
            game_message = "SKAK! Giliran Pemain 1 (Putih)"
        else:
            game_message = "SKAK! Giliran Pemain 2 (Hitam)"
    else:
        if board.turn == chess.WHITE:
            game_message = "Giliran Pemain 1 (Putih)"
        else:
            game_message = "Giliran Pemain 2 (Hitam)"


# ==========================================
# 8. MENGGAMBAR PAPAN CATUR
# ==========================================
def draw_board():
    for row in range(8):
        for col in range(8):
            color = CREAM if (row + col) % 2 == 0 else BROWN
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            pygame.draw.rect(
                screen, color,
                (x, y, SQUARE_SIZE, SQUARE_SIZE)
            )

    # Menandai bidak yang sedang dipilih
    if selected_square is not None:
        file_pos = chess.square_file(selected_square)
        rank_pos = chess.square_rank(selected_square)
        row = 7 - rank_pos
        col = file_pos
        pygame.draw.rect(
            screen, YELLOW,
            (col * SQUARE_SIZE, row * SQUARE_SIZE,
             SQUARE_SIZE, SQUARE_SIZE),
            5
        )

    # Menampilkan tujuan langkah yang legal
    for square in legal_targets:
        file_pos = chess.square_file(square)
        rank_pos = chess.square_rank(square)
        row = 7 - rank_pos
        col = file_pos
        center = (
            col * SQUARE_SIZE + SQUARE_SIZE // 2,
            row * SQUARE_SIZE + SQUARE_SIZE // 2
        )
        pygame.draw.circle(screen, GREEN, center, 10)

    # Menggambar seluruh bidak
    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is None:
            continue

        symbol = PIECES[piece.symbol()]
        text_color = (255, 255, 255) if piece.color else (20, 20, 20)

        file_pos = chess.square_file(square)
        rank_pos = chess.square_rank(square)
        col = file_pos
        row = 7 - rank_pos

        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

        piece_text = font_piece.render(symbol, True, text_color)
        piece_rect = piece_text.get_rect(
            center=(center_x, center_y)
        )
        screen.blit(piece_text, piece_rect)

    # Garis tepi papan
    pygame.draw.rect(
        screen, DARK, (0, 0, BOARD_SIZE, BOARD_SIZE), 3
    )


# ==========================================
# 9. PANEL INFORMASI DI SAMPING PAPAN
# ==========================================
def draw_sidebar():
    pygame.draw.rect(
        screen, SIDEBAR,
        (BOARD_SIZE, 0, WIDTH - BOARD_SIZE, HEIGHT)
    )

    title = font_title.render("NYATUR", True, TEXT_WHITE)
    screen.blit(title, (680, 25))

    pygame.draw.line(
        screen, GRAY, (680, 75), (880, 75), 1
    )

    player1 = font_normal.render(
        "Pemain 1 : Putih", True, TEXT_WHITE
    )
    player2 = font_normal.render(
        "Pemain 2 : Hitam", True, TEXT_WHITE
    )
    screen.blit(player1, (680, 125))
    screen.blit(player2, (680, 153))

    status_title = font_normal.render(
        "STATUS PERMAINAN", True, YELLOW
    )
    screen.blit(status_title, (680, 200))

    # Status dapat terdiri dari teks panjang, jadi dibungkus
    words = game_message.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font_small.size(test_line)[0] <= 200:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        status_text = font_small.render(
            line, True, TEXT_WHITE
        )
        screen.blit(status_text, (680, 230 + i * 20))

    pygame.draw.line(
        screen, GRAY, (680, 285), (880, 285), 1
    )

    history_title = font_normal.render(
        "RIWAYAT LANGKAH", True, YELLOW
    )
    screen.blit(history_title, (680, 305))

    # Menampilkan maksimal 12 langkah terakhir
    recent_moves = move_history[-12:]
    for i, move_text in enumerate(recent_moves):
        history_text = font_small.render(
            move_text, True, TEXT_WHITE
        )
        screen.blit(
            history_text,
            (680, 335 + i * 19)
        )

    draw_button(680, 570, 200, 35, "RESTART", GREEN)
    draw_button(680, 615, 200, 35, "MENU", RED)


# ==========================================
# 10. MEMPROSES KLIK PADA PAPAN
# ==========================================
def handle_board_click(position):
    global selected_square, legal_targets, game_message

    if board.is_game_over():
        return

    x, y = position

    if x >= BOARD_SIZE or y >= BOARD_SIZE:
        return

    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    # Mengubah koordinat layar menjadi kotak catur
    file_pos = col
    rank_pos = 7 - row
    square = chess.square(file_pos, rank_pos)

    piece = board.piece_at(square)

    # Jika belum ada bidak yang dipilih
    if selected_square is None:
        if piece is not None and piece.color == board.turn:
            selected_square = square
            legal_targets = [
                move.to_square
                for move in board.legal_moves
                if move.from_square == square
            ]
        return

    # Jika pemain memilih bidak lain miliknya
    if piece is not None and piece.color == board.turn:
        selected_square = square
        legal_targets = [
            move.to_square
            for move in board.legal_moves
            if move.from_square == square
        ]
        return

    # Membuat langkah dari kotak asal ke kotak tujuan
    move = chess.Move(selected_square, square)

    # Promosi pion otomatis menjadi ratu
    selected_piece = board.piece_at(selected_square)
    if (
        selected_piece is not None
        and selected_piece.piece_type == chess.PAWN
        and chess.square_rank(square) in [0, 7]
    ):
        move.promotion = chess.QUEEN

    # Memastikan langkah sesuai aturan catur
    if move in board.legal_moves:
        if board.turn == chess.WHITE:
            player_name = "P1"
        else:
            player_name = "P2"

        san_move = board.san(move)
        board.push(move)
        move_history.append(
            f"{len(move_history) + 1}. {player_name}: {san_move}"
        )

        selected_square = None
        legal_targets = []
        update_game_status()
    else:
        selected_square = None
        legal_targets = []



# ==========================================
# 12. MENU AWAL
# ==========================================
def draw_menu():
    screen.fill(DARK)

    title = font_title.render(
        "NYATUR", True, TEXT_WHITE
    )
    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 150)
    )

    subtitle = font_normal.render(
        "GAME CATUR - 2 PLAYER", True, GREEN
    )
    screen.blit(
        subtitle,
        (WIDTH // 2 - subtitle.get_width() // 2, 205)
    )

    info = font_normal.render(
        "Mainkan catur bersama teman pada satu komputer",
        True, TEXT_WHITE
    )
    screen.blit(
        info,
        (WIDTH // 2 - info.get_width() // 2, 270)
    )

    draw_button(300, 350, 300, 60, "MULAI BERMAIN", GREEN)

    hint = font_small.render(
        "Pemain 1 menggunakan putih, Pemain 2 menggunakan hitam",
        True, GRAY
    )
    screen.blit(
        hint,
        (WIDTH // 2 - hint.get_width() // 2, 440)
    )


# ==========================================
# 13. PROGRAM UTAMA
# ==========================================
def main():
    global game_started, selected_square, legal_targets

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if not game_started:
                    # Tombol mulai pada menu
                    if 300 <= x <= 600 and 350 <= y <= 410:
                        start_game()

                else:
                    if x < BOARD_SIZE and y < BOARD_SIZE:
                        handle_board_click(event.pos)

                    elif 570 <= y <= 605 and 680 <= x <= 880:
                        start_game()

                    elif 615 <= y <= 650 and 680 <= x <= 880:
                        game_started = False
                        selected_square = None
                        legal_targets = []

        # Menggambar tampilan
        if not game_started:
            draw_menu()
        else:
            screen.fill(DARK)
            draw_board()
            draw_sidebar()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# Program dimulai dari fungsi main()
if __name__ == "__main__":
    main()
