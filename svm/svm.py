import pygame
import numpy as np
import sklearn.svm as svm


WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((500, 500))
screen.fill(WHITE)

# сюда записываем точки
points = []
clast = []
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 = левая кнопка мыши - красная точка
            if event.button == 1:
                pygame.draw.circle(screen, RED, event.pos, 10)
                points.append(event.pos)
                clast.append(0)
            # 2 = правая кнопка мыши - зеленый цвет
            if event.button == 3:
                pygame.draw.circle(screen, GREEN, event.pos, 10)
                points.append(event.pos)
                clast.append(1)
        # при нажатии на любую из кнопок отрисовывакем линию
        elif event.type == pygame.KEYDOWN:
            clf = svm.SVC(kernel='linear', C=1)
            clf.fit(points, clast)

            #  вытаскиваем веса
            weights = clf.coef_[0]
            a = weights[0]
            b = weights[1]
            x = np.linspace(0, 800, 2)

            y = -a/b * x - (clf.intercept_[0]) / b

            pygame.draw.line(screen, BLACK, (x[0], y[0]), (x[len(x) - 1], y[len(y) - 1]))


    pygame.display.update()


pygame.quit()
quit()