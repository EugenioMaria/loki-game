import pygame
import random

pygame.init()

# Configurações da tela
game_display = (1600, 900)
screen = pygame.display.set_mode(game_display)
pygame.display.set_caption('Loki')

# Inicialização do relógio para controle de frames por segundo
clock = pygame.time.Clock()

# Carregando e ajustando as imagens do céu e do chão
sky_surface = pygame.transform.scale(pygame.image.load('graphics/Sky.png').convert(), game_display)
ground_surface = pygame.transform.scale(pygame.image.load('graphics/ground.png').convert(), (game_display[0], 200))

# Carregando a imagem do personagem e definindo sua posição inicial
player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(600, 750))

# Carregando a imagem do jogador atacando
espada_surf = pygame.image.load('graphics/Player/espada.png').convert_alpha()
espada_rect = espada_surf.get_rect(midleft=player_rect.topright)

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect_list = []  # Lista para armazenar retângulos das Snails

# Variáveis de rolagem para o céu e o chão
background_scroll = 0
ground_scroll = 0
ground_width = ground_surface.get_width()
sky_width = sky_surface.get_width()

# Variáveis do jogo
game_active = True
player_gravity = 0
player_speed = 5
jumping = False
dash_speed = 200  # Velocidade do dash
attack_cooldown = 0
attack_duration = 20  # Número de frames que o ataque é exibido
cooldown_duration = 0  # Tempo de cooldown entre os ataques (60 frames por segundo * 5 segundos)
is_attacking = False  # Flag para indicar se o jogador está atacando

# Configuração da fonte para exibir o tempo de jogo
font = pygame.font.Font(None, 36)

# Variáveis do score (tempo em segundos)
score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Verifica se o botão direito do mouse foi pressionado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # Aplica o dash apenas se a tecla A ou D estiver pressionada
            if pygame.key.get_pressed()[pygame.K_a]:
                if player_rect.left > 400:
                    player_rect.left -= dash_speed
                    espada_rect.left -= dash_speed
            if pygame.key.get_pressed()[pygame.K_d]:
                if player_rect.right < game_display[0] - 400:
                    player_rect.left += dash_speed
                    espada_rect.left += dash_speed
        # Verifica se o botão esquerdo do mouse foi pressionado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and attack_cooldown == 0:
            if cooldown_duration == 0:
                attack_cooldown = attack_duration
                is_attacking = True

    keys = pygame.key.get_pressed()
    if game_active:
        if keys[pygame.K_SPACE] and player_rect.bottom == 750:
            player_gravity = -20
            jumping = True

        movement_speed = player_speed if not jumping else player_speed
        # Movimentação para a esquerda com restrição para não sair da tela
        if keys[pygame.K_a]:
            if player_rect.left > 400:
                player_rect.left -= movement_speed
                espada_rect.left -= movement_speed
            background_scroll += movement_speed
            ground_scroll += movement_speed
        # Movimentação para a direita com restrição para não sair da tela
        if keys[pygame.K_d]:
            if player_rect.right < game_display[0] - 400:
                player_rect.left += movement_speed
                espada_rect.left += movement_speed
            background_scroll -= movement_speed
            ground_scroll -= movement_speed

        # Atualizando a posição vertical do personagem
        player_gravity += 1
        player_rect.y += player_gravity
        espada_rect.y += player_gravity

        # Verificando se o personagem está no chão
        if player_rect.bottom >= 750:
            player_rect.bottom = 750
            espada_rect.bottom = 750
            player_gravity = 0
            jumping = False

        # Desenhando o cenário movendo-se com base nas variáveis de rolagem
        screen.blit(sky_surface, (background_scroll % sky_width - sky_width, 0))
        screen.blit(sky_surface, ((background_scroll % sky_width), 0))
        screen.blit(ground_surface, (ground_scroll % ground_width - ground_width, 750))
        screen.blit(ground_surface, ((ground_scroll % ground_width), 750))
        screen.blit(player_surface, player_rect)

        # Atualiza o cooldown do ataque
        if attack_cooldown > 0:
            attack_cooldown -= 1
            if is_attacking:
                screen.blit(espada_surf, espada_rect)

        if cooldown_duration == 0 and attack_cooldown > 0:
            cooldown_duration = 50

        if attack_cooldown == 0:
            is_attacking = False

        # Exibe o tempo de recarga na tela
        if cooldown_duration > 0:
            cooldown_duration -= 1
            cooldown_text = font.render(f"Tempo de Recarga: {int(cooldown_duration/60)+1}", True, 'black')
            screen.blit(cooldown_text, (10, 10))

        # Gera Snails aleatoriamente e as move
        if random.randint(0, 100) < 1:  # Probabilidade de 1% de gerar uma Snail
            new_snail_rect = snail_surf.get_rect(midbottom=(1600, 750))
            snail_rect_list.append(new_snail_rect)

        for snail_rect in snail_rect_list:
            screen.blit(snail_surf, snail_rect)
            snail_rect.x -= 10
            if snail_rect.right <= 0:
                snail_rect_list.remove(snail_rect)

            # Verifica a colisão entre a espada e a Snail durante a animação de ataque
            if is_attacking and espada_rect.colliderect(snail_rect):
                is_attacking = False  # Desativa a animação de ataque
                snail_rect.x = 1600  # Reposiciona a Snail fora da tela

        score += 1  # Incrementa o score
        # Exibe o score (tempo em segundos) na tela
        score_text = font.render(f"Tempo: {int(score/60)+1} s", True, 'black')
        screen.blit(score_text, (game_display[0] // 2 - score_text.get_width() // 2, 10))

        if any(snail_rect.colliderect(player_rect) for snail_rect in snail_rect_list):
            game_active = False

        # Atualizando a posição do chão e do cenário para a repetição
        ground_scroll %= ground_width
        background_scroll %= sky_width

    else:
        if keys[pygame.K_SPACE] or keys[pygame.K_a] or keys[pygame.K_d]:
            game_active = True
            snail_rect_list.clear()  # Limpa a lista de Snails
            player_rect.midbottom = (600, 750)  # Reposiciona o jogador
            espada_rect.midleft = player_rect.topright  # Reposiciona a espada
            score = 0  # Reinicia o score

    # Atualizando a tela e controlando os frames por segundo
    pygame.display.update()
    clock.tick(60)
