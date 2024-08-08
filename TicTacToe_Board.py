
import pygame

class Player:
	def __init__(self, name, symbol):
		self.name   = name
		self.symbol = symbol
		self.b      = [ [False]*3, [False]*3, [False]*3 ]


class Block:

	def __init__(self, screen, fill_color, border_color, symbol, posX, posY, width, height, border_size):
		self.height 	  = height
		self.width  	  = width
		self.posX    	  = posX
		self.posY   	  = posY
		self.symbol  	  = symbol
		self.rect   	  = pygame.Rect(self.posX, self.posY, self.width, self.height) 
		self.fill_color   = fill_color
		self.border_size  = border_size
		self.border_color = border_color

	def draw(self, screen):
		pygame.draw.rect(screen, self.border_color, self.rect, 1, 25) #int(self.border_size)
		pygame.time.delay(35)
		pygame.display.update()		
		
	def draw_symbol(self, screen):		
		print(self.symbol)	
		font 			= pygame.font.Font('freesansbold.ttf', int(0.66*min(self.width,self.height)))
		text 			= font.render(self.symbol, True, (0, 0, 0))
		textRect 		= text.get_rect()
		textRect.center = ( int(self.posX + (self.width/2)) , int(self.posY + (self.height/2)) )
		screen.blit(text, textRect)
		pygame.display.update()		

	
	def is_empty(self):
		return self.symbol == None	


	def __setattr__(self, name, value):
		if name == 'posY':
			pass
		super().__setattr__(name, value)


class Board:

	def __init__(self, height, width):
		self.height 	   = height 
		self.width 		   = width
		self.blocks 	   = [[None]*3,[None]*3,[None]*3]
		self.status_bar	   = None		
		self.filled_blocks = 0

	def draw(self, screen):
		#blocks draw code
		for i in range(3):
			for j in range(3):
				self.blocks[i][j].draw(screen)

		#status bar draw code
		self.status_bar.draw(screen)

		#pygame.display.update()

	def find_block(self,mouse_pos):
		print(mouse_pos)
		for i in range(3):
			for j in range(3):
				if self.blocks[i][j].rect.collidepoint(mouse_pos):
					return (i, j)
		

		return (None, None)



class Status_Bar:
	def __init__(self, height, width, posX, posY, border_size, player, turn, fill_color, border_color):
		self.height         = height
		self.width    	    = width
		self.posX     	    = posX
		self.posY     	    = posY
		self.border_size    = border_size
		self.rect     	    = pygame.Rect(self.posX, self.posY, self.width, self.height)
		self.player         = player
		self.turn		    = turn
		self.fill_color     = fill_color
		self.border_color   = border_color 

		self.font_size		= int( 0.77 * ( min(self.width,self.height) )/2 )
		self.font 	    	= pygame.font.Font('freesansbold.ttf', self.font_size)	
		
		self.btn_posX       = self.width   * 0.67
		self.btn_posY		= self.height  * 0.15
		self.btn_width		= self.width   / 3.2
		self.btn_height		= self.height  * 0.7
		self.button_rect    = pygame.Rect(self.btn_posX, self.btn_posY, self.btn_width, self.btn_height)

	def draw(self, screen):
		pygame.draw.rect(screen, self.border_color, self.rect,       -1, 23)  #int(self.border_size)
		pygame.draw.rect(screen, self.border_color, self.button_rect, 2, 23)  #int(self.border_size*0.8)
		pygame.display.update()

	def update_sb(self, screen, n):
		black       = (0,0,0)		
		p0_text     = self.font.render(n, True, black, self.fill_color)
		p0_textRect = p0_text.get_rect()
		p0_textRect = ( self.posX + (self.width/10) , self.posY + (self.height*0.4) )
		screen.blit(p0_text, p0_textRect)

		btn_text 			= self.font.render('Restart Game', True, black, self.fill_color)
		btn_textRect 		= btn_text.get_rect()
		btn_textRect.center = ( self.btn_posX + self.btn_width/2 , self.btn_posY + self.btn_height*0.50 )
		screen.blit(btn_text, btn_textRect)

		pygame.display.update()	


class TicTacToe:

	def __init__(self):
		self.height = 600
		self.width  = 600
		self.title  = 'TicTacToe'
		self.colors = [(230, 230, 230),(48, 141, 70), (0, 0, 128)]	 #239,200,177  48, 141, 70

		pygame.init()

		self.screen        = self.create_screen()
		self.board   	   = None
		self.sb_height     = None
		self.sb_width	   = None
		self.turn    	   = None
		self.block_h 	   = None
		self.block_w 	   = None
		self.players 	   = [None, None]
		self.border_size   = None
		

	def create_screen(self):
		screen = pygame.display.set_mode((self.width, self.height)) 			# draws a screen
		pygame.display.set_caption(self.title)				
		screen.fill(self.colors[0])
		return screen


	def change_turn(self):
		if self.turn == 0:
			self.turn   = 1
			player_info = str(self.players[self.turn].name) + ': ' + str(self.players[self.turn].symbol)
			#self.board.status_bar.update_sb(self.screen, player_info)
		else:
			self.turn   = 0
			player_info = str(self.players[self.turn].name) + ': ' + str(self.players[self.turn].symbol)

		self.board.status_bar.update_sb(self.screen, player_info)


	def winning_strategy(self):			
		def cols(alist):
			return [[row[i] for row in alist] for i in range(3)]

		mat = self.players[self.turn].b

		h   = any( [ all(row)    for row in mat]       )		
		v   = any( [ all(col)    for col in cols(mat)] )
		d1  = all( [ mat[i][i]   for i   in range(3) ] )	
		d2  = all( [ mat[i][2-i] for i   in range(3) ] ) 

		result = any([h, v, d1, d2])

		if self.board.filled_blocks == 9 and result != True:
			tie_str = "it's a Tie...restarting"
			self.board.status_bar.update_sb(self.screen, tie_str)
			pygame.time.delay(2200)						
			return 'restart_game'
		return result

	
	def run(self):
		self.board         = Board(self.height*0.99, self.width*0.98)	# initialize board height and width
		self.border_size   = int(min(self.height, self.width) * 0.01)
	
		self.turn       = 0								# start game with player1's turn
		self.players[0] = Player('Player 0', 'x')		# initializing players and its symbols
		self.players[1] = Player('Player 1', 'o')		# initializing players and its symbols

		self.sb_height = self.board.height * 0.08 		# status bar height is 8 percent of board height
		self.sb_width  = self.board.width  				# status bar width  is same as board width

		#status bar init
		self.board.status_bar = Status_Bar(self.sb_height, self.sb_width, 0, 0, self.border_size, self.players, self.turn, self.colors[0], self.colors[1])

		self.block_h = int( self.board.height * (0.92) / 3 )		# calculates & stores block height
		self.block_w = int( self.board.width           / 3 )		# calculates & stores block width

		# initializing 9 blocks to draw 
		for i in range(0,3):
			for j in range(0,3):
				x = j * self.block_w + 6
				y = i * self.block_h + (0.08 * self.board.height)				
				self.board.blocks[i][j]  = \
						Block(self.screen, self.colors[0],  self.colors[1], None, x, y, self.block_w, self.block_h, self.border_size) 
	

		self.board.draw(self.screen)					# draw blocks
		
		# construction of player info to display on status bar
		player_info = str(self.players[self.turn].name) + ': ' + str(self.players[self.turn].symbol)
		self.board.status_bar.update_sb(self.screen, player_info)

		running = True
		while(running):
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					quit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						quit()
				
				elif event.type == pygame.MOUSEBUTTONDOWN:					
					p = pygame.mouse.get_pos()
					(i,j) = self.board.find_block(p) 
					
					if i != None and self.board.blocks[i][j].is_empty():

						self.board.blocks[i][j].symbol = self.players[self.turn].symbol
						self.board.filled_blocks += 1		
						self.players[self.turn].b[i][j] = True
						self.board.blocks[i][j].draw_symbol(self.screen)
						
						res = self.winning_strategy()	
						if res == True:
							winner = str(self.players[self.turn].name) + ' is winner..restarting'
							self.board.status_bar.update_sb(self.screen, winner)	
							pygame.time.delay(3000)
							return					
						elif res == 'restart_game':
							return
						
						self.change_turn()	
					
					if i == None:
						if self.board.status_bar.button_rect.collidepoint(p):
							self.board.status_bar.update_sb(self.screen, 'Restarting ')
							del self.screen
							return
						else:
							continue


#game = TicTacToe()
#game.run()


