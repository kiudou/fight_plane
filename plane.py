# -*- coding: utf-8 -*-
import pygame
import random
from sys import exit
#定义敌机类
class Enemy:
	def restart(self): #重置敌机的位置和速度
		self.x = random.randint(50, 400)
		self.y = random.randint(-200, -50)
		self.speed = random.random()+0.1
	def __init__(self): #初始化
		self.restart()
		self.image = pygame.image.load('enemy.png').convert_alpha()
	def move(self): #向下移动
		if self.y < 800 :
			self.y +=self.speed
		else : #重置
			self.restart()

#定义Bullet类。封装子弹相关的数据和方法
class Bullet:
	def __init__(self): #初始变量,两个_,该类被创建时会被自动,不然会出现AttributeError: Bullet instance has no attribute
		self.x = 0
		self.y = -1
		self.image = pygame.image.load('bullet.png').convert_alpha()
		self.active = False #默认不激活
	def move(self): #处理子弹的运动
		if self.active: #激活状态下，向上移动
			self.y -= 3
		if self.y < 0:
			self.active = False
	def restart(self):	#重置子弹位置
		mouseX, mouseY = pygame.mouse.get_pos()
		self.x = mouseX - self.image.get_width()/2
		self.y = mouseY - self.image.get_height()/2
		self.active = True #激活子弹
#定义飞机类
class Plane:
	def restart(self):
		self.x = 200
		self.y = 300
	def __init__(self):
		self.restart()
		self.image = pygame.image.load('plane.png').convert_alpha()
	def move(self):
		 x,y = pygame.mouse.get_pos() #获取鼠标的位置
		 x -= self.image.get_width() / 2 #使得鼠标在飞机图像的最中间
		 y -= self.image.get_height() / 2
		 self.x = x
		 self.y = y
	
def checkHit(enemy, bullet): #检测子弹和飞机是否相撞
	if(bullet.x > enemy.x and bullet.x < enemy.x+enemy.image.get_width()) and \
		(bullet.y > enemy.y and bullet.y < enemy.y+enemy.image.get_height()): #空格+\为代码换行
		enemy.restart()
		bullet.active = False
		return True
	return False

def checkCrash(enemy, plane):#检测敌机与飞机是否相撞
	if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and \
		(plane.y + 0.7*plane.image.get_height() > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
		return True
	return False
	
pygame.init()
screen = pygame.display.set_mode((450,700), 0, 32) #制作窗口
pygame.display.set_caption('fight plane') #窗口名称
background = pygame.image.load('background.jpg').convert() #加载背景图
plane = Plane() #创建飞机对象
enemies = [] #创建敌机list
for i in range(5):
	enemies.append(Enemy())
bullets = [] #创建子弹list
for i in range(5): #list中添加5发子弹
	bullets.append(Bullet())
count_b = len(bullets) #子弹总数
index_b = 0 #即将激活的子弹序号
interval_b = 0 #发射子弹间隔
gameover = False
score = 0
font = pygame.font.Font(None,32) #创建一个font对象,None为默认字体，32为字号
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if gameover and event.type == pygame.MOUSEBUTTONUP: #点击鼠标游戏重置
			plane.restart()
			for e in enemies :
				e.restart()
			for b in bullets :
				b.active = False
			score = 0
			gameover = False
			index_b = 0
			interval_b = 0
	screen.blit(background,(0,0)) #画背景图像，从最左上角开始即（0,0）
	
	if not gameover :
		interval_b -= 1 #发射间隔递减，实际发射间隔受cpu影响
		if interval_b < 0: #间隔小于0时,激发一个子弹
			bullets[index_b].restart()
			interval_b = 100 #重置时间间隔
			index_b = (index_b + 1) %count_b #子弹序号周期性递减
		for b in bullets: #绘制激活的子弹
			if b.active:
				b.move()
				screen.blit(b.image,(b.x,b.y))
				for e in enemies:
					if checkHit(e, b) :#检测激活的子弹是否和飞机相撞
						score += 10
		for e in enemies : #敌机的移动和描述		
			if checkCrash(e, plane) :
				gameover = True
			e.move() 
			screen.blit(e.image,(e.x, e.y))
		plane.move()
		screen.blit(plane.image,(plane.x,plane.y)) #画飞机
		text = font.render("Score:%d" %score,1,(0,0,0))
		screen.blit(text,(0,0)) #在屏幕左上角显示分数
	else :
		text1 = font.render("Score:%d" %score,1,(0,0,0))
		text2 = font.render("click restart",1,(0,0,0))
		screen.blit(text1,(190,400)) #在屏幕中间显示分数
		screen.blit(text2,(170,420))
	pygame.display.update()	#刷新
