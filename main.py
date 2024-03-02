import pygame
import threading
import copy
def alphatonum(lis):
  nums=[]
  for i in lis:
    string=i
    for a in string:
      nums.append(ord(a))
  return nums

def lessthan(lis, lis2):
  if len(lis)< len(lis2):
    return True
  else:
    x=lis2
    for i in range(len(x)):
      if lis[i]<lis2[i]:
        return True
      else:
        return False



def start():
  elements=[]

  with open("matches.txt", 'r') as f:
      stats = f.readlines()
  for i in range(len(stats)):
    stats[i] = stats[i].replace(" ","").strip("\n").lower().split(";")
    for a in stats[i]:
      if a not in "1234567890" and a not in elements:
        elements.append(a)
    num= int(stats[i][0])
    current= stats[i][1: (num+1)]
    current.sort()
    current.append(stats[i][-1])
    stats[i]=current
  #print(stats)
  ordered= stats

  for i in range(1, len(ordered)):
    key = ordered[i]
    j= i-1

    keylessthanother= lessthan(key, ordered[j])

    while j>=0 and keylessthanother:

      ordered[j+1]= ordered[j]
      j-=1
      keylessthanother= lessthan(key, ordered[j])
    ordered[j+1]= key

  #print(ordered)

  elements.sort()

  #print(elements)


  numordered= []
  for i in ordered:
    numordered.append(alphatonum(i))

  #numordered
  return numordered, ordered, elements


def find(items, numordered, ordered):
    totallen=0
    num= alphatonum(items)
    for i in items:
        totallen+=len(i)
    for i in range(len(numordered)):
        #print(num, " ", numordered[i][0:totallen])

        if num == numordered[i][0:totallen]:
            print(i)
            result= ordered[i][-1]
            return (result)
    return "none"

####################################################

numordered, ordered, elements = start()

##########################################

""""print(elements)
items=["sdah", "he"]
print(find(items, numordered, ordered))"""

activeObjects = []

class element:
    def __init__(self, PATH, name, x, y):
        self.image = pygame.image.load(PATH)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.name = name
        self.x = x
        self.y = y
        self.isNew = True
    def draw(self, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.x, self.y, 60, 60))

    def drag(self, isMergeds):
        if self.isNew:
          self.isNew = False
        self.dragging = True
        while self.dragging:
            for events in pygame.event.get():
                if events.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                    break
            self.pos = pygame.mouse.get_pos()
            self.draw(self.pos[0], self.pos[1]) 
        if ((self.x > 500) and (self.y > 250) and (self.x < 700) and (self.y < 350)):
            isMergeds.append(self.name)


mergeObjects = []

# Drag logic
def findObject():
    pos=pygame.mouse.get_pos()
    for item in activeObjects:
        print(item)
        if ((pos[0] > item.x) and (pos[1] > item.y) and (pos[0] < item.x+100) and (pos[1] < item.y+100)):
            return item
# Start of input thread
def handleMouse(val):
    while True:
        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONDOWN:
                ele = findObject()
                print(ele)
                if ele != None:
                    ele.drag(mergeObjects)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Universe_Builder 1.0")
clock = pygame.time.Clock()
# Input

itemSelection = []
k = 50
for items in elements:
    pathname = "images/" + items + ".png"
    ellie = element(pathname, element, k, 0)
    k+=150
    itemSelection.append(ellie)
    activeObjects.append(ellie)

inputT = threading.Thread(target=handleMouse, args=(10,))
inputT.start()

k = 50
for item in itemSelection:
  item.draw(k, 600)
  k+=150
  if (k > 1280):
    break

background = pygame.image.load("wallpaper.png")
running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KMOD_LSHIFT:
            rc = find(mergeObjects, numordered, ordered)
            if rc != None:
                ellie = element("image/3135319326_e7c62aa03e_b.jpg", rc, 0, 0)

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(500, 250, 200, 100))

    for item in activeObjects:
        item.draw(item.x, item.y)

    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()