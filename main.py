# Example file showing a circle moving on screen
import pygame
import math

print("MAIN")


# pygame setup
pygame.init()

SCREEN_SIZE = (1280, 720)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
is_running = True
degrees_rotation = 0

SIZE_MULTIPLIER = 200
SHAPE_PRECISION = 1
SHOULD_SPIN = True

SCREEN_CENTER	= (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
SHAPE_CENTER 	= (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/3)
FLOOR_CENTER  = (SHAPE_CENTER[0], SHAPE_CENTER[1]+SIZE_MULTIPLIER)



# ______________________ SHAPES ______________________________

# CIRCLE
c1 = []
m1 = SIZE_MULTIPLIER
for o in range(0, 360 * SHAPE_PRECISION):
  x = round(math.cos(math.radians(o)), 3)
  y = round(math.sin(math.radians(o)), 3)
  c1.append( ( x, y ) )

circle = (c1, m1)

# SQUARE
c2 = []
m2 = SIZE_MULTIPLIER*2
for deg in range(0, 360*SHAPE_PRECISION):
  two = deg/SHAPE_PRECISION

  if two <= 45:
    x = 0.5
    y = -0.5 * two / 45

  elif 45 < two <= 90:
    x = 0.5 * (1 - (two - 45) / 45)  # Transition from (0.5, -0.5) to (0, -0.5)
    y = -0.5

  elif 90 < two <= 135:
    x = -0.5 * ((two - 90) / 45)  # Transition from (0, -0.5) to (-0.5, -0.5)
    y = -0.5

  elif 135 < two <= 180:
    x = -0.5
    y = -0.5 * (1 - (two - 135) / 45)  # Transition from (-0.5, -0.5) to (-0.5, 0)

  elif 180 < two <= 225:
    x = -0.5
    y = 0.5 * ((two - 180) / 45)  # Transition from (-0.5, 0) to (-0.5, 0.5)

  elif 225 < two <= 270:
    x = -0.5 * (1 - (two - 225) / 45)  # Transition from (-0.5, 0.5) to (0, 0.5)
    y = 0.5

  elif 270 < two <= 315:
    x = 0.5 * ((two - 270) / 45)  # Transition from (0, 0.5) to (0.5, 0.5)
    y = 0.5

  elif 315 < two < 360:
    x = 0.5
    y = 0.5 * (1 - (two - 315) / 45)  # Transition from (0.5, 0.5) to (0.5, 0)

  c2.append((x, y))

square = (c2, m2)

# HEART
c3 = []
m3 = SIZE_MULTIPLIER*0.945
for deg in range(0, 360*SHAPE_PRECISION):
  radians = math.radians(deg)  # Convert degrees to radians
  x = math.sin(radians) ** 3
  y = -(1 / 16) * (13 * math.cos(radians) - 5 * math.cos(2 * radians) - 2 * math.cos(3 * radians) - math.cos(4 * radians))
  
  c3.append((x, y))

heart = (c3, m3)

# _________________________ FUNCTIONS ___________________________

# draw shape
def drawShape(shape, rotation = 0, color = (255, 255, 255), type = "line"):
  shape_coords = rotate_points(shape[0], rotation)
  multiplier = shape[1]

  for i in range(len(shape_coords)):
    if type == "line":
      pygame.draw.line(screen, color, SHAPE_CENTER, (SHAPE_CENTER[0] + shape_coords[i][0]*multiplier, SHAPE_CENTER[1] + shape_coords[i][1]*multiplier))

    elif type == "outline":
      pos1 = (SHAPE_CENTER[0] + shape_coords[i][0]*multiplier, SHAPE_CENTER[1] + shape_coords[i][1]*multiplier)
      if i == len(shape_coords):
        pos2 = (SHAPE_CENTER[0] + shape_coords[0][0]*multiplier, SHAPE_CENTER[1] + shape_coords[0][1]*multiplier)
      else:
        pos2 = (SHAPE_CENTER[0] + shape_coords[i][0]*multiplier, SHAPE_CENTER[1] + shape_coords[i][1]*multiplier)

      pygame.draw.line(screen, color, pos1, pos2, 3)
  


    elif type == "d_outline":
      pos = (SHAPE_CENTER[0] + shape_coords[i][0]*multiplier, SHAPE_CENTER[1] + shape_coords[i][1]*multiplier)
      pygame.draw.line(screen, color, pos, pos)

    else:
      raise Exception("Invalid type")


# Rotate in 2d
def rotate_points(points, angle_degrees):
  angle_radians = math.radians(angle_degrees)  # Convert degrees to radians
  cos_theta = math.cos(angle_radians)
  sin_theta = math.sin(angle_radians)

  rotated_points = [
    (x * cos_theta - y * sin_theta, x * sin_theta + y * cos_theta)
    for x, y in points
  ]

  return rotated_points


# distance of points
def points_distance(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Generate floor
def generate_floor(shape):
  floorCoords = []
  for coord in shape[0]:
    floorCoords.append( points_distance((0, 0), (coord[0], coord[1])) )
    
    
  return (floorCoords, shape[1])
  

# draw floor
def draw_floor(shape, steps = 0):
  floorCoords = generate_floor(shape)

  x = FLOOR_CENTER[0] - steps*3 - 90
  y = FLOOR_CENTER[1]
  h = floorCoords[1]/2

  distances = []
  for i in range(len(shape[0])-1):
    distances.append( points_distance(shape[0][i], shape[0][i+1]) )
  distances.append( points_distance(shape[0][len(shape[0])-1], shape[0][0]) )
  
  for i in range(len(floorCoords[0])):
    x += distances[i] * shape[1]
    pygame.draw.line(screen, (255, 255, 255), (x, y-floorCoords[0][i]*floorCoords[1]), (x, y+h))


# _________________________ MAIN LOOP ___________________________

while is_running:
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      is_running = False

  # fill the screen with a color to wipe away anything from last frame
  screen.fill(color=(5, 0, 20))

  # Each frame draw:
  if SHOULD_SPIN:
    degrees_rotation += 1
    if degrees_rotation >= 360:
      degrees_rotation = 0


  c = (255, 0, 0)
  shape = heart

  drawShape(shape, degrees_rotation,color=(255, 0,0), type = "line")

  draw_floor(shape, degrees_rotation)
  # drawShape(heart, degrees_rotation, c, type = "line")
  # drawShape(square, degrees_rotation, c, type = "line")



  # flip() the display to draw
  pygame.display.flip()

  # limits FPS
  clock.tick(75)

pygame.quit()
