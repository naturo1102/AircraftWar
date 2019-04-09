# -*- coding:utf-8 -*-
from random import choice

import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
import time
from pygame.locals import*

pygame.init()
pygame.mixer.init()

bg_size = width,height = 512,768
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")
bg_image = pygame.image.load("image/background.png").convert()

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
YELLOW = (227,207,87)

surface_list = []
# 界面初始化
surface_list = [
    'image/surface1.jpg',
    'image/surface2_2.jpg',
    'image/surface3.jpg'
]

#载入游戏音乐

# pygame.mixer.music.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)
use_bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
use_bomb_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bullet_sound.set_volume(0.2)


def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def add_mid_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)
def add_big_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def draw_text(surf, text, size, x, y):
        # 定义文本参数
        font = pygame.font.Font("font/font.ttf", size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

def main():
    global screen
    # 加载游戏初始界面背景音乐
    menu_song = pygame.mixer.music.load("sound/DOMA.ogg")
    # 循环播放
    pygame.mixer.music.play(-1)
    # 加载初始化界面
    for i in range(3):
        surimage = surface_list[i]
        title = pygame.image.load(surimage).convert()
        title = pygame.transform.scale(title, (width, height), screen)
        screen.blit(title, (0, 0))
        pygame.display.update()
        time.sleep(2)

    # 加载游戏初始界面背景图片
    # title = pygame.image.load(path.join(img_dir,"main.png")).convert()
    title = pygame.image.load("image/img_bg_logo.jpg").convert()
    title = pygame.transform.scale(title, (width, height), screen)
    screen.blit(title, (0, 0))
    pygame.display.update()

    # 检测玩家操作事件
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, width / 2, height / 2)
            draw_text(screen, "[A] ←  [S] ↓  [D] →  [W] ↑", 30, width / 2, 2 * height / 3)
            draw_text(screen, "[Space] fire", 30, width / 2, 3 * height / 4)
            pygame.display.update()

    # 加载准备开始界面背景颜色和文本
    screen.fill(BLACK)
    draw_text(screen, "READY GO!", 40, width / 2, height / 3)
    pygame.display.update()

    # pygame.mixer.music.play(-1)
    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    Bullet1_Num = 4
    for i in range(Bullet1_Num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    Bullet2_Num = 12
    for i in range(Bullet2_Num//3):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(bullet.Bullet2(me.rect.midtop))
        bullet2.append(bullet.Bullet2((me.rect.centerx+33,me.rect.centery)))

    #生成敌方飞机
    enemies = pygame.sprite.Group()
    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)
    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 15)

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #统计得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf",36)

    #是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("image/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("image/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("image/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("image/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left,paused_rect.top = width - paused_rect.width - 10,10
    paused_image = pause_nor_image

    #全屏炸弹
    bomb_image = pygame.image.load("image/daodan.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf",40)
    bomb_num = 3

    clock = pygame.time.Clock()
    #用于切换图片
    switch_image = True
    running = True

    #每30s发放一个补给
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    Supply_Time = USEREVENT
    pygame.time.set_timer(Supply_Time,30*1000)

    #超级子弹定时器
    Bullet_Time = USEREVENT + 1
    #标志是否使用超级子弹
    is_super_bullet = False

    #解除我方无敌
    Invincible_Time = USEREVENT +2


    #我方HP
    life_image = pygame.image.load("image/life_plane.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    #用于延迟火焰效果
    delay = 100

    #限制重复打开存档文件
    record = False

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("image/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("image/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    while running:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/DOMA.ogg")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(Supply_Time,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(Supply_Time, 30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                     if paused:
                         paused_image = resume_nor_image
                     else:
                         paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        use_bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == Supply_Time:
                if choice([True , False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == Bullet_Time:
                is_super_bullet = False
                pygame.time.set_timer(Bullet_Time,0)
            elif event.type == Invincible_Time:
                me.invincible =False
                pygame.time.set_timer(Invincible_Time,0)



        screen.blit(bg_image, (0, 0))

        if life_num and not paused:
                    #检测用户的键盘操作
                    key_press = pygame.key.get_pressed()
                    if key_press[K_w] or key_press[K_UP]:
                       me.Up()
                    if key_press[K_s] or key_press[K_DOWN]:
                        me.Down()
                    if key_press[K_a] or key_press[K_LEFT]:
                        me.Left()
                    if key_press[K_d] or key_press[K_RIGHT]:
                        me.Right()

                    #绘制全屏炸弹补给检测是否获得
                    if bomb_supply.active:
                        bomb_supply.move()
                        screen.blit(bomb_supply.image,bomb_supply.rect)
                        if pygame.sprite.collide_mask(bomb_supply,me):
                            get_bomb_sound.play()
                            if bomb_num < 3:
                                bomb_num += 1
                            bomb_supply.active = False

                    # 绘制超级子弹补给检测是否获得
                    if bullet_supply.active:
                        bullet_supply.move()
                        screen.blit(bullet_supply.image, bullet_supply.rect)
                        if pygame.sprite.collide_mask(bullet_supply, me):
                           get_bullet_sound.play()
                           is_super_bullet = True
                           pygame.time.set_timer(Bullet_Time,18*1000)
                           bullet_supply.active = False




                    #检测我方飞机是否被撞
                    enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
                    if enemies_down and not me.invincible:
                        me.active = False
                        for e in enemies_down:
                            e.active = False


                    #绘制我方飞机
                    if me.active:
                        # 绘制血槽
                        pygame.draw.line(screen, BLACK, (me.rect.left, me.rect.bottom - 5),
                                         (me.rect.right, me.rect.bottom - 5), 2)
                        # 当能量值小于30%显示红色，小于100%显示黄色，否则显示绿色
                        # My_Energy = myplane.MyPlane.Energy
                        # Score = score
                        # while My_Energy:
                        #     My_Energy += Score
                        #     if  My_Energy < 20000:
                        #             Energy_color = RED
                        #     elif My_Energy >= 20000 and My_Energy < 50000:
                        #             Energy_color = YELLOW
                        #     else:
                        #         Energy_color = GREEN
                        #         pygame.draw.line(screen, Energy_color, (me.rect.left, me.rect.bottom - 5),
                        #                          (me.rect.left + me.rect.width, me.rect.bottom - 5), 2)
                        if switch_image:
                            screen.blit(me.image1, me.rect)
                        else:
                            screen.blit(me.image2,me.rect)
                    else:
                        # 毁灭
                        if not (delay % 3):
                            if me_destroy_index == 0:
                                me_down_sound.play()
                            screen.blit(me.destory_images[me_destroy_index], me.rect)
                            me_destroy_index = (me_destroy_index + 1) % 3
                            if me_destroy_index == 0:
                                life_num -= 1
                                me.reset()
                                pygame.time.set_timer(Invincible_Time,3*1000)

                    #绘制剩余生命数量
                    if life_num:
                        for i in range(life_num):
                            screen.blit(life_image,(width - 80-(i*1)*life_rect.width,height - 10 - life_rect.height))

                    #发射子弹
                    if not (delay % 10):
                        if is_super_bullet:
                            bullets = bullet2
                            bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                            bullets[bullet2_index+1].reset(me.rect.midtop)
                            bullets[bullet2_index+2].reset((me.rect.centerx+33,me.rect.centery))
                            bullet2_index = (bullet2_index + 3) % Bullet2_Num
                        else:
                            bullets = bullet1
                            bullets[bullet1_index].reset(me.rect.midtop)
                            bullet1_index = (bullet1_index + 1) % Bullet1_Num
                    #检测子弹是否击中
                    for b in bullets:
                        if b.active:
                            b.move()
                            screen.blit(b.image,b.rect)
                            enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                            if enemy_hit:
                                b.active = False
                                for e in enemy_hit:
                                    if e in mid_enemies or e in big_enemies:
                                        e.HP -= 1
                                        if e.HP == 0:
                                            e.active = False
                                    else:
                                        e.active = False

                    #绘制大型飞机
                    for each in big_enemies:
                        if each.active:
                            each.move()
                            screen.blit(each.image,each.rect)
                            #绘制血槽
                            pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                            #当生命值大于20%显示 绿色，否则显示红色
                            HP_remain = each.HP / enemy.BigEnemy.HP
                            if HP_remain > 0.2:
                                HP_color = GREEN
                            else:
                                HP_color = RED
                            pygame.draw.line(screen,HP_color,(each.rect.left,each.rect.top - 5),\
                                             (each.rect.left + each.rect.width * HP_remain,each.rect.top - 5),2)

                            if each.rect.bottom == -50:
                                enemy3_fly_sound.play(-1)
                        else:
                            #毁灭
                            if not (delay % 3):
                                if e3_destroy_index == 0:
                                    enemy3_down_sound.play()

                                screen.blit(each.destroy_enemies[e3_destroy_index],each.rect)
                                e3_destroy_index = (e3_destroy_index + 1)%4
                                if e3_destroy_index == 0:
                                    enemy3_fly_sound.stop()
                                    score += 12000
                                    each.reset()

                    #绘制中型飞机
                    for each in mid_enemies:
                        if each.active:
                            each.move()
                            screen.blit(each.image,each.rect)
                            # 绘制血槽
                            pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                             (each.rect.right, each.rect.top - 5), 2)
                            # 当生命值大于20%显示 绿色，否则显示红色
                            HP_remain = each.HP / enemy.MidEnemy.HP
                            if HP_remain > 0.2:
                                HP_color = GREEN
                            else:
                                HP_color = RED
                            pygame.draw.line(screen, HP_color, (each.rect.left, each.rect.top - 5), \
                                             (each.rect.left + each.rect.width * HP_remain,each.rect.top - 5), 2)
                        else:
                            #毁灭

                            if not (delay % 3):
                                if e2_destroy_index == 0:
                                    enemy2_down_sound.play()
                                screen.blit(each.destroy_enemies[e2_destroy_index],each.rect)
                                e2_destroy_index = (e2_destroy_index + 1)%3
                                if e2_destroy_index == 0:
                                    score += 6000
                                    each.reset()
                    #绘制小型飞机
                    for each in small_enemies:
                        if each.active:
                            each.move()
                            screen.blit(each.image,each.rect)
                        else:
                            #毁灭
                            if not (delay % 3):
                                if e1_destroy_index == 0:
                                    enemy1_down_sound.play()
                                screen.blit(each.destroy_enemies[e1_destroy_index],each.rect)
                                e1_destroy_index = (e1_destroy_index + 1)%2
                                if e1_destroy_index == 0:
                                    score += 1000
                                    each.reset()
                    # 绘制得分
                    score_text = score_font.render("Score : %s" % str(score), True, WHITE)
                    screen.blit(score_text, (10, 5))

        #绘制游戏结束画面
        elif life_num == 0:
                #首先关闭背景音乐
                pygame.mixer.music.stop()
                #停止音效
                pygame.mixer.stop()
                #停止补给发放
                pygame.time.set_timer(Supply_Time,0)

                if not record:
                    record = True
                    #读取历史最高得分
                    with open("cundang.txt","r") as f:
                        cundang_score = int(f.read())

                    #判断玩家的分是否高于最高分
                    if score > cundang_score:
                        with open("cundang.txt","w")as f:
                            f.write(str(score))


                #绘制结束画面
                record_score_text = score_font.render("Best : %d" % cundang_score, True, (255, 255, 255))
                screen.blit(record_score_text, (50, 50))

                gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
                gameover_text1_rect = gameover_text1.get_rect()
                gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
                screen.blit(gameover_text1, gameover_text1_rect)

                gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
                gameover_text2_rect = gameover_text2.get_rect()
                gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
                screen.blit(gameover_text2, gameover_text2_rect)

                again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text2_rect.bottom + 50
                screen.blit(again_image, again_rect)

                gameover_rect.left, gameover_rect.top = (width - again_rect.width) // 2, again_rect.bottom + 10
                screen.blit(gameover_image, gameover_rect)

                # 检测用户的鼠标操作
                # 如果用户按下鼠标左键
                if pygame.mouse.get_pressed()[0]:
                    # 获取鼠标坐标
                    pos = pygame.mouse.get_pos()
                    # 如果用户点击“重新开始”
                    if again_rect.left < pos[0] < again_rect.right and \
                            again_rect.top < pos[1] < again_rect.bottom:
                        # 调用main函数，重新开始游戏
                        main()
                    # 如果用户点击“结束游戏”
                    elif gameover_rect.left < pos[0] < gameover_rect.right and \
                            gameover_rect.top < pos[1] < gameover_rect.bottom:
                        # 退出游戏
                        pygame.quit()
                        sys.exit()



        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        #绘制炸弹
        bomb_text = bomb_font.render("× %d" % bomb_num,True,WHITE)
        text_rect = bomb_text.get_rect()
        screen.blit(bomb_image,(10,height - 10 - bomb_rect.height))
        screen.blit(bomb_text,(20 + bomb_rect.width,height - 5 - text_rect.height))

        if not (delay % 5):
            # 切换飞机
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
