from connect4.policy import Policy
from connect4.utils import find_importable_classes
from tournament import run_tournament, play

# Read all files within subfolder of "groups"
participants = find_importable_classes("groups", Policy)

# Build a participant list (name, class)
players = list(participants.items())

W=[]
a=0
t=5
# Run the tournament
for i in range(t):
    champion = run_tournament(
        players,
        play,  # You could also create your own play function for testing purposes
        shuffle=True,
    )
    w,x=champion
    W.append(w)
    if(w == 'Grupo X1'):
        a+=1

print("Champion:", W)
progres = ""
remanining = ""
for i in range(round(a*10/t)):
    progres+="█"
if 10-round(a+10/t) > 0:
    for i in range(11-round(a+10/t)):
        remanining+="■"
print(f"Ganó {a} veces")
print(f"=== {round(a*100/t)}% ["+progres+remanining+"]===")
